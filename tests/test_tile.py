import pytest
import tilematrix

from meintile import TilePyramid


def _round_tuple(t, r):
    return tuple(map(lambda x: round(x, r), t))


def test_web_mercator_tile_bounds():
    tp = TilePyramid.from_wkss("WebMercatorQuad")
    tp_ref = tilematrix.TilePyramid("mercator")
    for zoom in range(10):
        for row, col in zip(
            list(range(tp.matrix_height(zoom))), list(range(tp.matrix_width(zoom)))
        ):
            # there is different precision between packages and to account for rounding
            # errors we have to round both bounds
            round_value = 2
            rounded_bounds = _round_tuple(tp.tile(zoom, row, col).bounds, round_value)
            rounded_ref_bounds = _round_tuple(
                tp_ref.tile(zoom, row, col).bounds(), round_value
            )
            assert rounded_bounds == rounded_ref_bounds


def test_crs84_tile_bounds():
    tp = TilePyramid.from_wkss("WorldCRS84Quad")
    tp_ref = tilematrix.TilePyramid("geodetic")
    for zoom in range(10):
        for row, col in zip(
            list(range(tp.matrix_height(zoom))), list(range(tp.matrix_width(zoom)))
        ):
            # leave out every second column to follow a diagonal path from corner to
            # corner of the WGS84 Tile Matrix
            col = col * 2
            # there is different precision between packages and to account for rounding
            # errors we have to round both bounds
            round_value = 8
            rounded_bounds = _round_tuple(tp.tile(zoom, row, col).bounds, round_value)
            rounded_ref_bounds = _round_tuple(
                tp_ref.tile(zoom, row, col).bounds(), round_value
            )
            assert rounded_bounds == rounded_ref_bounds


def test_parents_children():
    tp = TilePyramid.from_wkss("WorldCRS84Quad")
    tile = tp.tile(5, 5, 5)

    children = tile.get_children()
    assert len(children) == 4
    for child in children:
        assert child.get_parent().id == tile.id

    top_tile = tp.tile(0, 0, 0)
    assert top_tile.get_parent() is None


def test_neighbors():
    tp = TilePyramid.from_wkss("WorldCRS84Quad")
    tile = tp.tile(5, 5, 5)
    # neighbors
    neighbors_control = [(5, 4, 5), (5, 6, 5), (5, 5, 4), (5, 5, 6)]
    neighbors = tile.get_neighbors(connectedness=4)
    assert len(neighbors) == 4
    for neighbor in neighbors:
        assert neighbor.id in neighbors_control

    neighbors_control.extend([(5, 4, 4), (5, 4, 6), (5, 6, 4), (5, 6, 6)])
    neighbors = tile.get_neighbors(connectedness=8)
    assert len(neighbors) == 8
    for neighbor in neighbors:
        assert neighbor.id in neighbors_control

    with pytest.raises(ValueError):
        tile.get_neighbors(connectedness="invalid")

    # over antimeridian
    tile = tp.tile(3, 1, 0)
    # 8 neighbors
    test_neighbors = {
        (3, 0, 0),
        (3, 1, 1),
        (3, 2, 0),
        (3, 1, 15),
        (3, 0, 1),
        (3, 2, 1),
        (3, 2, 15),
        (3, 0, 15),
    }
    neighbors = {t.id for t in tile.get_neighbors()}
    assert test_neighbors == neighbors
    # 4 neighbors
    test_neighbors = {(3, 0, 0), (3, 1, 1), (3, 2, 0), (3, 1, 15)}
    neighbors = {t.id for t in tile.get_neighbors(connectedness=4)}
    assert test_neighbors == neighbors

    # tile has exactly two identical neighbors
    tile = tp.tile(0, 0, 0)
    test_tile = [(0, 0, 1)]
    neighbors = [t.id for t in tile.get_neighbors(connectedness=8)]
    assert test_tile == neighbors

    # tile is alone at current zoom level
    tp = TilePyramid.from_wkss("WebMercatorQuad")
    tile = tp.tile(0, 0, 0)
    neighbors = [t.id for t in tile.get_neighbors(connectedness=8)]
    assert neighbors == []

    # don't wrap over antimeridian on non-global scale set
    tp = TilePyramid.from_wkss("EuropeanETRS89_LAEAQuad")
    tile = tp.tile(3, 1, 0)
    # 8 neighbors
    test_neighbors = {(3, 0, 0), (3, 1, 1), (3, 2, 0), (3, 0, 1), (3, 2, 1)}
    neighbors = {t.id for t in tile.get_neighbors(connectedness=8)}
    assert test_neighbors == neighbors
    # 4 neighbors
    test_neighbors = {(3, 0, 0), (3, 1, 1), (3, 2, 0)}
    neighbors = {t.id for t in tile.get_neighbors(connectedness=4)}
    assert test_neighbors == neighbors
    # other way round
    tile = tp.tile(3, 1, 7)
    test_neighbors = {(3, 0, 7), (3, 1, 6), (3, 2, 7), (3, 0, 6), (3, 2, 6)}
    neighbors = {t.id for t in tile.get_neighbors(connectedness=8)}
    assert test_neighbors == neighbors


def test_magic_methods():
    tp = TilePyramid.from_wkss("WorldCRS84Quad")
    tile = tp.tile(5, 5, 5)
    assert str(tile)
    assert hash(tile)
    for i in tile:
        assert i == 5
