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
