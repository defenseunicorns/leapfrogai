"""Parse a helper for parsing files into documents."""

from typing import Iterator
from langchain_community.document_loaders.parsers.pdf import PyMuPDFParser
from langchain_community.document_loaders.parsers.msword import MsWordParser
from langchain_community.document_loaders.parsers.txt import TextParser
from langchain_core.document_loaders import Blob
from langchain_core.documents import Document


def parse_file_bytes(file_bytes: bytes, filename: str) -> Iterator[Document]:
    """Parse a file into a document line by line."""

    if filename.endswith(".pdf"):
        blob = Blob.from_data(
            data=file_bytes, metadata={"source": filename}, mime_type="application/pdf"
        )
        parse = PyMuPDFParser()
        for document in parse.lazy_parse(blob):
            yield document
    if filename.endswith((".docx", ".doc")):
        # Requires LibreOffice to be installed
        blob = Blob.from_data(
            data=file_bytes,
            metadata={"source": filename},
            mime_type="application/msword",
        )
        parse = MsWordParser()
        for document in parse.lazy_parse(blob):
            yield document
    if filename.endswith(("txt", "md")):
        blob = Blob.from_data(data=file_bytes, metadata={"source": filename})
        print("here")
        parse = TextParser()
        for document in parse.lazy_parse(blob):
            yield document
