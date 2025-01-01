import datetime

import pytest

from collections import namedtuple
from signer.crawler import Crawler, CrawledData

ExpectedCrawledData = namedtuple("ExpectedCrawledData", ["holidays", "additional_workdays"])

EXPECTED_RESULTS = {
    (2024, 1): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 1, 1),
        ],
        additional_workdays=[],
    ),
    (2024, 2): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2024, 3): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 3, 15),
            datetime.date(2024, 3, 29),
        ],
        additional_workdays=[],
    ),
    (2024, 4): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 4, 1),
        ],
        additional_workdays=[],
    ),
    (2024, 5): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 5, 1),
            datetime.date(2024, 5, 20),
        ],
        additional_workdays=[],
    ),
    (2024, 6): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2024, 7): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2024, 8): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 8, 19),
            datetime.date(2024, 8, 20),
        ],
        additional_workdays=[
            datetime.date(2024, 8, 3),
        ],
    ),
    (2024, 9): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2024, 10): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 10, 23),
        ],
        additional_workdays=[],
    ),
    (2024, 11): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 11, 1),
        ],
        additional_workdays=[],
    ),
    (2024, 12): ExpectedCrawledData(
        holidays=[
            datetime.date(2024, 12, 24),
            datetime.date(2024, 12, 25),
            datetime.date(2024, 12, 26),
            datetime.date(2024, 12, 27),
        ],
        additional_workdays=[
            datetime.date(2024, 12, 7),
            datetime.date(2024, 12, 14),
        ],
    ),
    (2025, 1): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 1, 1),
        ],
        additional_workdays=[],
    ),
    (2025, 2): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2025, 3): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2025, 4): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 4, 18),
            datetime.date(2025, 4, 21),
        ],
        additional_workdays=[],
    ),
    (2025, 5): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 5, 1),
            datetime.date(2025, 5, 2),
        ],
        additional_workdays=[
            datetime.date(2025, 5, 17),
        ],
    ),
    (2025, 6): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 6, 9),
        ],
        additional_workdays=[],
    ),
    (2025, 7): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2025, 8): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 8, 20),
        ],
        additional_workdays=[],
    ),
    (2025, 9): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2025, 10): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 10, 23),
            datetime.date(2025, 10, 24),
        ],
        additional_workdays=[
            datetime.date(2025, 10, 18),
        ],
    ),
    (2025, 11): ExpectedCrawledData(
        holidays=[],
        additional_workdays=[],
    ),
    (2025, 12): ExpectedCrawledData(
        holidays=[
            datetime.date(2025, 12, 24),
            datetime.date(2025, 12, 25),
            datetime.date(2025, 12, 26),
        ],
        additional_workdays=[
            datetime.date(2025, 12, 13),
        ],
    ),
}

YEARS = (2024, 2025)
MONTHS = tuple(range(1, 13))


def get_crawled_data(year: int, month: int) -> CrawledData:
    crawler = Crawler(year=year, month=month)
    data = crawler.crawl()
    return data


@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("month", MONTHS)
def test_crawler(year: int, month: int):
    data = get_crawled_data(year=year, month=month)
    expected = EXPECTED_RESULTS[(year, month)]
    assert data.holidays == expected.holidays
    assert data.additional_workdays == expected.additional_workdays


def test_crawler_value_error():
    for i in (0, 13):
        with pytest.raises(ValueError):
            Crawler(year=2024, month=i)
