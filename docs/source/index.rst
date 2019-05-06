=====================
Francy Python Adapter
=====================

A Python adapter for Francy
to graphically represent graphs in Jupyter.

This package presents a specialized Francy widget,
which is based on an `ipywidgets` widget.

To use this module, you need to import it::

    from francy_widget import *

You can feed this widget with any python `networkx` graph::

    import networkx
    g = network.PathGraph(3)
    w = FrancyWidget(g)
    w

This work is licensed under a `Creative Commons Attribution-Share Alike
3.0 License`__.

__ https://creativecommons.org/licenses/by-sa/3.0/

Francy Widget
=============

.. toctree::
   :maxdepth: 2
   :glob:

   francy_*

.. automodule:: francy_widget
   :members:
   :special-members:
   :undoc-members:
   :show-inheritance:
   :exclude-members:

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
