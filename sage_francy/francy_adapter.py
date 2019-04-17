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
    r"""
    A Sage Francy dictionary.
    """
    def __init__(self, *args, **kwargs):
        r"""
        Initialize a Sage Francy dictionary.
        All None values will be deleted
        at the end of initialization.
        """
        super(fdict, self).__init__(*args, **kwargs)
        to_drop = []
        for k in self.keys():
            if self[k] is None:
                to_drop.append(k)
        for k in to_drop:
            del(self[k])

class GraphNode(fdict):
    r"""
    An immutable dictionary to hold Graph Nodes
    Identified by a math object
    """
    def __init__(self, **kwargs):
        r"""
        Initialize a GraphNode.
        All None values will be deleted
        at the end of initialization.
        """
        super(GraphNode, self).__init__([
            ('id', None), ('obj', None), ('x', 0), ('y', 0), ('type', None), ('size', None), ('nodeName', ''), ('conjugate', None), ('color', ''),
            ('highlight', None), ('layer', None), ('parent', ''), ('menus', None), ('messages', None), ('callbacks', None)
        ], **kwargs)

    def __hash__(self):
        r"""
        Has to be hashable to become a graph's node.
        """
        return hash(tuple(sorted(self.items())))

class GraphEdge(fdict):
    def __init__(self, **kwargs):
        super(GraphEdge, self).__init__([
            ('source', None), ('weight', None), ('color', ''), ('target', None)
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
        for k in ['canvas', 'graph']:
            if k in d and not isinstance(d[k], dict):
                d[k] = d[k].to_dict()
        for k in ['menus', 'messages']:
            if k in d:
                if not isinstance(d[k], dict):
                    raise TypeError(d[k])
                mm = d[k]
                for fid, m in mm.items():
                    mm[fid] = m.to_dict()
                d[k] = mm
        return d

    def to_json(self):
        return self.encoder.encode(self.to_dict())

class FrancyAdapter(FrancyOutput):
    r"""
    An adapter for representing a graph in a sage-francy Francy Widget

    Examples
    --------
    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G1 = nx.Graph(e)
    >>> a = FrancyAdapter()
    >>> a.to_json(G1, title="Example Undirected Graph")
    '{"version": "1.1.3", "mime": "application/vnd.francy+json", "canvas": {"id": "F1", "title": "Example Undirected Graph", "width": 800, "height": 100, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "F2", "type": "undirected", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F3": {"id": "F3", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F4": {"id": "F4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F5": {"id": "F5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F6": {"id": "F6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F7": {"id": "F7", "source": "F3", "weight": 1, "color": "", "target": "F4"}, "F8": {"id": "F8", "source": "F4", "weight": 1, "color": "", "target": "F5"}, "F9": {"id": "F9", "source": "F5", "weight": 1, "color": "", "target": "F6"}}}, "menus": {}, "messages": {}}}'
    >>> G2 = nx.DiGraph([('1', 'G'), ('G', 'SG1'), ('G', 'SG2')])
    >>> a.to_json(G2, title="Example Tree Graph", graphType="tree", collapsed=False, nodeTypes=['square', 'circle', 'circle', 'circle'])
    '{"version": "1.1.3", "mime": "application/vnd.francy+json", "canvas": {"id": "F1", "title": "Example Tree Graph", "width": 800, "height": 100, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "F2", "type": "tree", "simulation": true, "collapsed": false, "drag": false, "showNeighbours": false, "shapes": ["square", "circle", "circle", "circle"], "nodes": {"F3": {"id": "F3", "x": 0, "y": 0, "type": "square", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F4": {"id": "F4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "G", "color": "", "highlight": true, "layer": 2, "parent": "F3", "menus": {}, "messages": {}, "callbacks": {}}, "F5": {"id": "F5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "SG1", "color": "", "highlight": true, "layer": 3, "parent": "F4", "menus": {}, "messages": {}, "callbacks": {}}, "F6": {"id": "F6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "SG2", "color": "", "highlight": true, "layer": 4, "parent": "F4", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F7": {"id": "F7", "source": "F3", "weight": 1, "color": "", "target": "F4"}, "F8": {"id": "F8", "source": "F4", "weight": 1, "color": "", "target": "F5"}, "F9": {"id": "F9", "source": "F4", "weight": 1, "color": "", "target": "F6"}}}, "menus": {}, "messages": {}}}'
    """
    def __init__(self, version='1.1.3', counter=-1):
        super(FrancyAdapter, self).__init__(counter=counter)
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = None

    def to_dict(self, obj, **kws):
        canvas_kws = {}
        canvas_kws['title'] = "A Francy graph representation" # default title
        for k in ['title', 'width', 'height', 'zoomToFit', 'texTypesetting']:
            if k in kws:
                canvas_kws[k] = kws[k]
                del kws[k]
        self.canvas = FrancyCanvas(self.counter, self.encoder, **canvas_kws)
        if 'menus' in kws:
            for men in kws['menus']:
                self.canvas.add_menu(men)
            del kws['menus']
        if 'messages' in kws:
            for msg in kws['messages']:
                self.canvas.add_message(msg)
            del kws['messages']
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
    '{"id": "F1", "title": "My Canvas", "width": 800, "height": 100, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "F2", "type": "undirected", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F3": {"id": "F3", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F4": {"id": "F4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F5": {"id": "F5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F6": {"id": "F6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F7": {"id": "F7", "source": "F3", "weight": 1, "color": "", "target": "F4"}, "F8": {"id": "F8", "source": "F4", "weight": 1, "color": "", "target": "F5"}, "F9": {"id": "F9", "source": "F5", "weight": 1, "color": "", "target": "F6"}}}, "menus": {}, "messages": {}}'
    """
    def __init__(self, counter=0, encoder=None, title="My Canvas", width=800, height=100, zoomToFit=True, texTypesetting=False):
        super(FrancyCanvas, self).__init__(counter, encoder)
        self.title = title
        self.width = float(width) # in case we get them
        self.height = float(height) # as objects
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
        raise NotImplementedError

    def add_message(self, text, msgType="default", title=""):
        r"""
        Input
        ----
        * text -- a string
        * title -- a string
        * msgType -- message type
        """
        self.counter += 1
        fid = francy_id(self.counter)
        self.messages[fid] = FrancyMessage(text=text, title=title, msgType=msgType)

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
    '{"id": "F16", "type": "undirected", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F17": {"id": "F17", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 1, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F18": {"id": "F18", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F19": {"id": "F19", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F20": {"id": "F20", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F21": {"id": "F21", "source": "F17", "weight": 1, "color": "", "target": "F18"}, "F22": {"id": "F22", "source": "F18", "weight": 1, "color": "", "target": "F19"}, "F23": {"id": "F23", "source": "F19", "weight": 1, "color": "", "target": "F20"}}}'
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
        self.size = nodeSize
        self.color = color
        self.highlight = True
        self.layer = 0
        self.compute()

    def compute(self):
        counter = self.counter
        self.id = francy_id(counter)
        if not self.type:
            if self.obj.is_directed():
                self.type = "directed"
            else:
                self.type = "undirected"
        self.nodes = {}
        # Keep track of original nodes
        match = {}
        #layer = 0
        for n in self.obj.nodes:
            counter += 1
            ident = francy_id(counter)
            match[n] = ident
            opt = {}
            if hasattr(n, 'nodeName'):
                title = n.nodeName
            elif isinstance(n, dict) and 'nodeName' in n:
                title = n['nodeName']
            else:
                title = str(n)
            #layer += 1
            if hasattr(n, 'parentNode'):
                parent = n.parentNode
            else:
                parent = ""
            for parm in ['layer', 'size', 'nodeType', 'color', 'highlight']:
                if hasattr(n, parm):
                    opt[parm] = getattr(n, parm)
                else:
                    opt[parm] = getattr(self, parm)
            self.nodes[ident] = GraphNode(
                id = ident,
                type = opt['nodeType'],
                size = opt['size'],
                title = title,
                parent = parent,
                layer = opt['layer'],
                color = opt['color'],
                highlight = opt['highlight']
            )
        self.links = {}
        for e in self.obj.edges:
            counter += 1
            ident = francy_id(counter)
            self.links[ident] = GraphEdge(
                id = ident,
                source = match[e[0]],
                weight = 1,
                color = self.color,
                target = match[e[1]]
            )
        if self.type == "tree":
            # specify node parents
            for (src, tgt) in self.obj.edges:
                tgtNode = self.nodes[match[tgt]]
                if not hasattr(tgtNode, 'parent'):
                    # NB because our GraphNodes here do no act as actual graph node
                    # but only graph node JSON representation,
                    # we can change them although they are supposedly immutable.
                    self.nodes[match[tgt]]['parent'] = self.nodes[match[src]]['id']

class FrancyMessage(FrancyOutput):
    r"""
    Displays a message

    Examples
    --------
    >>> m = FrancyMessage(text="There are 8 levels in this Group.")
    >>> m.to_json()
    '{"id": "F1", "type": "default", "title": "", "text": "There are 8 levels in this Group."}'
    """
    def __init__(self, counter=0, encoder=None, msgType="default", title="", text=""):
        super(FrancyMessage, self).__init__(counter)
        self.type = msgType
        self.title = title
        self.text = text
