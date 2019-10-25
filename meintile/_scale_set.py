from rasterio.crs import CRS

from meintile.exceptions import InvalidCRS


URL_TO_CRS = {
    "http://www.opengis.net/def/crs/EPSG/0/3035": CRS.from_epsg(3035),
    "http://www.opengis.net/def/crs/OGC/1.3/CRS84": CRS.from_epsg(4626),
    "http://www.opengis.net/def/crs/EPSG/0/3857": CRS.from_epsg(3857),
    "http://www.opengis.net/def/crs/EPSG/0/3395": CRS.from_epsg(3395),
}


def _crs_from_url(url):
    try:
        return URL_TO_CRS[url]
    except KeyError:
        raise InvalidCRS("Could not determine CRS from URL %s" % url)


class ScaleSetDefinition:
    """Container for scale set definitions."""

    def __init__(self, in_dict, crs=None):
        """Keep Scale Set definition dictionary and add CRS as WKT."""
        self.dict = in_dict
        self.crs = crs or _crs_from_url(in_dict["supportedCRS"])

    def __repr__(self):
        """Representational string."""
        return "ScaleSetDefinition('%s')" % self.dict["identifier"]
