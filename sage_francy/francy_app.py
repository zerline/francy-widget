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

class FrancyMessage(fdict):
    def __init__(self, **kwargs):
        super(FrancyMessage, self).__init__([
            ('id', None), ('type', None), ('text', None), ('title', None)
        ], **kwargs)

def francy_id(i):
    return "F%d" % i

class FrancyAdapter:
    r"""
    An adapter for representing a graph in a sage-francy Francy Widget

    Examples
    --------
    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> app = FrancyAdapter()
    >>> app.to_json(G)
    """
    def __init__(self, version='1.1.1'):
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = None
        self.encoder = JSONEncoder()

    def to_dict(self):
        d = copy(self.__dict__)
        del d['encoder']
        if 'canvas' in d.keys() and not isinstance(d['canvas'], dict):
            d['canvas'] = d['canvas'].to_dict()
        return d

    def to_json(self, obj):
        if not self.canvas:
            self.canvas = FrancyCanvas(title='') #str(obj)))
        self.canvas.set_graph(obj)
        return self.encoder.encode(self.to_dict())

class FrancyCanvas:
    r"""
    Displays a canvas

    Examples
    --------
    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> FC = FrancyCanvas()
    >>> FC.set_graph(G)
    >>> FC.to_json(JSONEncoder())
    """
    def __init__(self, title="My Canvas", width=800, height=100, zoomToFit=True, texTypesetting=False):
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
        self.graph = FrancyGraph(graph)

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

    def to_dict(self):
        d = copy(self.__dict__)
        if 'graph' in d.keys():
            d['graph'] = d['graph'].to_dict()
        return d

    def to_json(self, encoder):
        return encoder.encode(self.to_dict())


class FrancyMenu:
    def __init__(self, title, callback, menus, messages):
        r"""
        Input
        ----
        * title -- a string
        * callback -- a Callback named tuple
        * menus -- a list of Menu named tuples
        * messages -- a list of FrancyMessage named tuples
        """
        self.title = title
        self.callback = tuple2dict(callback)
        self.menus = {}
        for m in menus:
            self.menus[m.id] = tuple2dict(m)
        self.messages = {}
        for m in messages:
            self.messages[m.id] = tuple2dict(m)

    def to_json(self, encoder):
        return encoder.encode(self.__dict__)

class FrancyGraph:
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
    def __init__(self, graph, graphType=None, simulation=True, collapsed=True, drag=False, showNeighbours=False, nodeType='circle', nodeSize=10, color="", highlight=True):
        self.graph = graph
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

    def compute(self, rank=0):
        rank += 1
        self.id = francy_id(rank)
        if not self.type:
            if self.graph.is_directed():
                self.type = "directed"
            else:
                self.type = "undirected"
        self.nodes = {}
        for n in self.graph.nodes:
            if type(n) == type(()):
                title = str(n[0])
            else:
                title = str(n)
            rank += 1
            ident = francy_id(rank)
            self.nodes[ident] = GraphNode(
                id = ident,
                type = self.nodeType,
                size = self.nodeSize,
                title = title,
                color = self.color,
                highlight = self.highlight,
                layer = rank
            )
        self.links = {}
        for e in self.graph.edges:
            rank += 1
            ident = francy_id(rank)
            self.links[ident] = GraphEdge(
                id = ident,
                source = francy_id(e[0]),
                weight = 1,
                color = self.color,
                target = francy_id(e[1])
            )

    def to_dict(self):
        d = copy(self.__dict__)
        del d['graph']
        return d

    def to_json(self, encoder):
        return encoder.encode(self.to_dict())
