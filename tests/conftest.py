import pytest


@pytest.fixture
def web_mercator_pixel_sizes():
    return [
        156543.033928041,
        78271.5169640205,
        39135.7584820102,
        19567.8792410051,
        9783.9396205026,
        4891.9698102513,
        2445.9849051256,
        1222.9924525628,
        611.4962262814,
        305.7481131407,
        152.8740565704,
        76.4370282852,
        38.2185141426,
        19.1092570713,
        9.5546285356,
        4.7773142678,
        2.3886571339,
        1.194328567,
        0.5971642835,
        0.2985821417,
        0.1492910709,
        0.0746455354,
        0.0373227677,
        0.0186613839,
        0.0093306919,
    ]


@pytest.fixture
def web_mercator_bounds():
    return (-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892)


@pytest.fixture
def crs84_pixel_sizes():
    return [
        0.703125,
        0.3515625,
        0.17578125,
        8.78906250000000 * 10 ** -2,
        4.39453125000000 * 10 ** -2,
        2.19726562500000 * 10 ** -2,
        1.09863281250000 * 10 ** -2,
        5.49316406250000 * 10 ** -3,
        2.74658203125000 * 10 ** -3,
        1.37329101562500 * 10 ** -3,
        6.86645507812500 * 10 ** -4,
        3.43322753906250 * 10 ** -4,
        1.71661376953125 * 10 ** -4,
        8.58306884765625 * 10 ** -5,
        4.29153442382812 * 10 ** -5,
        2.14576721191406 * 10 ** -5,
        1.07288360595703 * 10 ** -5,
        5.36441802978516 * 10 ** -6,
    ]


@pytest.fixture
def crs84_bounds():
    return (-180.0, -90.0, 180.0, 90.0)
