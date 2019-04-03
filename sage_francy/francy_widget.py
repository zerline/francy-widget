# -*- coding: utf-8 -*-
r"""
A Francy Widget for the Jupyter Notebook.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from ipywidgets import register
from ipywidgets.widgets.widget_string import _String
from traitlets import Unicode

css_lines = []
css_lines.append(".widget-francy {font-size: 13px;}")
css_lines.append(".widget-francy > .widget-francy-content {/* Fill out the area in the HTML widget */\n\
    -ms-flex-item-align: stretch;\n        align-self: stretch;\n    -webkit-box-flex: 1;\n\
        -ms-flex-positive: 1;\n            flex-grow: 1;\n    -ms-flex-negative: 1;\n        flex-shrink: 1;\n\
    /* Makes sure the baseline is still aligned with other elements */\n    line-height: 28px;\n\
    /* Make it possible to have absolutely-positioned elements in the html */\n    position: relative;\n}}")

@register
class FrancyWidget(_String):
    """Francy widget."""
    _view_name = Unicode('FrancyView').tag(sync=True)
    _view_module = Unicode('sage-francy').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_name = Unicode('FrancyModel').tag(sync=True)
    _model_module = Unicode('sage-francy').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    def _ipython_display_(self, **kwargs):
        """Called when `IPython.display.display` is called on the widget."""
        if self._view_name is not None:
            plaintext = repr(self)
            if len(plaintext) > 110:
                plaintext = plaintext[:110] + '…'
            # The 'application/vnd.francy+json' mimetype has not been registered yet.
            # See the registration process and naming convention at
            # http://tools.ietf.org/html/rfc6838
            # and the currently registered mimetypes at
            # http://www.iana.org/assignments/media-types/media-types.xhtml.
            data = {
                'text/plain': plaintext,
                'application/vnd.francy+json': self.value
            }
            display(data, raw=True)

            self._handle_displayed(**kwargs)
