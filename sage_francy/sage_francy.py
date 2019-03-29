# -*- coding: utf-8 -*-
r"""
A Francy Widget for Jupyter Notebook.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from ipywidgets import HTML, register
from traitlets import Unicode

@register
class FrancyWidget(HTML):
    """Francy widget."""
    _view_name = Unicode('FrancyView').tag(sync=True)
    _view_module = Unicode('sage-francy').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
