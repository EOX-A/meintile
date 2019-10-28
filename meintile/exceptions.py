class InvalidTileMatrixIndex(KeyError):
    """Raise when Tile Matrix is not available in TileMatrixSet."""


class InvalidTileIndex(KeyError):
    """Raise when Tile is not available in TileMatrix."""


class InvalidCRS(ValueError):
    """Raise when no or invalid CRS is given."""
