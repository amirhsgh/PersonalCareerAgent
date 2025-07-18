from PyPDF2 import PdfReader
from typing import BinaryIO


def extract_pdf(file: BinaryIO) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()
