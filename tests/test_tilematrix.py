from meintile import TilePyramid


def test_web_mercator_pixel_sizes(web_mercator_pixel_sizes):
    tp = TilePyramid.from_wkss("WebMercatorQuad")
    for i in range(len(tp)):
        assert round(tp.pixel_x_size(i), 9) == round(web_mercator_pixel_sizes[i], 9)


def test_web_mercator_matrix_bounds(web_mercator_bounds):
    tp = TilePyramid.from_wkss("WebMercatorQuad")
    for tm in tp:
        assert tm.bounds == web_mercator_bounds


def test_crs84_pixel_sizes(crs84_pixel_sizes):
    tp = TilePyramid.from_wkss("WorldCRS84Quad")
    for i in range(len(tp)):
        assert round(tp.pixel_x_size(i), 9) == round(crs84_pixel_sizes[i], 9)


def test_crs84_matrix_bounds(crs84_bounds):
    tp = TilePyramid.from_wkss("WorldCRS84Quad")
    for tm in tp:
        assert tm.bounds == crs84_bounds
