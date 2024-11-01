import os
import pathlib
import tempfile

import camelot

import signer.pdf_creator as signer


def test_creates():
    with tempfile.TemporaryDirectory() as td:
        tmp_file_name = "temp_file.pdf"
        tmp_file_path = pathlib.Path(td, tmp_file_name)
        assert not os.path.exists(tmp_file_path)

        creator = signer.PdfCreator(name="Test test")
        creator.create_pdf()
        creator.output(str(tmp_file_path))

        assert os.path.exists(tmp_file_path)


def test_name():
    name = "TEST NAME"
    with tempfile.TemporaryDirectory() as td:
        tmp_file_name = "temp_file.pdf"
        tmp_file_path = pathlib.Path(td, tmp_file_name)
        assert not os.path.exists(tmp_file_path)

        creator = signer.PdfCreator(name=name)
        creator.create_pdf()
        creator.output(str(tmp_file_path))

        assert os.path.exists(tmp_file_path)
        data = camelot.read_pdf(str(tmp_file_path), flavor="stream")[0]  # type: ignore
        assert data.cells[1][2].text.strip() == name  # type: ignore
