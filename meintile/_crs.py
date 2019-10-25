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


def get_crs(crs):
    """
    Get CRS from various input types.

    Parameters
    ----------
    crs : rasterio.crs.CRS or OGC URL

    Returns
    -------
    crs : rasterio.crs.CRS
        A valid rasterio CRS object
    """
    if isinstance(crs, CRS):
        return crs
    elif isinstance(crs, str) and crs.startswith("http"):
        return _crs_from_url(crs)
    else:
        raise InvalidCRS(
            "crs in not a valid rasterio.crs.CRS object or OGC URL: %s" % crs
        )
