from meintile import TilePyramid, TileMatrixSet


def test_from_wkss():
    for i in [
        "EuropeanETRS89_LAEAQuad",
        "WebMercatorQuad",
        "WorldCRS84Quad",
        "WorldMercatorWGS84Quad",
    ]:
        tp = TilePyramid.from_wkss(i)
        assert isinstance(tp, TilePyramid)

    # now again constructing TileMatrixSet objects
    for i in [
        "EuropeanETRS89_LAEAQuad",
        "WebMercatorQuad",
        "WorldCRS84Quad",
        "WorldMercatorWGS84Quad",
    ]:
        tms = TileMatrixSet.from_wkss(i)
        assert isinstance(tms, TileMatrixSet)


# TODO
# iterate over TilePyramid / TileMatrixSet to get TileMatrix objects
