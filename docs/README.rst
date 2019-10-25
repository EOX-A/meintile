====================
Create Documentation
====================

--------------------------
Generate API Documentation
--------------------------

.. code-block:: shell

    pip install -r source/requirements.txt
    sphinx-apidoc -fe -o source/apidoc/ ../meintile ../meintile/wkss/* -H "API Reference"
