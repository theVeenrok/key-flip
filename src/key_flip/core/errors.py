class KeyFlipError(Exception):
    """Base class for all KeyFlip errors."""


class LayoutNotFoundError(KeyFlipError):
    """Raised when a layout is not found."""


class LayoutPairNotFoundError(KeyFlipError):
    """Raised when a layout pair is not found."""


class InvalidConvertOptionsError(KeyFlipError):
    """Raised when invalid convert options are provided."""


class InvalidMappingError(KeyFlipError):
    """Raised when invalid mapping is provided."""
