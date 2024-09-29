import os
from pathlib import Path

TXT_FILE_NAME = "test_with_data.txt"
PPTX_FILE_NAME = "test.pptx"
WAV_FILE = "0min12sec.wav"
WAV_FILE_ARABIC = "arabic-audio.wav"
XLSX_FILE_NAME = "test.xlsx"


def data_path(filename: str | None = None):
    """Return the path to the data directory or a specific file within it.

    Args:
        filename (str): The name of the file to return the path to (see constants). Defaults to None.

    Returns:
        Path: The path to the data directory or a specific file within it.

    Raises:
        FileNotFoundError: If the file does not exist in the data directory.
    """

    data_path = Path(os.path.dirname(__file__) + f"/../data/{filename}")

    try:
        # Check if the file exists
        with open(data_path, "r"):
            return data_path
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found in data directory: {data_path}")
