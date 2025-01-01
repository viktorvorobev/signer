# type: ignore

import calendar
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


@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("month", MONTHS)
def test_additional_workdays(month: int, year: int):
    name = "Name Surname"

    workdays = 0
    days_in_month = calendar.monthrange(year=year, month=month)[1]
    for day in range(days_in_month):
        date = datetime.datetime(year=year, month=month, day=day + 1)
        if date.weekday() not in (5, 6):
            workdays += 1

    additional_workdays_amount = 2
    additional_workdays = utils.get_random_days_in_month(
        year=year,
        month=month,
        days_amount=additional_workdays_amount,
        weekdays=False,
    )
    result = utils.create_pdf_and_get_result(
        name=name,
        month=month,
        year=year,
        additional_workdays=list(additional_workdays),
    )
    assert result.workdays_total == workdays + additional_workdays_amount
    assert result.work_hours_total == (workdays + additional_workdays_amount) * PdfCreator.WORK_HOURS
