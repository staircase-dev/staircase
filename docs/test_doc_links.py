import pytest
import requests

urls = [
    # README.md
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html",  # getting_started.rst too
    "https://github.com/firstcontributions/first-contributions",  # contributing.rst too
    "https://pandas.pydata.org/pandas-docs/stable/development/contributing.html",  # contributing.rst too
    "http://semver.org/",
    "https://staircase.mit-license.org/",
    "http://www.grantjenks.com/docs/sortedcontainers/",
    # getting_started.rst
    "https://mathworld.wolfram.com/SimplyConnected.html",
    "https://en.wikipedia.org/wiki/Step_function",
    "https://mathworld.wolfram.com/Interval.html",
    "https://matplotlib.org",  # Case Study Queue Analysis too
    # learning_resources.rst
    "https://2020.pycon.org.au/",
    "https://2020.pycon.org.au/program/3tds8k/",
    "https://www.youtube.com/embed/CS1dZ-01b-Q",
    # timezones.ipynb
    "https://en.wikipedia.org/wiki/Daylight_saving_time",
    "http://pytz.sourceforge.net/",
    "https://en.wikipedia.org/wiki/Coordinated_Universal_Time",
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html",
    # Case Study State Machine
    "https://en.wikipedia.org/wiki/State_diagram",
    # Case Study Queue Analysis
    "https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#datetimes",
    "https://en.wikipedia.org/wiki/Empirical_distribution_function",
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.plot.html",
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rolling.html",
    "https://matplotlib.org/",  # Case Study Hotel Stays too
    "https://seaborn.pydata.org/",  # Case Study Hotel Stays too
    # Case Study Hotel Stays
    "https://www.kaggle.com/jessemostipak/hotel-booking-demand",
    "https://vita.had.co.nz/papers/tidy-data.pdf",
    # FAQ
    "https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html#timedelta-limitations",
]


@pytest.mark.parametrize("url", urls)
def test(url):
    code = requests.head(url).status_code
    assert code < 400, f"URL not found {url}"
