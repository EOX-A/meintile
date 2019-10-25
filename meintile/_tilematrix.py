class TileMatrix:
    """A Tile Matrix object close to the OGC specification."""

    def __init__(
        self,
        identifier=None,
        scale_denominator=None,
        top_left_corner=None,
        tile_width=None,
        tile_height=None,
        matrix_width=None,
        matrix_height=None,
    ):
        self.identifier = identifier
        self.scale_denominator = scale_denominator
        self.top_left_corner = top_left_corner
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height

    def from_wkss(wkss):
        mapping = dict(
            identifier=wkss["identifier"],
            scale_denominator=wkss["scaleDenominator"],
            top_left_corner=wkss["topLeftCorner"],
            tile_width=wkss["tileWidth"],
            tile_height=wkss["tileHeight"],
            matrix_width=wkss["matrixWidth"],
            matrix_height=wkss["matrixHeight"],
        )
        return TileMatrix(**mapping)
