"""Basic API key security functions."""

import secrets
import hashlib

KEY_PREFIX = "lfai"


def generate_api_key() -> tuple[str, str]:
    """Generate an API key.

    returns:
        read_once_token: str
        hashed_token: str
    """
    unique_key = secrets.token_bytes(32).hex()
    hashed_token = encode_unique_key(unique_key)
    checksum = parse_api_key(hashed_token)[2]

    read_once_token = f"{KEY_PREFIX}_{unique_key}_{checksum}"
    hashed_token = encode_unique_key(unique_key)

    return read_once_token, hashed_token


def encode_unique_key(unique_key: str):
    """Hashes and encodes an API key as a string.

    returns:
        api_key: str # in the format {prefix}_{one_way_hash}_{checksum}
    """
    one_way_hash = hashlib.sha256(unique_key.encode()).hexdigest()
    checksum = hashlib.sha256(unique_key.encode()).hexdigest()[:4]
    return f"{KEY_PREFIX}_{one_way_hash}_{checksum}"


def validate_checksum(unique_key: str, checksum: str):
    """Validate the checksum of an API key."""
    return hashlib.sha256(unique_key.encode()).hexdigest()[:4] == checksum


def validate_api_key(api_key: str) -> bool:
    """Validate an API key.

    returns:
        bool: True if the key is valid, False otherwise
    """
    try:
        _prefix, key, checksum = parse_api_key(api_key)
    except ValueError:
        return False

    return validate_checksum(key, checksum)


def parse_api_key(api_key: str) -> tuple[str, str, str]:
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

    return prefix, key, checksum
