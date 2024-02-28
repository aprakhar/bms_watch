import asyncio
from json import dumps
from textwrap import indent
from tomllib import load
from typing import Any, Final
from bms_watch.constants import HOUR
from bms_watch.selenium.read_website import ReadWebsite
from twilio.rest import Client


async def _main() -> None:
    config: Final[dict[str, Any]] = _read_config()
    client = Client(
        config["twilio"]["secrets"]["account_sid"],
        config["twilio"]["secrets"]["auth_token"],
    )
    from_number = config["twilio"]["from_"]["from_"]
    to_numbers = config["twilio"]["to"]["to"]

    while True:
        await ReadWebsite(
            client=client, from_number=from_number, to_numbers=to_numbers
        ).read(booking=config["booking"])
        await asyncio.sleep(1 * HOUR)


def _read_config(filepath: str = "config.toml") -> dict[str, Any]:
    data: dict[str, Any]
    with open(filepath, "rb") as fptr:
        data = load(fptr)
    return data


if __name__ == "__main__":
    asyncio.run(_main())
