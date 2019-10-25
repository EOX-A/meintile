# import pytest
# from rasterio.crs import CRS

# from meintile import ScaleSetDefinition, wkss
# from meintile.exceptions import InvalidCRS


# def test_wkss():
#     for i in [
#         "EuropeanETRS89_LAEAQuad",
#         "WebMercatorQuad",
#         "WorldCRS84Quad",
#         "WorldMercatorWGS84Quad"
#     ]:
#         scale_set = wkss.get_wkss("EuropeanETRS89_LAEAQuad")
#         assert isinstance(scale_set, ScaleSetDefinition)
#         assert scale_set.__repr__()
#         assert isinstance(scale_set.crs, CRS)


# def test_errors():
#     with pytest.raises(TypeError):
#         ScaleSetDefinition(None)
#     with pytest.raises(InvalidCRS):
#         ScaleSetDefinition(dict(), crs="invalid")
