import datetime
import pathlib
from dataclasses import dataclass


@dataclass
class AttendanceParams:
    name: str = ""
    month: int = 0
    year: int = 0
    additional_workdays: list[datetime.date] | None = None
    public_holidays: list[datetime.date] | None = None
    vacation_days: list[datetime.date] | None = None
    signature: pathlib.Path | None = None

    @property
    def date(self) -> datetime.date:
        if self.month and self.year:
            return datetime.date(year=self.year, month=self.month, day=1)
        return datetime.date.today()
