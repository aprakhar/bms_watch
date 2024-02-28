import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any, Final
from selenium import webdriver
from selenium.webdriver.common.by import By
from twilio.rest import Client
from selenium.common.exceptions import NoSuchElementException

from bms_watch.constants import SECOND


def parse_month(month: str) -> int:
    hashmap: dict[str, int] = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    return hashmap[month.casefold()]


class ReadWebsite:
    """Usage:
    with ReadWebsite as reader:
        reader.read(booking)
    """

    def __init__(self, client: Client, from_number: str, to_numbers: list[str]) -> None:
        self._client = client
        self._from_number = from_number
        self._to_numbers = to_numbers

    def _check_open_booking(
        self, name: str, url: str, check_year: int, check_month: int, check_date: int
    ) -> None:
        _driver = webdriver.Chrome()
        _driver.get(url)

        date_html = _driver.find_element(By.CLASS_NAME, "date-href")
        date: int = int(date_html.find_element(By.CLASS_NAME, "date-numeric").text)
        month: int = parse_month(
            date_html.find_element(By.CLASS_NAME, "date-month").text
        )
        year: int = datetime.now().year
        first_date = datetime(year, month, date)
        no_of_days_open: timedelta = timedelta(
            days=len(_driver.find_elements(By.CLASS_NAME, "date-href"))
        )
        last_date = first_date + no_of_days_open - timedelta(days=1)

        if last_date >= datetime(check_year, check_month, check_date):
            msg_body: Final[str] = f"Tickets are available for {name}!"
            self._send_sms(msg_body)

        _driver.quit()

    def _check_closed_booking(self, name: str, url: str) -> None:
        _driver = webdriver.Chrome()
        _driver.get(url)

        try:
            _driver.find_element(By.XPATH, "//div[contains(@id, 'page-cta-container')]")
        except NoSuchElementException:
            print("Tickets are not available yet")
        else:
            msg_body: Final[str] = f"Tickets are available for {name}!"
            self._send_sms(msg_body)

        _driver.quit()

    async def read(self, booking: dict[str, Any]) -> None:
        for movie, info in booking["open"].items():
            self._check_open_booking(
                movie, info["url"], info["year"], info["month"], info["date"]
            )

        await asyncio.sleep(5 * SECOND)

        for movie, info in booking["closed"].items():
            self._check_closed_booking(movie, info["url"])

    def _send_sms(self, msg: str) -> None:
        logging.info(msg)

        for to_number in self._to_numbers:
            self._client.messages.create(
                from_=self._from_number, body=msg, to=to_number
            )
