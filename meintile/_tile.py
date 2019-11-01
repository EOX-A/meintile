from affine import Affine
from shapely.geometry import box

from meintile.exceptions import InvalidTileIndex, InvalidTileMatrixIndex
from meintile._global import PRECISION
from meintile._types import Bounds, Shape, TileIndex


class Tile(object):
    """
    A Tile is a square somewhere on Earth.

    Each Tile can be identified with the zoom, row, column index in a
    TilePyramid.

    Some tile functions can accept a tile buffer in pixels (pixelbuffer). A
    pixelbuffer value of e.g. 1 will extend the tile boundaries by 1 pixel.

    Attributes
    ----------
    tile_matrix, tm : meintile.TileMatrix
        Parent Tile Matrix.
    zoom : int
        Zoom level / parent Tile Matrix identifier.
    row : int
        Row within parent Tile Matrix.
    col : int
        Column within Tile Matrix.
    index, id : meintile.TileIndex
        Unique tile index.
    pixel_x_size : float
        Pixel size alongside x axis.
    pixel_y_size : float
        Pixel size alongside y axis.
    bounds : meintile.Bounds
        Bounding coordinates of tile
    bbox : shapely.geometry.Polygon
        Polygon geometry of tile.
    left : float
        Left coordinate of tile.
    bottom : float
        Bottom coordinate of tile.
    right : float
        Right coordinate of tile.
    top : float
        Top coordinate of tile.
    x_size : float
        Tile width in CRS units.
    y_size : float
        Tile height in CRS units.
    shape : meintile.Shape
        Tile shape in pixels.
    height : int
        Tile height in pixels.
    width : int
        Tile width in pixels.
    affine : affine.Affine
        Affine object to locate tile using rasterio.
    """

    def __init__(self, tile_matrix=None, row=None, col=None):
        """
        Initialize a Tile object.

        Parameters
        ----------
        tile_matrix : meintile.TileMatrix
            Parent Tile Matrix.
        row : int
            Row within parent Tile Matrix.
        col : int
            Column within Tile Matrix.
        """
        self.tile_matrix = self.tm = tile_matrix

        # assert Tile is valid
        if not isinstance(row, int):
            raise InvalidTileIndex("row must be an integer, not {}".format(row))
        if row >= self.tile_matrix.height:
            raise InvalidTileIndex(
                "Tile row ({}) exceeds matrix height ({})".format(
                    row, self.tile_matrix.height
                )
            )
        if not isinstance(col, int):
            raise InvalidTileIndex("col must be an integer, not {}".format(col))
        if col >= self.tile_matrix.width:
            raise InvalidTileIndex(
                "Tile col ({}) exceeds matrix width ({})".format(col, self.tm.width)
            )
        # get Tile index values
        self.zoom = self.tm.id
        self.row = row
        self.col = col
        self.index = self.id = TileIndex(self.zoom, self.row, self.col)

        # Tile properties in CRS units
        self.pixel_x_size = self.tm.pixel_x_size
        self.pixel_y_size = self.tm.pixel_y_size
        tm_left, tm_top = self.tm.top_left_corner
        tile_x_size = self.pixel_x_size * self.tm.tile_width
        tile_y_size = self.pixel_y_size * self.tm.tile_height
        self.top = round(tm_top + (self.row * tile_y_size), PRECISION)
        self.bottom = round(self.top - tile_x_size, PRECISION)
        self.left = round(tm_left + (self.col * tile_x_size), PRECISION)
        self.right = round(self.left + tile_x_size, PRECISION)
        self.bounds = Bounds(self.left, self.bottom, self.right, self.top)
        self.bbox = box(*self.bounds)
        self.x_size = self.right - self.left
        self.y_size = self.top - self.bottom

        # Tile properties in pixel units
        self.height = self.tm.tile_height
        self.width = self.tm.tile_width
        self.shape = Shape(height=self.height, width=self.width)

        # Affine object for rasterio
        self.affine = Affine(
            self.pixel_x_size, 0, self.left, 0, self.pixel_y_size, self.top
        )

    def get_parent(self):
        """
        Return tile from previous zoom level.

        Returns
        -------
        parent : meintile.Tile or None
            If no parent is available, None is returned.
        """
        try:
            return self.tm.tp.tile(self.zoom - 1, self.row // 2, self.col // 2)
        except InvalidTileMatrixIndex:
            return None

    def get_children(self):
        """
        Return tiles from next zoom level.

        Returns
        -------
        children : list of meintile.Tile
        """
        next_zoom = self.zoom + 1
        return [
            self.tm.tp.tile(
                next_zoom, self.row * 2 + row_offset, self.col * 2 + col_offset
            )
            for row_offset, col_offset in [
                (0, 0),  # top left
                (0, 1),  # top right
                (1, 1),  # bottom right
                (1, 0),  # bottom left
            ]
            if all(
                [
                    self.row * 2 + row_offset < self.tm.tp.matrix_height(next_zoom),
                    self.col * 2 + col_offset < self.tm.tp.matrix_width(next_zoom),
                ]
            )
        ]

    def get_neighbors(self, connectedness=8):
        """
        Return tile neighbors.

        Tile neighbors are unique, i.e. in some edge cases, where both the left
        and right neighbor wrapped around the antimeridian is the same. Also,
        neighbors ouside the northern and southern TilePyramid boundaries are
        excluded, because they are invalid.

        -------------
        | 8 | 1 | 5 |
        -------------
        | 4 | x | 2 |
        -------------
        | 7 | 3 | 6 |
        -------------

        Parameters
        ----------
        connectedness : int, (4 or 8)
            Return the four direct neighbors or all eight.

        Returns
        -------
        neighbors : list of meintile.Tile
        """
        if connectedness not in [4, 8]:
            raise ValueError("only connectedness values 8 or 4 are allowed")

        unique_neighbors = {}
        # 4-connected neighborsfor pyramid
        matrix_offsets = [
            (-1, 0),  # 1: above
            (0, 1),  # 2: right
            (1, 0),  # 3: below
            (0, -1),  # 4: left
        ]
        if connectedness == 8:
            matrix_offsets.extend(
                [
                    (-1, 1),  # 5: above right
                    (1, 1),  # 6: below right
                    (1, -1),  # 7: below left
                    (-1, -1),  # 8: above left
                ]
            )

        for row_offset, col_offset in matrix_offsets:
            new_row = self.row + row_offset
            new_col = self.col + col_offset
            # omit if row is outside of tile matrix
            if new_row < 0 or new_row >= self.tp.matrix_height(self.zoom):
                continue
            # wrap around antimeridian if new column is outside of tile matrix
            if new_col < 0:
                if not self.tp.is_global:
                    continue
                new_col = self.tp.matrix_width(self.zoom) + new_col
            elif new_col >= self.tp.matrix_width(self.zoom):
                if not self.tp.is_global:
                    continue
                new_col -= self.tp.matrix_width(self.zoom)
            # omit if new tile is current tile
            if new_row == self.row and new_col == self.col:
                continue
            # create new tile
            unique_neighbors[(new_row, new_col)] = self.tp.tile(
                self.zoom, new_row, new_col
            )

        return unique_neighbors.values()

    def __repr__(self):
        """Return representational string."""
        return "Tile(%s, %s)" % (self.id, self.tm)

    def __hash__(self):
        """Return unique hash."""
        return hash(repr(self))

    def __iter__(self):
        """
        Enable unpacking of tile index values.

        Examples:
        ---------
        zoom, row, col = tile
        """
        yield self.zoom
        yield self.row
        yield self.col
