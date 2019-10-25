from meintile._crs import get_crs


class ScaleSetDefinition:
    """
    Container for scale set definition dictionary.

    Attributes
    ==========
    dict : dict
        Dictionary representation of configuration JSON.
    crs : rasterio.crs.CRS
        CRS object.
    """

    def __init__(self, in_dict, crs=None):
        """Keep Scale Set definition dictionary and add CRS as WKT."""
        if not isinstance(in_dict, dict):
            raise TypeError(
                "in_dict needs to be a dictionary representation of a scale set"
            )
        self.dict = in_dict
        self.crs = get_crs(crs) if crs else get_crs(in_dict["supportedCRS"])

    def __repr__(self):
        """Representational string."""
        return "ScaleSetDefinition('%s')" % self.dict["identifier"]
