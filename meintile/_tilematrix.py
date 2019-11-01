import math
from rasterio.crs import CRS

from meintile._global import PRECISION, SCALE_MULTIPLIER
from meintile._tile import Tile
from meintile._types import Bounds


class TileMatrix:
    """
    A TileMatrix object contains Tiles organized in rows and columns.

    Attributes
    ----------
    identifier : int
        Tile matrix identifier.
    crs : str or rasterio.crs.CRS
        CRS object or reference to one coordinate reference system. (e.g. an OGC URI)
    scale_denominator : float
        Scale denominator level of this tile matrix.
        The pixel size of the tile can be obtained from the scaleDenominator by
        multiplying the later by 0.28 10^-3 / metersPerUnit. If the CRS uses meters as
        units of measure for the horizontal dimensions, then metersPerUnit=1; if it
        has degrees, then metersPerUnit=2pa/360 (a is the Earth maximum radius of the
        ellipsoid).
    top_left_corner : tuple or list
        Position in CRS coordinates of the top-left corner of this tile matrix.
    tile_width : int
        Width of each tile of this tile matrix in pixels.
    tile_height : int
        Height of each tile of this tile matrix in pixels.
    width : int
        Width of the matrix (number of tiles in width).
    height : int
        Height of the matrix (number of tiles in height).
    pixel_x_size : float
        Pixel size alongside x axis.
    pixel_y_size : float
        Pixel size alongside y axis.
    matrix_bounds : meintile.Bounds
        Bounding coordinates calculated between given top left corner, matrix shape and
        tile size. Can extend over CRS bounds.
    left : float
        Left coordinate of matrix bounds.
    bottom : float
        Bottom coordinate of matrix bounds.
    right : float
        Right coordinate of matrix bounds.
    top : float
        Top coordinate of matrix bounds.
    bounds : meintile.Bounds
        Minimum bounding rectangle surrounding the tile matrix set, provided while
        initializing.
    """

    def __init__(
        self,
        identifier=None,
        crs=None,
        scale_denominator=None,
        top_left_corner=None,
        tile_width=None,
        tile_height=None,
        matrix_width=None,
        matrix_height=None,
        bounds=None,
        tile_pyramid=None,
    ):
        """
        Initialize a TileMatrix object.

        Parameters
        ----------
        identifier : int
            Tile matrix identifier.
        crs : str or rasterio.crs.CRS
            CRS object or reference to one coordinate reference system. (e.g. an OGC URI)
        scale_denominator : float
            Scale denominator level of this tile matrix.
            The pixel size of the tile can be obtained from the scaleDenominator by
            multiplying the later by 0.28 10^-3 / metersPerUnit. If the CRS uses meters as
            units of measure for the horizontal dimensions, then metersPerUnit=1; if it
            has degrees, then metersPerUnit=2pa/360 (a is the Earth maximum radius of the
            ellipsoid).
        top_left_corner : tuple or list
            Position in CRS coordinates of the top-left corner of this tile matrix.
        tile_width : int
            Width of each tile of this tile matrix in pixels.
        tile_height : int
            Height of each tile of this tile matrix in pixels.
        matrix_width : int
            Width of the matrix (number of tiles in width).
        matrix_height : int
            Height of the matrix (number of tiles in height).
        bounds : tuple, optional
            Minimum bounding rectangle surrounding the tile matrix set, in the supported
            CRS.
        tile_pyramid : meintile.TilePyramid, optional
            Parent Tile Pyramid. This is required when using certain tile functions such
            as get_parent() or get_children()
        """
        self.identifier = self.id = identifier
        self.crs = CRS.from_user_input(crs)
        self.scale_denominator = scale_denominator
        self.top_left_corner = top_left_corner
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.matrix_width = self.width = matrix_width
        self.matrix_height = self.height = matrix_height

        # convert scale_denominator to pixel size
        if "EPSG:4326" in self.crs.to_string():
            # TODO: find a better way to handle non-metric CRSes
            meters_per_unit = 2 * math.pi * 6378137 / 360.0
        else:
            meters_per_unit = self.crs.linear_units_factor[1]
        self.pixel_x_size = round(
            self.scale_denominator * 10 ** -3 * SCALE_MULTIPLIER / meters_per_unit,
            PRECISION,
        )
        self.pixel_y_size = -self.pixel_x_size

        # calculate matrix bounds
        top, left = self.top_left_corner
        tile_x_size = self.pixel_x_size * self.tile_width
        tile_y_size = self.pixel_y_size * self.tile_height
        self.matrix_bounds = Bounds(
            left=round(left, PRECISION),
            bottom=round(top + tile_y_size * self.height, PRECISION),
            right=round(left + tile_x_size * self.width, PRECISION),
            top=round(top, PRECISION),
        )
        self.left, self.bottom, self.right, self.top = self.matrix_bounds
        self.bounds = Bounds(*bounds) if bounds else self.matrix_bounds
        self.tile_pyramid = self.tp = tile_pyramid

    def tile(self, row=None, col=None):
        """
        Return Tile object of this TileMatrix.

        Parameters
        ----------
        row : int
            TileMatrix row
        col : int
            TileMatrix column

        Returns
        -------
        tile : meintile.Tile
        """
        return Tile(tile_matrix=self, row=row, col=col)

    def __repr__(self):
        """Return representational string."""
        return "TileMatrix(id={}, crs={})".format(self.id, self.crs.to_string())
