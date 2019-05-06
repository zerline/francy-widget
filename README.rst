=============
Francy Widget
=============

Francy Python adapter for representing graphs in Jupyter

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/zerline/francy-widget/master?filepath=demo_FrancyWidget.ipynb


Installation
------------

Local install from source
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the source from the git repository::

    $ git clone https://github.com/zerline/francy-widget.git

Change to the root directory and run::

    $ pip install --upgrade --no-index -v .

For convenience this package contains a [makefile](makefile) with this
and other often used commands. Should you wish too, you can use the
shorthand::

    $ make install

Usage
-----

Once the package is installed, you can use it in Jupyter Notebook.

    from francy_widget import FrancyWidget
    import networkx
    g = network.PathGraph(3)
    w = FrancyWidget(g)
    w

See the `demo notebook <demo_FrancyWidget.ipynb>`_.

Sage Usage
----------

This package is usable also within the Sagemath environment:

See the `Sage example notebook <examples/S4.ipynb>`_.


Tests
-----

Once the package is installed, you can use the Python test system
configured in ``setup.py`` to run the tests::

    $ python -m doctest

Documentation
-------------

The documentation of the package can be generated using
``Sphinx`` installation::

    $ cd docs
    $ make html

Thanks
------
All my thanks to Manuel Machado Martins for his excellent Francy package,
to Sebastian Gutsche, Sylvain Corlay, Claus Fieker and Nicolas Thiéry
for various help at different stages.
