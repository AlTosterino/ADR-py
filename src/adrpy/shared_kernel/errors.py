class AdrPyError(Exception):
    """Base exception for expected ADR-py errors."""


class ConfigurationError(AdrPyError):
    """Raised when ADR-py configuration is missing or invalid."""


class MetadataValidationError(AdrPyError):
    """Raised when an ADR document has invalid or incomplete metadata."""
