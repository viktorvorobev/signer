import calendar
import datetime

import fpdf
import fpdf.table
import pathlib

RED_CELL = fpdf.FontFace(family="Times", emphasis="B", size_pt=12, fill_color=(240, 192, 193))
WHITE_CELL = fpdf.FontFace(family="Times", emphasis="B", size_pt=12, fill_color=(255, 255, 255))
FILL_COLOR_WHITE = (0, 0, 0)

TEXT_STYLE_NORMAL = {"family": "Times", "style": "", "size": 12}
TEXT_STYLE_BALD = {"family": "Times", "style": "B", "size": 12}


class PdfCreator(fpdf.FPDF):
    TITLE = "Emlid Tech Kft. Jelenléti ív - {}"
    COLUMNS = ("", "Kezdés\nStart time", "Vége\nEnd time", "Ledolgozott óra\nWork hours", "Aláírás\nSignature")
    START_TIME = "9:00"
    END_TIME = "18:00"
    WORK_HOURS = 8

    WORKDAYS_TOTAL_NAME = "Ledolgozott napok száma\nWorkdays total"
    WORK_HOURS_TOTAL_NAME = "Ledolgozott órák száma\nWork hours total"
    PUBLIC_HOLIDAYS_NAME = "Ünnepnapok száma\nPublic holidays"
    VACATION_DAYS = "Szabadnapok száma\nVacation days"

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        month: int = 0,
        year: int = 0,
        public_holidays: list[datetime.date] | None = None,
        vacation_days: list[datetime.date] | None = None,
        signature: pathlib.Path | None = None,
    ) -> None:
        super().__init__()
        self._name = name
        if month and year:
            self._date = datetime.datetime(year=year, month=month, day=1)
        else:
            self._date = datetime.datetime.today()

        self._public_holidays = public_holidays if public_holidays else []
        self._vacation_days = vacation_days if vacation_days else []
        self._signature = signature
        self._work_days_total = 0

    def create_pdf(self) -> None:
        self.add_page()
        self.set_font(**TEXT_STYLE_NORMAL)
        self.set_fill_color(FILL_COLOR_WHITE)
        with self.table(line_height=5, col_widths=(0.26, 0.16, 0.16, 0.16, 0.25)) as table:
            self._create_header(table)
            self._create_body(table)
            self._create_footer(table)

    def _create_header(self, table: fpdf.table.Table) -> None:
        self.set_font(**TEXT_STYLE_BALD)
        row = table.row(style=RED_CELL)
        row.cell(self.TITLE.format(self._date.strftime("%Y %B")), align=fpdf.enums.Align.C, colspan=5)

        row = table.row(style=RED_CELL)
        row.cell(self._name, align=fpdf.enums.Align.C, colspan=5)

        self.set_font(**TEXT_STYLE_NORMAL)
        row = table.row(style=RED_CELL)
        for title in self.COLUMNS:
            row.cell(title, align=fpdf.enums.Align.C)

    def _create_body(self, table: fpdf.table.Table) -> None:
        monthrange = calendar.monthrange(year=self._date.year, month=self._date.month)
        for day in range(monthrange[1]):
            date = datetime.datetime(year=self._date.year, month=self._date.month, day=day + 1)

            if date.weekday() not in (5, 6):  # saturday and sunday
                row = table.row(style=WHITE_CELL)
                row.cell(f"{date.day}", align=fpdf.enums.Align.C)
                row.cell(self.START_TIME, align=fpdf.enums.Align.C)
                row.cell(self.END_TIME, align=fpdf.enums.Align.C)
                if date in self._public_holidays:
                    row.cell("Public Holiday", align=fpdf.enums.Align.C)
                elif date in self._vacation_days:
                    row.cell("Vacation", align=fpdf.enums.Align.C)
                else:
                    self._work_days_total += 1
                    row.cell(f"{self.WORK_HOURS}", align=fpdf.enums.Align.C)
                if self._signature:
                    row.cell(img=self._signature)
                else:
                    row.cell()

            else:
                row = table.row(style=RED_CELL)
                for _ in self.COLUMNS:
                    row.cell()

    def _create_footer(self, table: fpdf.table.Table) -> None:
        row = table.row(style=WHITE_CELL)
        row.cell(self.WORKDAYS_TOTAL_NAME, align=fpdf.enums.Align.C)
        row.cell(f"{self._work_days_total}", colspan=4, align=fpdf.enums.Align.C)

        row = table.row(style=WHITE_CELL)
        row.cell(self.WORK_HOURS_TOTAL_NAME, align=fpdf.enums.Align.C)
        row.cell(f"{self._work_days_total * self.WORK_HOURS}", colspan=4, align=fpdf.enums.Align.C)

        row = table.row(style=WHITE_CELL)
        row.cell(self.PUBLIC_HOLIDAYS_NAME, align=fpdf.enums.Align.C)
        row.cell(f"{len(self._public_holidays)}", colspan=4, align=fpdf.enums.Align.C)

        row = table.row(style=WHITE_CELL)
        row.cell(self.VACATION_DAYS, align=fpdf.enums.Align.C)
        row.cell(f"{len(self._vacation_days)}", colspan=4, align=fpdf.enums.Align.C)


if __name__ == "__main__":
    pdf = PdfCreator(
        name="Vorobev Viktor",
        vacation_days=[],
        public_holidays=[datetime.datetime(year=2024, month=10, day=23)],
        signature=pathlib.Path("./example.png"),
    )
    pdf.create_pdf()
    pdf.output("test.pdf")
