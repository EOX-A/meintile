from meintile.exceptions import InvalidTileIndex


class Tile(object):
    """
    A Tile is a square somewhere on Earth.

    Each Tile can be identified with the zoom, row, column index in a
    TilePyramid.

    Some tile functions can accept a tile buffer in pixels (pixelbuffer). A
    pixelbuffer value of e.g. 1 will extend the tile boundaries by 1 pixel.
    """

    def __init__(self, tile_matrix=None, row=None, col=None):
        self.tile_matrix, self.tm = tile_matrix, tile_matrix
        self.tile_pyramid, self.tp = self.tm.tp, self.tm.tp
        self.zoom = self.tm.id
        # assert Tile is valid
        if not isinstance(row, int):
            raise InvalidTileIndex("row must be an integer, not {}".format(row))
        if row >= self.tile_matrix.width:
            raise InvalidTileIndex(
                "Tile row ({}) exceeds matrix width ({})".format(
                    row, self.tile_matrix.width
                )
            )
        if not isinstance(col, int):
            raise InvalidTileIndex("col must be an integer, not {}".format(col))
        if col >= self.tile_matrix.height:
            raise InvalidTileIndex(
                "Tile col ({}) exceeds matrix height ({})".format(
                    col, self.tile_matrix.height
                )
            )
        self.row = row
        self.col = col
