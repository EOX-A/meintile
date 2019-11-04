import json
import os

from meintile._types import ScaleSet

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def _load_json(wkss_json):
    return json.load(open(os.path.join(SCRIPT_DIR, wkss_json)))


# Lambert Azimuthal Equal Area ETRS89 for Europe
EuropeanETRS89_LAEAQuad = _load_json("EuropeanETRS89_LAEAQuad.json")

# Google Maps Compatible for the World
WebMercatorQuad = _load_json("WebMercatorQuad.json")

# CRS84 for the World
WorldCRS84Quad = _load_json("WorldCRS84Quad.json")

# World Mercator WGS84 (ellipsoid)
WorldMercatorWGS84Quad = _load_json("WorldMercatorWGS84Quad.json")


WKSS_BY_NAME = {
    "EuropeanETRS89_LAEAQuad": ScaleSet(EuropeanETRS89_LAEAQuad, False),
    "WebMercatorQuad": ScaleSet(WebMercatorQuad, True),
    "WorldCRS84Quad": ScaleSet(WorldCRS84Quad, True),
    "WorldMercatorWGS84Quad": ScaleSet(WorldMercatorWGS84Quad, True),
}


def get_wkss(wkss_identifier):
    """
    Return well-known scale set by name as ScaleSetDefinition object.

    Parameters
    ----------
    wkss_identifier : str
        Currently available scale sets:
        - EuropeanETRS89_LAEAQuad: Lambert Azimuthal Equal Area ETRS89 for Europe
        - WebMercatorQuad: Google Maps Compatible for the World
        - WorldCRS84Quad: CRS84 for the World
        - WorldMercatorWGS84Quad: World Mercator WGS84 (ellipsoid)

    Returns
    -------
    meintile.ScaleSetDefinition
    """
    return WKSS_BY_NAME[wkss_identifier]
