from rasterio.crs import CRS

from meintile import wkss


def test_laea():
    laea = wkss.get_wkss("EuropeanETRS89_LAEAQuad")
    laea.__repr__()
    assert isinstance(laea.crs, CRS)
