===========
Sage Francy
===========

Francy Python adapter for representing graphs in Jupyter

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/zerline/sage-francy/master?filepath=demo_SageFrancy.ipynb


Installation
------------

Local install from source
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the source from the git repository::

    $ git clone https://github.com/zerline/sage-francy.git

Change to the root directory and run::

    $ sage -pip install --upgrade --no-index -v .

For convenience this package contains a [makefile](makefile) with this
and other often used commands. Should you wish too, you can use the
shorthand::

    $ make install

Usage
-----

Once the package is installed, you can use it in Jupyter Notebook.

    from sage_francy import FrancyWidget
    import networkx
    g = network.PathGraph(3)
    w = FrancyWidget(g)
    w

See the `demo notebook <demo_SageFrancy.ipynb>`_.

Sage Usage
----------

This package is usable also within the Sagemath environment:

See the `Sage demo <test_S4.ipynb>`_.


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
