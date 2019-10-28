from meintile import TilePyramid, TileMatrixSet, TileMatrix


def test_from_wkss():
    for i in [
        "EuropeanETRS89_LAEAQuad",
        "WebMercatorQuad",
        "WorldCRS84Quad",
        "WorldMercatorWGS84Quad",
    ]:
        tp = TilePyramid.from_wkss(i)
        assert isinstance(tp, TilePyramid)
        assert isinstance(tp, TileMatrixSet)

    # now again constructing TileMatrixSet objects
    for i in [
        "EuropeanETRS89_LAEAQuad",
        "WebMercatorQuad",
        "WorldCRS84Quad",
        "WorldMercatorWGS84Quad",
    ]:
        tms = TileMatrixSet.from_wkss(i)
        assert isinstance(tms, TileMatrixSet)


def test_iter():
    # iterate over TilePyramid / TileMatrixSet to get TileMatrix objects
    tp = TilePyramid.from_wkss("WebMercatorQuad")

    for tile_matrix_id, tile_matrix in tp.items():
        assert isinstance(tile_matrix_id, int)
        assert isinstance(tile_matrix, TileMatrix)

    for tile_matrix_id in tp.keys():
        assert isinstance(tile_matrix_id, int)

    for tile_matrix in tp.values():
        assert isinstance(tile_matrix, TileMatrix)


def test_get():
    tp = TilePyramid.from_wkss("WebMercatorQuad")
    for i in range(len(tp)):
        tile_matrix = tp[i]
        assert isinstance(tile_matrix, TileMatrix)
