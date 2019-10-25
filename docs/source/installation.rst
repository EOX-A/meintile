============
Installation
============

Use ``pip`` to install the latest stable version:

.. code-block:: shell

    $ pip install meintile

Manually install the latest development version

.. code-block:: shell

    $ git clone git@github.com:EOX-A/meintile.git
    $ pip install -e meintile[dev]


To make sure Rasterio is properly built against your local GDAL installation, don't
install the binaries but build them on your system:

.. code-block:: shell

    $ pip install --upgrade rasterio --no-binary :all:
