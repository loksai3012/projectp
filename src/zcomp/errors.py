class ZCompError(Exception):
    """Base package error."""


class ArchiveError(ZCompError):
    """Raised for invalid or unsupported archives."""


class ValidationError(ZCompError):
    """Raised for invalid user file selection."""


class CodecError(ZCompError):
    """Raised when a codec cannot process data."""
