# type: ignore

from . import utils


def test_name():
    name = "TEST NAME"
    data = utils.create_pdf_and_get_result(name=name)
    assert data.name == name
