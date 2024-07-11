"""Basic API key security functions."""

import secrets
import hashlib
from pydantic import BaseModel

KEY_PREFIX = "lfai"
KEY_BYTES = 32
CHECKSUM_LENGTH = 8

### KEEP ###


class APIKey(BaseModel):
    """API key model."""

    prefix: str
    unique_key: str
    checksum: str


def generate_new_api_key() -> str:
    """Generate a new API key.

    key format: {prefix}_{unique_key}_{checksum}

    returns:
        api_key: str
    """
    unique_key = _generate_unique_key()
    checksum = _calculate_checksum(unique_key)
    return f"{KEY_PREFIX}_{unique_key}_{checksum}"


def validate_api_key(api_key: str) -> bool:
    """Validate an API key.

    returns:
        bool: True if the key is valid, False otherwise
    """
    try:
        parsed_key = parse_api_key(api_key)
        prefix = parsed_key.prefix
        key = parsed_key.unique_key
        checksum = parsed_key.checksum
    except ValueError:
        return False
    if not prefix or not key or not checksum:
        return False
    if prefix != KEY_PREFIX:
        return False
    if not secrets.compare_digest(checksum, _calculate_checksum(key)):
        return False

    return True


def _generate_unique_key() -> str:
    """Generate a unique key.

    returns:
        unique_key: str
    """
    return secrets.token_bytes(KEY_BYTES).hex()


def _calculate_checksum(unique_key: str) -> str:
    """Calculate a checksum for a unique key.

    returns:
        checksum: str
    """
    return hashlib.sha256(unique_key.encode()).hexdigest()[:CHECKSUM_LENGTH]


def parse_api_key(api_key: str) -> APIKey:
    """Parse an API key into its components.

    key format: {prefix}_{unique_key}_{checksum}

    Note: Does not validate prefix, checksum, or key.

    returns:
        prefix: str
        key: str
        checksum: str
    """

    prefix, key, checksum = (
        api_key.split("_")[0],
        "_".join(api_key.split("_")[1:-1]),
        api_key.split("_")[-1],
    )

    if not prefix or not key or not checksum:
        raise ValueError("Invalid API key format")

    return APIKey(prefix=prefix, unique_key=key, checksum=checksum)
