from collections import namedtuple


Bounds = namedtuple("Bounds", "left bottom right top")
Bounds.__doc__ = """
Bounds coordinates in CRS units.

Attributes
==========
left : float
    Left coordinate.
bottom : float
    Bottom coordinate.
right : float
    Right coordinate.
top : float
    Top coordinate.
"""

ScaleSet = namedtuple("ScaleSet", "definition is_global")
ScaleSet.__doc__ = """
Standard-conform Scale Set plus meintile specific properties.

Attributes
==========
definition : dict
    Pythonized OGC Scale Set definition.
is_global : bool
    Indicates whether TileMatrixSet is to be interpreted as global coverage. This will
    trigger Antimeridian wrapping.
"""

Shape = namedtuple("Shape", "height width")
Shape.__doc__ = """
Width and height in pixels.

Attributes
==========
height : int
    Number of pixel rows.
width : int
    Number of pixel columns.
"""

TileIndex = namedtuple("TileIndex", "zoom row col")
TileIndex.__doc__ = """
Unique Tile index.

Attributes
==========
zoom : int
    Zoom level / Tile Matrix.
row : int
    Tile Matrix row.
col : int
    Tile Matrix column.
"""
