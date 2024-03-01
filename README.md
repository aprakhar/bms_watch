# Summary

Python program to notify when next batch movie tickets are available 
for movies which already have some dates open.
It checks if the tickets are available every hour. 
It sends a SMS when a movie is open for booking at the specified date.

# Steps to use for Users

- [ ] Install python3.12 (tutorials on web)
- [ ] Clone repo
- [ ] Update installers `python3.12 -m pip install --no-cache-dir --force-reinstall setuptools`
- [ ] Install `python3.12 -m pip install bms_watch`
- [ ] Create twilio account
- [ ] Add your email and phone number to your twilio account
- [ ] Add the details in [config file](config.toml)
- [ ] Run the program `python3.12 -m bms_watch`

# Editing the [config file](config.toml)

After creating a twilio account, add `account_sid`, `auth_token` & `from_`.
Next, verify the recipient phone numbers on twilio website and then
add those phone numbers in `to`

## Case 1: Booking is open for few dates

If a movie is already open for booking and you'd like to be notified when next dates open, add an entry as follows

```TOML
[booking.open."Dune2"]
url = "http://in.bookmyshow.com/buytickets/dune-part-two-imax-bengaluru/movie-bang-ET00387000-MT/20240229"
date = 7
month = 3
year = 2024
```

where url is the website where current open dates are listed;
date, month & year is the date which you want to be notified for.

## Case 2: Booking has not been opened for any date

If no dates are open for booking then url will be the homepage of the movie.

```TOML
[booking.closed.Shaitaan]
url = "http://in.bookmyshow.com/bengaluru/movies/operation-valentine/ET00361961"
```

# Steps to use for Developers

- [ ] Install python3.12 (tutorials on web)
- [ ] Clone repo
- [ ] Create virtual environment `python3.12 -m venv venv`
- [ ] Activate virtual environment `. .\venv\Scripts\activate`
- [ ] Install `python3.12 -m pip install -e bms_watch`
- [ ] Create twilio account
- [ ] Add your email and phone number to your twilio account
- [ ] Add the details in [config file](config.toml)
- [ ] Run the program `python3.12 -m bms_watch`

# TODO

1. [ ] Add logging support
