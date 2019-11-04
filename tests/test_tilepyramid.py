import pytest

from meintile import TilePyramid, TileMatrixSet, TileMatrix, Tile
from meintile.exceptions import InvalidTileIndex, InvalidTileMatrixIndex
from meintile.wkss import get_wkss


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

    # use WKSS dictionary
    tp = TilePyramid.from_wkss(get_wkss("WorldCRS84Quad").definition)

    # rais error on invalid input
    with pytest.raises(TypeError):
        TilePyramid.from_wkss(None)


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


def test_methods():
    tp = TilePyramid.from_wkss("WebMercatorQuad")

    # Tile construction
    assert isinstance(tp.tile(0, 0, 0), Tile)
    with pytest.raises(InvalidTileMatrixIndex):
        tp.tile(None, 0, 0)
    with pytest.raises(InvalidTileIndex):
        tp.tile(0, None, 0)
    with pytest.raises(InvalidTileIndex):
        tp.tile(0, 0, None)
    with pytest.raises(InvalidTileIndex):
        tp.tile(0, 1, 0)
    with pytest.raises(InvalidTileIndex):
        tp.tile(0, 0, 1)

    assert tp.matrix_width(0) == 1
    assert tp.matrix_height(0) == 1


def test_attributes():
    tp = TilePyramid.from_wkss("WebMercatorQuad")
    assert tp.pixel_x_size(5) == -tp.pixel_y_size(5)
