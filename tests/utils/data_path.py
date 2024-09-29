import os
from pathlib import Path

TXT_FILE = "test.txt"
TXT_DATA_FILE = "test_with_data.txt"
PPTX_FILE = "test.pptx"
WAV_FILE = "0min12sec.wav"
WAV_FILE_ARABIC = "arabic-audio.wav"
MP3_FILE_RUSSIAN = "russian.mp3"
XLSX_FILE = "test.xlsx"


def data_path(filename: str):
    """Return the path to a test file in the data directory. (See constants for specific files.)

    Args:
        filename (str): The name of the file to return the path.

    Returns:
        Path: The path to the file in the data directory.

    Raises:
        FileNotFoundError: If the file does not exist in the data directory.
    """

    data_path = Path(
        os.path.realpath(os.path.dirname(__file__) + f"/../data/{filename}")
    )

    try:
        # Check if the file exists
        with open(data_path, "r"):
            return data_path
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found in data directory: {data_path}")
