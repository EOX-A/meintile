"""TilePyramid class."""

from collections import OrderedDict

from meintile._crs import get_crs
from meintile.exceptions import InvalidTileMatrixIndex
from meintile._tilematrix import TileMatrix
from meintile._types import Bounds
from meintile.wkss import get_wkss


class TileMatrixSet:
    """
    A Tile Matrix Set close to the OGC specification.

    Parameters
    ----------


    Attributes
    ----------
    bounding_box : meintile.Bounds
        Minimum bounding rectangle surrounding the tile matrix set, in the supported CRS.
    bounds : meintile.Bounds
        Alias of self.bounding_box.
    supported_crs : rasterio.crs.CRS
        Reference to one coordinate reference system (CRS).
    crs : rasterio.crs.CRS
        Alias of self.supported_crs.
    wkss : dict
        Reference to a well-known scale set.
    tile_matrices : list
        List of parameters of multiple Tile Matrices.
    """

    def __init__(self, crs=None, bounds=None, tile_matrices=None, **kwargs):
        """Initialize a Tile Matrix Set."""
        self.bounds = Bounds(*bounds)
        self.bounding_box = self.bounds
        self.crs = get_crs(crs)
        self.supported_crs = self.crs
        self._wkss = kwargs.get("init_wkss")
        self.tile_matrices = OrderedDict(
            [
                (int(i["identifier"]), TileMatrix(**i, crs=self.crs))
                for i in tile_matrices
            ]
        )

    @classmethod
    def from_wkss(self, wkss):
        """
        Construct a Tile Matrix Set using a predefined well-known scale set.

        Parameters
        ----------
        wkss : str or dict
            Either a WKSS identifier or a WKSS dictionary.
            Currently available scale sets:
                - EuropeanETRS89_LAEAQuad: Lambert Azimuthal Equal Area ETRS89 for Europe
                - WebMercatorQuad: Google Maps Compatible for the World
                - WorldCRS84Quad: CRS84 for the World
                - WorldMercatorWGS84Quad: World Mercator WGS84 (ellipsoid)

        Returns
        -------
        TileMatrixSet
        """
        return TileMatrixSet(**_get_wkss_mapping(wkss))

    def items(self):
        """Return a list of tuples with TileMatrix IDs and TileMatrix objects."""
        return self.tile_matrices.items()

    def keys(self):
        """Return TileMatrix identifiers."""
        return self.tile_matrices.keys()

    def values(self):
        """Return TileMatrix objects."""
        return self.tile_matrices.values()

    def __getitem__(self, key):
        """Get containing TileMatrix by identifier."""
        try:
            return self.tile_matrices[key]
        except KeyError:
            raise InvalidTileMatrixIndex("TileMatrix '{}' not found".format(key))

    def __len__(self):
        """Return number of containing TileMatrix objects."""
        return len(self.tile_matrices)


class TilePyramid(TileMatrixSet):
    """
    A Tile Pyramid is a subset of a Tile Matrix Set.

    Tile Matrix Sets consist of Tile Matrices with arbitrary properties. In a Tile Pyramid
    the Tile Matrices are ordered, and their shape and pixel sizes increase by a factor
    of 2. Tile Pyramids resemble the image pyramid structure used by many image formats.

    Parameters
    ----------

    Attributes
    ----------
    """

    def __init__(self, crs=None, bounds=None, tile_matrices=[], **kwargs):
        """Initialize a Tile Pyramid."""
        all_kwargs = dict(crs=crs, bounds=bounds, tile_matrices=tile_matrices)
        all_kwargs.update(**kwargs)
        super().__init__(**all_kwargs)
        # TODO: check whether parameters meet tile pyramid restrictions

    def tile(self, zoom=None, row=None, col=None):
        """
        Return Tile object of this TilePyramid.

        Parameters
        ----------
        zoom : int
            zoom level / TileMatrix identifier
        row : int
            TileMatrix row
        col : int
            TileMatrix column

        Returns
        -------
        tile : meintile.Tile
        """
        return self[zoom].tile(row=row, col=col)

    def matrix_width(self, zoom=None):
        """
        Return TileMatrix height (number of rows) at zoom level.

        Parameters
        ----------
        zoom : int
            zoom level / TileMatrix identifier

        Returns
        -------
        matrix width : int
        """
        return self[zoom].matrix_width

    def matrix_height(self, zoom=None):
        """
        Return TileMatrix height (number of rows) at zoom level.

        Parameters
        ----------
        zoom : int
            zoom level / TileMatrix identifier

        Returns
        -------
        matrix height : int
        """
        return self[zoom].matrix_height

    def pixel_x_size(self, zoom):
        """
        Return pixel size at the x-axis at zoom level in CRS units.

        Parameters
        ----------
        zoom : int
            zoom level / TileMatrix identifier

        Returns
        -------
        pixel_x_size : float
        """
        return self[zoom].pixel_x_size

    def pixel_y_size(self, zoom):
        """
        Return pixel size at the y-axis at zoom level in CRS units.

        Parameters
        ----------
        zoom : int
            zoom level / TileMatrix identifier

        Returns
        -------
        pixel_y_size : float
        """
        return self[zoom].pixel_y_size

    @classmethod
    def from_wkss(self, wkss):
        """
        Construct a Tile Pyramid using a predefined well-known scale set.

        Parameters
        ----------
        wkss : str or dict
            Either a WKSS identifier or a WKSS dictionary.
            Currently available scale sets:
                - EuropeanETRS89_LAEAQuad: Lambert Azimuthal Equal Area ETRS89 for Europe
                - WebMercatorQuad: Google Maps Compatible for the World
                - WorldCRS84Quad: CRS84 for the World
                - WorldMercatorWGS84Quad: World Mercator WGS84 (ellipsoid)

        Returns
        -------
        TilePyramid
        """
        return TilePyramid(**_get_wkss_mapping(wkss))


def _get_wkss_mapping(wkss):
    if isinstance(wkss, str):
        wkss_definition = get_wkss(wkss)
    elif isinstance(wkss, dict):
        wkss_definition = wkss
    else:
        raise TypeError("invalid WKSS given")
    left, bottom = wkss_definition["boundingBox"]["lowerCorner"]
    right, top = wkss_definition["boundingBox"]["upperCorner"]
    return dict(
        crs=get_crs(wkss_definition["supportedCRS"]),
        bounds=(left, bottom, right, top),
        init_wkss=wkss_definition,
        tile_matrices=[
            dict(
                identifier=i["identifier"],
                scale_denominator=i["scaleDenominator"],
                top_left_corner=i["topLeftCorner"],
                tile_width=i["tileWidth"],
                tile_height=i["tileHeight"],
                matrix_width=i["matrixWidth"],
                matrix_height=i["matrixHeight"],
            )
            for i in wkss_definition["tileMatrix"]
        ],
    )
