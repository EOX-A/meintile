"""
Constants suggested by OGC.

http://docs.opengeospatial.org/is/17-083r2/17-083r2.html

SCALE MULTIPLIER:

"The scale denominator is defined here with respect to a “standardized rendering pixel
size” of 0.28 mm × 0.28 mm (millimeters). The definition is the same as used in Web Map
Service WMS 1.3.0 [OGC 06-042] and in Symbology Encoding (SE) Implementation Specification
1.1.0 [OGC 05-077r4] and later adopted by WMTS 1.0 [OGC 07-057r7]. Frequently, the true
pixel size is unknown and 0.28 mm has the actual size of a common display from 2005. This
value is still being used as reference even if current display devices are built with
pixel sizes much smaller.

NOTE: Since the 1980s, the Microsoft Windows operating system has set their default
standard display pixels per inch (PPI) to 96. This value results in an approximated
0.264 mm per pixel. The similarity of this value with the actual 0.28 mm adopted in this
standard can create some confusion."


PRECISION:

"NOTE: Clients and servers have to be careful when comparing floating numbers with
tolerance (double precision, 16-digit numbers, have to be used)."
"""

SCALE_MULTIPLIER = 0.28

PRECISION = 16
