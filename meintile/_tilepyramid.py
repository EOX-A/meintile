"""TilePyramid class."""

from collections import OrderedDict
from rasterio.crs import CRS

from meintile.exceptions import InvalidTileMatrixIndex
from meintile._tilematrix import TileMatrix
from meintile._types import Bounds
from meintile.wkss import get_wkss


class TileMatrixSet:
    """
    A Tile Matrix Set contains TileMatrix objects.

    Attributes
    ----------
    crs : rasterio.crs.CRS
        Coordinate reference system used by TileMatrixSet.
    tile_matrices : OrderedDict
        Keys are TileMatrix identifiers, values are TileMatrix objects.
    well_known_scale_set : str
        Reference to the well-known scale set used as base.
    bounds : meintile.Bounds or None
        Bounding box values if bounding_box parameter was provided.
    """

    def __init__(
        self,
        crs=None,
        tile_matrix_params=None,
        well_known_scale_set=None,
        title=None,
        identifier=None,
        bounding_box=None,
        **kwargs
    ):
        """
        Initialize a Tile Matrix Set.

        Parameters
        ----------
        crs : str or rasterio.crs.CRS
            CRS object or reference to one coordinate reference system. (e.g. an OGC URI)
        tile_matrix_params : list of dicts
            Describes a scale level and its tile matrix. See parameters required by
            meintile.TileMatrix.
        well_known_scale_set : str, optional
            Reference to a well-known scale set.
        title : str, optional
            Title of this tile matrix set, normally used for display to a human.
        identifier : str, optional
            Tile matrix set identifier.
        bounding_box : dict, optional
            Minimum bounding rectangle surrounding the tile matrix set, in the supported
            CRS. The dictionary requires the following entries: 'type' (must be
            'BoundingBoxType'), 'crs' (reference to one coordinate reference system),
            'lower_corner' (lower left corner coordinates) and 'upper_corner' (upper
            right corner coordinates).
        """
        self.well_known_scale_set = well_known_scale_set
        self._title = title
        self._identifier = identifier
        self._bounding_box = bounding_box
        self._tile_matrix_params = tile_matrix_params

        if self._bounding_box:
            left, bottom = self._bounding_box["lower_corner"]
            right, top = self._bounding_box["upper_corner"]
            self.bounds = Bounds(left, bottom, right, top)
        else:
            self.bounds = None
        self.crs = CRS.from_user_input(crs)
        self.tile_matrices = OrderedDict(
            [
                (
                    int(i["identifier"]),
                    TileMatrix(
                        **dict(
                            i,
                            identifier=int(i["identifier"]),
                            crs=self.crs,
                            bounds=self.bounds,
                            tile_pyramid=self,
                        )
                    ),
                )
                for i in tile_matrix_params
            ]
        )
        self.is_global = True

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
        return self[zoom].width

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
        return self[zoom].height

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

    def __iter__(self):
        """Return iterator over containing Tile Matrix objects."""
        return iter(self.values())

    def __len__(self):
        """Return number of containing TileMatrix objects."""
        return len(self.tile_matrices)


class TilePyramid(TileMatrixSet):
    """
    A Tile Pyramid is a subset of a Tile Matrix Set.

    Tile Matrix Sets consist of Tile Matrices with arbitrary properties. In a Tile Pyramid
    the Tile Matrices are ordered, and their shape and pixel sizes increase by a factor
    of 2. Tile Pyramids resemble the image pyramid structure used by many image formats.

    Attributes
    ----------
    crs : rasterio.crs.CRS
        Coordinate reference system used by TileMatrixSet.
    tile_matrices : OrderedDict
        Keys are TileMatrix identifiers, values are TileMatrix objects.
    well_known_scale_set : str
        Reference to the well-known scale set used as base.
    bounds : meintile.Bounds or None
        Bounding box values if bounding_box parameter was provided.

    """

    def __init__(self, **kwargs):
        """
        Initialize a Tile Pyramid.

        Parameters
        ----------
        crs : str or rasterio.crs.CRS
            CRS object or reference to one coordinate reference system. (e.g. an OGC URI)
        tile_matrix_params : list of dicts
            Describes a scale level and its tile matrix. See parameters required by
            meintile.TileMatrix.
        well_known_scale_set : str, optional
            Reference to a well-known scale set.
        title : str, optional
            Title of this tile matrix set, normally used for display to a human.
        identifier : str, optional
            Tile matrix set identifier.
        bounding_box : dict, optional
            Minimum bounding rectangle surrounding the tile matrix set, in the supported
            CRS.
            Dictionary keys:
            type : str
                Must be "BoundingBoxType".
            crs : str
                Reference to one coordinate reference system.
            lower_corner : tuple or list
                Lower left corner coordinates.
            upper_corner : tuple or list
                Upper right corner coordinates.
        """
        super().__init__(**kwargs)
        # TODO: check whether parameters meet tile pyramid restrictions

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
    # get definition by ID or use dictionary representation
    if isinstance(wkss, str):
        wkss_definition = get_wkss(wkss)
    elif isinstance(wkss, dict):
        wkss_definition = wkss
    else:
        raise TypeError("invalid WKSS given")

    # map to pythonic names
    return dict(
        type=wkss_definition["type"],
        title=wkss_definition.get("title"),
        identifier=wkss_definition.get("identifier"),
        bounding_box=dict(
            type=wkss_definition["boundingBox"]["type"],
            crs=wkss_definition["boundingBox"]["crs"],
            lower_corner=wkss_definition["boundingBox"]["lowerCorner"],
            upper_corner=wkss_definition["boundingBox"]["upperCorner"],
        )
        if "boundingBox" in wkss_definition
        else None,
        crs=wkss_definition["supportedCRS"],
        well_known_scale_set=wkss_definition.get("wellKnownScaleSet"),
        tile_matrix_params=[
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
