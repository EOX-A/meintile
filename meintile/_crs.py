from rasterio.crs import CRS


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
    else:
        return CRS.from_user_input(crs)
