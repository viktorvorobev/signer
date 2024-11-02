# type: ignore

import datetime

import pytest

from signer.pdf_creator import PdfCreator

from . import utils


@pytest.mark.parametrize("year", (2024, 2025))
@pytest.mark.parametrize("month", (i + 1 for i in range(12)))
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
