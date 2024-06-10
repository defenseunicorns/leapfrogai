"""Load a file and split it into chunks."""

# This import is required for "magic" to work, see https://github.com/ahupp/python-magic/issues/233
# may not be needed after https://github.com/ahupp/python-magic/pull/294 is merged
import pylibmagic  # noqa: F401 # pylint: disable=unused-import
import magic
from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

HANDLERS = {
    "application/pdf": PyPDFLoader,
    "text/plain": TextLoader,
    "text/html": UnstructuredHTMLLoader,
    "text/csv": CSVLoader,
    "text/markdown": UnstructuredMarkdownLoader,
    "application/msword": Docx2txtLoader,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": Docx2txtLoader,
}


def is_supported_mime_type(mime_type: str) -> bool:
    """Validate the mime type of a file."""
    return mime_type in HANDLERS


async def load_file(file_path: str) -> list[Document]:
    """Load a file and return a list of documents."""

    mime_type = magic.from_file(file_path, mime=True)

    loader = HANDLERS.get(mime_type)

    if loader:
        return await loader(file_path).aload()
    raise ValueError(f"Unsupported file type: {mime_type}")


async def split(docs: list[Document]) -> list[Document]:
    """Split a document into chunks."""
    separators = [
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Full width comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Full width full stop
        "\u3002",  # Ideographic full stop
        "",
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        # TODO: This parameters might need to be tuned and/or exposed for configuration
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
        separators=separators,
    )

    return await text_splitter.atransform_documents(docs)
