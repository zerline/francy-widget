# -*- coding: utf-8 -*-
r"""
A Francy Widget for the Jupyter Notebook.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from json import JSONEncoder
from collections import defaultdict
from copy import copy

class fdict(dict):
    def __init__(self, *args, **kwargs):
        super(fdict, self).__init__(*args, **kwargs)
        to_drop = []
        for k in self.keys():
            if self[k] is None:
                to_drop.append(k)
        for k in to_drop:
            del(self[k])

class GraphNode(fdict):
    def __init__(self, **kwargs):
        super(GraphNode, self).__init__([
            ('id', None), ('x', 0), ('y', 0), ('type', None), ('size', None), ('title', ''), ('conjugate', None), ('color', ''),
            ('highlight', None), ('layer', None), ('parent', ''), ('menus', {}), ('messages', {}), ('callbacks', {})
        ], **kwargs)

class GraphEdge(fdict):
    def __init__(self, **kwargs):
        super(GraphEdge, self).__init__([
            ('id', None), ('source', None), ('weight', None), ('color', ''), ('target', None)
        ], **kwargs)

class Callback(fdict):
    def __init__(self, **kwargs):
        super(CallBack, self).__init__([
            ('id', None), ('func', str), ('trigger', str), ('knownArgs', list), ('requiredArgs', dict)
        ], **kwargs)

def francy_id(i):
    return "F%d" % i

class FrancyOutput:
    r"""
    A base class for Francy JSON representable objects having an id as required attribute.

    Input
    ----
    * counter -- an integer
    * encoder -- a JSON encoder

    Test
    ----
    >>> o = FrancyOutput(3)
    >>> o.encoder.__class__
    <class 'json.encoder.JSONEncoder'>
    >>> o.id
    'F4'
    >>> o.to_dict()
    {'id': 'F4'}
    >>> o.to_json()
    '{"id": "F4"}'
    """

    def __init__(self, counter=0, encoder=None):
        counter += 1
        self.counter = counter
        if not encoder:
            encoder = JSONEncoder()
        self.encoder = encoder
        self.obj = None
        self.id = francy_id(counter)

    def to_dict(self):
        d = copy(self.__dict__)
        del d['counter']
        del d['encoder']
        for k in ['obj']:
            if k in d:
                del d[k]
        for k in ['canvas', 'graph', 'menus']:
            if k in d and not isinstance(d[k], dict):
                d[k] = d[k].to_dict()
        return d

    def to_json(self):
        return self.encoder.encode(self.to_dict())

class FrancyMessage(fdict, FrancyOutput):
    def __init__(self, counter, **kwargs):
        fdict.__init__([
            ('id', None), ('type', None), ('text', None), ('title', None)
        ], **kwargs)
        FrancyOutput.__init__(counter)

class FrancyAdapter(FrancyOutput):
    r"""
    An adapter for representing a graph in a sage-francy Francy Widget

    Examples
    --------
    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> a = FrancyAdapter()
    >>> a.to_json(G)
    '{"version": "1.1.3", "mime": "application/vnd.francy+json", "canvas": {"id": "F1", "title": "A graph of type <class \'networkx.classes.graph.Graph\'>", "width": 800, "height": 100, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "F3", "type": "undirected", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F4": {"id": "F4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F5": {"id": "F5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F6": {"id": "F6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F7": {"id": "F7", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F8": {"id": "F8", "source": "F4", "weight": 1, "color": "", "target": "F5"}, "F9": {"id": "F9", "source": "F5", "weight": 1, "color": "", "target": "F6"}, "F10": {"id": "F10", "source": "F6", "weight": 1, "color": "", "target": "F7"}}}, "menus": {}, "messages": {}}}'
    """
    def __init__(self, version='1.1.3', counter=-1):
        super(FrancyAdapter, self).__init__(counter=counter)
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = None

    def to_dict(self, obj, **kws):
        canvas_kws = {}
        canvas_kws['title'] = "A graph of type %s" % repr(type(obj)) # default title
        for k in ['title', 'width', 'height', 'zoomToFit', 'texTypesetting']:
            if k in kws:
                canvas_kws[k] = kws[k]
                del kws[k]
        if not self.canvas:
            self.canvas = FrancyCanvas(self.counter, self.encoder, **canvas_kws)
        self.canvas.set_graph(obj, **kws)
        d = super(FrancyAdapter, self).to_dict()
        del d['id']
        return d

    def to_json(self, obj, **kws):
        return self.encoder.encode(self.to_dict(obj, **kws))

class FrancyCanvas(FrancyOutput):
    r"""
    Displays a canvas

    Examples
    --------
    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> FC = FrancyCanvas()
    >>> FC.set_graph(G)
    >>> FC.to_json()
    '{"id": "F1", "title": "My Canvas", "width": 800, "height": 100, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "F3", "type": "undirected", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F4": {"id": "F4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F5": {"id": "F5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F6": {"id": "F6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F7": {"id": "F7", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F8": {"id": "F8", "source": "F4", "weight": 1, "color": "", "target": "F5"}, "F9": {"id": "F9", "source": "F5", "weight": 1, "color": "", "target": "F6"}, "F10": {"id": "F10", "source": "F6", "weight": 1, "color": "", "target": "F7"}}}, "menus": {}, "messages": {}}'
    """
    def __init__(self, counter=0, encoder=None, title="My Canvas", width=800, height=100, zoomToFit=True, texTypesetting=False):
        super(FrancyCanvas, self).__init__(counter, encoder)
        self.title = title
        self.width = width
        self.height = height
        self.zoomToFit = zoomToFit
        self.texTypesetting = texTypesetting
        self.graph = None
        self.menus = {}
        self.messages = {}

    def set_graph(self, graph, **kws):
        r"""
        Input
        ----
        * graph -- a FrancyGraph object
        """
        self.graph = FrancyGraph(graph, self.counter, self.encoder, **kws)

    def add_menu(self, menu):
        r"""
        Input
        ----
        * menu -- a FrancyMenu object
        """
        self.menus[menu.id] = tuple2dict(menu)

    def add_message(self, message):
        r"""
        Input
        ----
        * message -- a FrancyMessage named tuple
        """
        self.messages[message.id] = tuple2dict(message)

class FrancyMenu(FrancyOutput):
    def __init__(self, counter, encoder, title='', callback=None, menus=None, messages=None):
        r"""
        Input
        ----
        * counter -- an integer
        * encoder -- a JSON encoder
        * title -- a string
        * callback -- a Callback named tuple
        * menus -- a list of Menu named tuples
        * messages -- a list of FrancyMessage named tuples
        """
        super(FrancyMenu, self).__init__(counter, encoder)
        self.title = title
        self.callback = tuple2dict(callback)
        self.menus = {}
        for m in menus:
            self.menus[m.id] = tuple2dict(m)
        self.messages = {}
        for m in messages:
            self.messages[m.id] = tuple2dict(m)

class FrancyGraph(FrancyOutput):
    r"""
    Displays a graph (ie a networkx object)

    Examples
    --------
    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> FG = FrancyGraph(G, 15, JSONEncoder())
    >>> FG.to_json()
    '{"id": "F17", "type": "undirected", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F18": {"id": "F18", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F19": {"id": "F19", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F20": {"id": "F20", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F21": {"id": "F21", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F22": {"id": "F22", "source": "F18", "weight": 1, "color": "", "target": "F19"}, "F23": {"id": "F23", "source": "F19", "weight": 1, "color": "", "target": "F20"}, "F24": {"id": "F24", "source": "F20", "weight": 1, "color": "", "target": "F21"}}}'
    """
    def __init__(self, obj, counter, encoder, graphType=None, simulation=True, collapsed=True, drag=False, showNeighbours=False, nodeType='circle', nodeSize=10, color="", highlight=True):
        super(FrancyGraph, self).__init__(counter)
        self.obj = obj
        self.type = graphType
        self.simulation = simulation
        self.collapsed = collapsed
        self.drag = drag
        self.showNeighbours = showNeighbours
        self.nodeType = nodeType
        self.nodeSize = nodeSize
        self.color = color
        self.highlight = True
        self.compute()

    def compute(self):
        counter = self.counter
        counter += 1
        layer = 0
        self.id = francy_id(counter)
        if not self.type:
            if self.obj.is_directed():
                self.type = "directed"
            else:
                self.type = "undirected"
        self.nodes = {}
        for n in self.obj.nodes:
            if type(n) == type(()):
                title = str(n[0])
            else:
                title = str(n)
            counter += 1
            layer += 1
            ident = francy_id(counter)
            # construct a dict with original node ids
            # this is necessary to compute the edges after that
            self.nodes[n] = GraphNode(
                id = ident,
                type = self.nodeType,
                size = self.nodeSize,
                title = title,
                color = self.color,
                highlight = self.highlight,
                layer = layer
            )
        self.links = {}
        for e in self.obj.edges:
            counter += 1
            ident = francy_id(counter)
            self.links[ident] = GraphEdge(
                id = ident,
                source = self.nodes[e[0]]['id'],
                weight = 1,
                color = self.color,
                target = self.nodes[e[1]]['id']
            )
        if self.type == "tree":
            # specify node parents
            for (src, tgt) in self.obj.edges:
                self.nodes[tgt]['parent'] = self.nodes[src]['id']

    def to_dict(self):
        for n in self.obj.nodes: # replace original # with new ids
            self.nodes[self.nodes[n]['id']] = self.nodes[n]
        for n in self.obj.nodes:
            del self.nodes[n]
        d = super(FrancyGraph, self).to_dict()
        for k in ['nodeType', 'nodeSize', 'color', 'highlight']:
            if k in d:
                del d[k]
        return d
