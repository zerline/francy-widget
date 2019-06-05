# -*- coding: utf-8 -*-
r"""
A Francy Widget for the Jupyter Notebook.

AUTHORS ::

    Odile Bénassy

"""
from ipywidgets import register
from ipywidgets.widgets.widget_string import Text
from traitlets import Any
from json import loads # for callbacks
try:
    from .francy_adapter import FrancyAdapter
except:
    from francy_adapter import FrancyAdapter # for doctesting


def Trigger(s):
    try:
        c = loads(s)
        assert('funcname' in c and 'knownArgs' in c and type(c['knownArgs']) == type([]))
    except:
        print("KO")
    if 'funcscope' in c and c['funcscope'] in ['object', 'class']:
        o = eval(c['knownArgs'][0])
        print(getattr(o, c['funcname']).__call__(*c['knownArgs'][1:]))
    else:
        print(eval(c['funcname']).__call__(*c['knownArgs']))

@register
class FrancyWidget(Text):
    r"""
    Francy widget.

    Test:

    >>> from networkx import Graph
    >>> G = Graph([(1, 2), (2, 3), (3, 4)])
    >>> w = FrancyWidget(G)
    >>> w.make_json()
    >>> len(w.adapter.canvas.graph.nodes)
    4
    """
    value = Any()  # should be a networkx graph
    adapter = FrancyAdapter()

    def __init__(self, obj=None, title="", counter=-1, menus=[], messages=[],
                 node_options=None, link_options=None, **kws):
        r"""
        Test:

        >>> from networkx import Graph
        >>> G = Graph([(1, 2), (2, 3), (3, 4)])
        >>> w = FrancyWidget(G)
        >>> w.value.__class__
        <class 'networkx.classes.graph.Graph'>
        """
        self.value = obj
        self.title = title
        if counter > -1:
            self.adapter.counter = counter
        self.test_json = False
        if 'test_json' in kws and kws['test_json']:
            self.test_json = True
            del kws['test_json']
        self.menus = menus
        self.messages = messages
        self.node_options = node_options  # A function: node object -> dict of options
        self.link_options = link_options  # A function: link object -> dict of options
        self.draw_kws = kws  # width, height ..
        self.json_data = None

    def validate(self, obj, obj_class=None):
        r"""
        Validate object type.
        """
        if self.test_json:
            import json
            try:
                json.loads(obj)
            except IOError:
                return False
            else:
                return True
        if obj_class:
            return issubclass(obj.__class__, obj_class)
        try:
            from sage.all import SageObject
            return issubclass(obj.__class__, SageObject)
        except:
            return False

    def set_value(self, obj, **kws):
        r"""
        Check compatibility, then set editor value.

        Test:

        >>> from networkx import Graph
        >>> G = Graph([(1, 2), (2, 3), (3, 4)])
        >>> w = FrancyWidget()
        >>> w.set_value(G)
        >>> len(w.canvas_id)
        32
        """
        if self.value and not self.validate(obj, self.value.__class__):
            raise ValueError("Object %s is not compatible." % str(obj))
        self.value = obj
        self.make_json()
        if not self.test_json:
            self.canvas_id = self.adapter.canvas.id

    def make_json(self):
        r"""
        Make JSON output for the display.

        Test:

        >>> from networkx import Graph
        >>> G = Graph([(1, 2), (2, 3), (3, 4)])
        >>> def node_options(n):
        ...   options = {}
        ...   options['type'] = 'square'
        ...   options['modal_menus'] = [{
        ...     'title': 'cardinality',
        ...     'funcname': 'cardinality',
        ...     'is_method': True
        ...   }]
        ...   return options
        >>> w = FrancyWidget(G, base_id='mycanvas', title="A small, but rich graph", node_options=node_options)
        >>> w.make_json()
        >>> w.json_data
        '{"version": "1.1.3", "mime": "application/vnd.francy+json", "canvas": {"id": "mycanvas", "title": "A small, but rich graph", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "mycanvas_graph2", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node3": {"id": "mycanvas_node3", "x": 0, "y": 0, "type": "square", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {"mycanvas_menu4": {"id": "mycanvas_menu4", "title": "cardinality", "callback": {"id": "mycanvas_callback4", "funcname": "cardinality", "trigger": "click", "knownArgs": ["python", "<object>"], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node4": {"id": "mycanvas_node4", "x": 0, "y": 0, "type": "square", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {"mycanvas_menu5": {"id": "mycanvas_menu5", "title": "cardinality", "callback": {"id": "mycanvas_callback5", "funcname": "cardinality", "trigger": "click", "knownArgs": ["python", "<object>"], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node5": {"id": "mycanvas_node5", "x": 0, "y": 0, "type": "square", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {"mycanvas_menu6": {"id": "mycanvas_menu6", "title": "cardinality", "callback": {"id": "mycanvas_callback6", "funcname": "cardinality", "trigger": "click", "knownArgs": ["python", "<object>"], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node6": {"id": "mycanvas_node6", "x": 0, "y": 0, "type": "square", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 6, "parent": "", "menus": {"mycanvas_menu7": {"id": "mycanvas_menu7", "title": "cardinality", "callback": {"id": "mycanvas_callback7", "funcname": "cardinality", "trigger": "click", "knownArgs": ["python", "<object>"], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge7": {"source": "mycanvas_node3", "weight": 1, "color": "", "target": "mycanvas_node4", "id": "mycanvas_edge7"}, "mycanvas_edge8": {"source": "mycanvas_node4", "weight": 1, "color": "", "target": "mycanvas_node5", "id": "mycanvas_edge8"}, "mycanvas_edge9": {"source": "mycanvas_node5", "weight": 1, "color": "", "target": "mycanvas_node6", "id": "mycanvas_edge9"}}, "type": "undirected"}, "menus": {}, "messages": {}}}'
        """
        if self.test_json:
            self.json_data = self.value
        else:
            self.json_data = self.adapter.to_json(
                self.value,
                title=self.title,
                menus=self.menus,
                messages=self.messages,
                node_options=self.node_options,
                link_options=self.link_options,
                **self.draw_kws
            )

    def _ipython_display_(self, **kws):
        """Called when `IPython.display.display` is called on the widget."""
        if self._view_name is not None:
            plaintext = repr(self)
            if len(plaintext) > 110:
                plaintext = plaintext[:110] + '…'
            if not self.json_data:
                self.make_json()
            # The 'application/vnd.francy+json' mimetype has not been registered yet.
            # See the registration process and naming convention at
            # http://tools.ietf.org/html/rfc6838
            # and the currently registered mimetypes at
            # http://www.iana.org/assignments/media-types/media-types.xhtml.
            data = {
                'text/plain': plaintext,
                'application/vnd.francy+json': self.json_data
            }

            display(data, raw=True)  # noqa

            self._handle_displayed(**kws)
