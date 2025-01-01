# type: ignore

import datetime

import pytest

from signer.pdf_creator import PdfCreator

from . import utils

YEARS = (2024, 2025)
MONTHS = tuple(range(1, 13))


@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("month", MONTHS)
def test_title(month: int, year: int):
    name = "Name Surname"
    result = utils.create_pdf_and_get_result(name=name, month=month, year=year)
    date = datetime.datetime(year=year, month=month, day=1)
    expected_title = PdfCreator.TITLE.format(date.strftime("%Y %B"))
    assert result.name == name
    assert result.title == expected_title


def test_name():
    name = "TEST NAME"
    data = utils.create_pdf_and_get_result(name=name)
    assert data.name == name


@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("month", MONTHS)
def test_holiday(month: int, year: int):
    name = "Name Surname"

    public_holidays = utils.get_random_days_in_month(year=year, month=month, days_amount=4)

    result = utils.create_pdf_and_get_result(
        name=name,
        month=month,
        year=year,
        public_holidays=list(public_holidays),
    )

    assert result.public_holidays == len(public_holidays)


@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("month", MONTHS)
def test_vacation_days(month: int, year: int):
    name = "Name Surname"

    vacation_days = utils.get_random_days_in_month(year=year, month=month, days_amount=5)

    result = utils.create_pdf_and_get_result(
        name=name,
        month=month,
        year=year,
        vacation_days=list(vacation_days),
    )

    assert result.vacation_days == len(vacation_days)
