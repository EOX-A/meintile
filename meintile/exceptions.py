class InvalidTileIndex(KeyError):
    """Raise when tile index is not available in Tile Matrix."""


class InvalidCRS(ValueError):
    """Raise when no or invalid CRS is given."""
