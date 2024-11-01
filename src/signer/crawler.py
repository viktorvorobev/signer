import calendar
import datetime
import enum
import os

import requests
from bs4 import BeautifulSoup, Tag

MIN_MONTH = 1
MAX_MONTH = 12


class DayType(enum.Enum):
    WORK_DAY = enum.auto()
    REST_DAY = enum.auto()
    HOLIDAY = enum.auto()


MONTH_NUM_TO_STR = {
    1: "Január",
    2: "Február",
    3: "Március",
    4: "Április",
    5: "Május",
    6: "Június",
    7: "Július",
    8: "Augusztus",
    9: "Szeptember",
    10: "Október",
    11: "November",
    12: "December",
}

DIV_CLASS_TO_DAY_TYPE = {
    "caltdred": DayType.HOLIDAY,
    "caltdsarga": DayType.HOLIDAY,
    "caltdszurke": DayType.WORK_DAY,
    "caltd": DayType.WORK_DAY,
    "caltdb": DayType.REST_DAY,
}


class Crawler:
    BASE_URL = "https://www.hrportal.hu"

    def __init__(self, year: int, month: int):
        if month < MIN_MONTH or month > MAX_MONTH:
            raise ValueError(f"Month must be in range {MIN_MONTH} - {MAX_MONTH}")
        self.year = year
        self.month = month

        self._days: dict[DayType, list[datetime.date]] = {
            DayType.HOLIDAY: [],
            DayType.WORK_DAY: [],
            DayType.REST_DAY: [],
        }

    @property
    def workdays(self) -> list[datetime.date]:
        return self._days[DayType.WORK_DAY]

    @property
    def rest_days(self) -> list[datetime.date]:
        return self._days[DayType.REST_DAY]

    @property
    def holidays(self) -> list[datetime.date]:
        return self._days[DayType.HOLIDAY]

    def crawl(self):
        page = self._get_page_content()
        self._parse(page)

    def _get_page_content(self):
        endpoint = f"munkaido-{self.year}.html"
        url = f"{self.BASE_URL}/{endpoint}"

        if not os.path.exists(endpoint):
            with open(endpoint, "w") as f:
                print(f"Fetching content from {url}")
                response = requests.get(url)
                f.write(response.text)

        print(f"Reading cached content from {url}")
        with open(endpoint, "r") as f:
            return f.read()

    def _parse(self, page: str):
        soup = BeautifulSoup(page, "html.parser")
        month_str = MONTH_NUM_TO_STR[self.month]
        month = soup.find("div", string=month_str)  # row with exact month name

        if not month or not month.parent:
            raise RuntimeError(f"Failed to find {month_str}")
        month = month.parent  # calendar month block

        monthrange = calendar.monthrange(year=self.year, month=self.month)
        for day in range(monthrange[1]):
            _day = day + 1  # convert from range to date
            day_div = month.find("div", string=f"{_day}")
            if not day_div or not isinstance(day_div, Tag):
                raise RuntimeError(f"Failed to find {_day} day for {month_str}")
            day_div_class = day_div["class"][0]

            date_type = DIV_CLASS_TO_DAY_TYPE[day_div_class]
            self._days[date_type].append(
                datetime.date(
                    year=self.year,
                    month=self.month,
                    day=_day,
                )
            )


if __name__ == "__main__":
    crawler = Crawler(year=2024, month=8)
    crawler.crawl()
    print(crawler.holidays)
