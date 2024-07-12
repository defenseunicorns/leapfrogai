"""API key pydantic model."""

import secrets
import hashlib
from pydantic import BaseModel, field_validator, ValidationInfo

KEY_PREFIX = "lfai"
KEY_BYTES = 32
CHECKSUM_LENGTH = 8


class APIKey(BaseModel):
    """API key model."""

    prefix: str
    unique_key: str
    checksum: str

    @classmethod
    def generate(cls) -> "APIKey":
        """Generate a new API key."""
        unique_key: str = secrets.token_bytes(KEY_BYTES).hex()
        checksum: str = cls._calculate_checksum(unique_key)
        return cls(prefix=KEY_PREFIX, unique_key=unique_key, checksum=checksum)

    @classmethod
    def parse(cls, key_string: str) -> "APIKey":
        """Parse a string representation of an API key."""
        parts: list[str] = key_string.split("_")
        if len(parts) != 3:
            raise ValueError("Invalid API key format")
        return cls(prefix=parts[0], unique_key=parts[1], checksum=parts[2])

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, prefix: str) -> str:
        """Validate the key prefix."""
        if prefix != KEY_PREFIX:
            raise ValueError(f"Invalid prefix. Expected {KEY_PREFIX}")
        return prefix

    @field_validator("unique_key")
    @classmethod
    def validate_unique_key(cls, unique_key: str) -> str:
        """Validate the unique key."""
        if len(unique_key) != KEY_BYTES * 2:  # hex representation is twice as long
            raise ValueError(
                f"Invalid unique key length. Expected {KEY_BYTES * 2} characters"
            )
        return unique_key

    @field_validator("checksum")
    @classmethod
    def validate_checksum(cls, checksum: str, info: ValidationInfo) -> str:
        """Validate the checksum."""
        if "unique_key" in info.data:
            expected_checksum: str = cls._calculate_checksum(info.data["unique_key"])
            if checksum != expected_checksum:
                raise ValueError("Invalid checksum")
        return checksum

    def __str__(self) -> str:
        return f"{self.prefix}_{self.unique_key}_{self.checksum}"

    def __repr__(self) -> str:
        return f"APIKey(prefix='{self.prefix}', unique_key='{self.unique_key}', checksum='{self.checksum}')"

    @staticmethod
    def _calculate_checksum(unique_key: str) -> str:
        """Calculate a checksum for a unique key."""
        return hashlib.sha256(unique_key.encode()).hexdigest()[:CHECKSUM_LENGTH]
