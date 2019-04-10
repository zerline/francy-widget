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
    def __init__(self, counter=0, encoder=None):
        r"""
        A base class for Francy JSON representable objects having an id as required attribute.

        Input
        ----
        * counter -- an integer
        * encoder -- a JSON encoder

        Test
        ----
        >>> o = FrancyOutput(3)
        >>> o.encoder
        JSONEncoder
        >>> o.id
        F3
        >>> o.to_dict()
        {}
        >>> o.to_json()
        ''
        """
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
    """
    def __init__(self, version='1.1.1', counter=-1):
        super(FrancyAdapter, self).__init__(counter=counter)
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = None

    def to_dict(self, obj):
        if not self.canvas:
            self.canvas = FrancyCanvas(self.counter, self.encoder, title=repr(obj))
        self.canvas.set_graph(obj)
        d = super(FrancyAdapter, self).to_dict()
        del d['id']
        return d

    def to_json(self, obj):
        return self.encoder.encode(self.to_dict(obj))

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

    def set_graph(self, graph):
        r"""
        Input
        ----
        * graph -- a FrancyGraph object
        """
        self.graph = FrancyGraph(graph, self.counter, self.encoder)

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
    >>> FG = FrancyGraph(G)
    >>> FG.to_json(JSONEncoder())
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
            ident = francy_id(counter)
            self.nodes[ident] = GraphNode(
                id = ident,
                type = self.nodeType,
                size = self.nodeSize,
                title = title,
                color = self.color,
                highlight = self.highlight,
                layer = counter
            )
        self.links = {}
        for e in self.obj.edges:
            counter += 1
            ident = francy_id(counter)
            self.links[ident] = GraphEdge(
                id = ident,
                source = francy_id(e[0]),
                weight = 1,
                color = self.color,
                target = francy_id(e[1])
            )
