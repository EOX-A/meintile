import math

from meintile._global import PRECISION, SCALE_MULTIPLIER
from meintile._tile import Tile
from meintile._types import Bounds


class TileMatrix:
    """A Tile Matrix object close to the OGC specification."""

    def __init__(
        self,
        identifier=None,
        crs=None,
        bounds=None,
        scale_denominator=None,
        top_left_corner=None,
        tile_width=None,
        tile_height=None,
        matrix_width=None,
        matrix_height=None,
    ):
        self.identifier = self.id = identifier
        self.crs = crs
        self.scale_denominator = scale_denominator
        self.top_left_corner = top_left_corner
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.matrix_width, self.width = matrix_width, matrix_width
        self.matrix_height, self.height = matrix_height, matrix_height

        # http://docs.opengeospatial.org/is/17-083r2/17-083r2.html
        # The pixel size of the tile can be obtained from the scaleDenominator by
        # multiplying the later by 0.28 10^-3 / metersPerUnit. If the CRS uses meters as
        # units of measure for the horizontal dimensions, then metersPerUnit=1; if it has
        # degrees, then metersPerUnit=2pa/360 (a is the Earth maximum radius of the
        # ellipsoid).
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
            bottom=round(top + tile_y_size * self.matrix_height, PRECISION),
            right=round(left + tile_x_size * self.matrix_width, PRECISION),
            top=round(top, PRECISION),
        )
        self.left, self.bottom, self.right, self.top = self.matrix_bounds
        self.bounds = Bounds(*bounds) if bounds else self.matrix_bounds

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
