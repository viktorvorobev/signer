# type: ignore

import calendar
import copy
import dataclasses
import datetime
import os
import pathlib
import random
import tempfile

import camelot
import camelot.core as camelot_core

from signer.constants import AttendanceParams
from signer.pdf_creator import PdfCreator


@dataclasses.dataclass
class Day:
    date: str
    start_time: str
    end_time: str
    work_hours: str


@dataclasses.dataclass
class PdfOutput:
    title: str
    name: str
    header_row: list[str]
    days: list[Day]
    workdays_total_title: str
    workdays_total: int
    work_hours_total_title: str
    work_hours_total: int
    public_holidays_title: str
    public_holidays: int
    vacation_days_title: str
    vacation_days: int


def create_pdf_and_get_result(*args, **kwargs) -> PdfOutput:
    params = AttendanceParams(*args, **kwargs)
    data = _create_pdf_and_get_result(params)

    converted = _convert_table(data)
    _validate_static_info(converted)

    return converted


def _create_pdf_and_get_result(params) -> camelot_core.Table:
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_file_name = "temp_file.pdf"
        tmp_file_path = pathlib.Path(temp_dir, tmp_file_name)
        assert not os.path.exists(tmp_file_path)

        creator = PdfCreator(params)
        creator.create_pdf()
        creator.output(str(tmp_file_path))

        assert os.path.exists(tmp_file_path)
        return camelot.read_pdf(str(tmp_file_path), flavor="stream")[0]


def _convert_table(table: camelot_core.Table) -> PdfOutput:
    rows = copy.deepcopy(table.cells)
    (
        title_row,
        name_row,
        header_row_hun,
        header_row_en,
        *day_rows,
        workdays_title_hu,
        workdays_num,
        workdays_title_en,
        work_hours_title_hu,
        work_hours_num,
        work_hours_title_en,
        holidays_title_hu,
        holidays_num,
        holidays_title_en,
        vacations_title_hu,
        vacations_num,
        vacations_title_en,
    ) = rows

    return PdfOutput(
        title=_parse_title_row(title_row),
        name=_parse_name_row(name_row),
        header_row=_parse_column_names(
            header_row_hun,
            header_row_en,
        ),
        days=_parse_days(day_rows),
        workdays_total_title=_merge_hu_en(
            workdays_title_hu[0],
            workdays_title_en[0],
        ),
        workdays_total=_parse_footer_num(workdays_num),
        work_hours_total_title=_merge_hu_en(
            work_hours_title_hu[0],
            work_hours_title_en[0],
        ),
        work_hours_total=_parse_footer_num(work_hours_num),
        public_holidays_title=_merge_hu_en(
            holidays_title_hu[0],
            holidays_title_en[0],
        ),
        public_holidays=_parse_footer_num(holidays_num),
        vacation_days_title=_merge_hu_en(
            vacations_title_hu[0],
            vacations_title_en[0],
        ),
        vacation_days=_parse_footer_num(vacations_num),
    )


def _parse_title_row(title_row: camelot_core.Cell) -> str:
    return title_row[2].text.strip()


def _parse_name_row(name_row: camelot_core.Cell) -> str:
    return name_row[2].text.strip()


def _merge_hu_en(hu_row: camelot_core.Cell, en_row: camelot_core.Cell) -> str:
    return "\n".join((hu_row.text.strip(), en_row.text.strip())).strip()


def _parse_column_names(
    header_row_hun: list[camelot_core.Cell],
    header_row_en: list[camelot_core.Cell],
) -> tuple[str]:
    return tuple(_merge_hu_en(hu, en) for hu, en in zip(header_row_hun, header_row_en))


def _parse_days(day_rows: list[camelot_core.Cell]) -> list[Day]:
    return [
        Day(
            date=day_row[0].text.strip(),
            start_time=day_row[1].text.strip(),
            end_time=day_row[2].text.strip(),
            work_hours=day_row[3].text.strip(),
        )
        for day_row in day_rows
    ]


def _parse_footer_num(footer_row: camelot_core.Cell) -> int:
    return int(footer_row[3].text.strip())


def _validate_static_info(converted: PdfOutput):
    assert converted.header_row == PdfCreator.COLUMNS
    assert converted.workdays_total_title == PdfCreator.WORKDAYS_TOTAL_NAME
    assert converted.work_hours_total_title == PdfCreator.WORK_HOURS_TOTAL_NAME
    assert converted.public_holidays_title == PdfCreator.PUBLIC_HOLIDAYS_NAME
    assert converted.vacation_days_title == PdfCreator.VACATION_DAYS

    for day in converted.days:
        if day.start_time:
            assert day.start_time == PdfCreator.START_TIME
        if day.end_time:
            assert day.end_time == PdfCreator.END_TIME


def get_random_days_in_month(year: int, month: int, days_amount: int, weekdays: bool = True) -> list[datetime.datetime]:
    forbidden_days = (5, 6) if weekdays else (0, 1, 2, 3, 4)
    vacation_days = set()
    days_in_month = calendar.monthrange(year=year, month=month)[1]
    while len(vacation_days) < days_amount:
        try_day = random.choice(range(1, days_in_month + 1))
        try_datetime = datetime.datetime(year=year, month=month, day=try_day)
        if try_datetime.weekday() in forbidden_days:
            continue
        vacation_days.add(try_datetime)
    return list(vacation_days)
