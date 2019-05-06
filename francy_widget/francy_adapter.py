# -*- coding: utf-8 -*-
r"""
A Francy Widget for the Jupyter Notebook.

AUTHORS ::

    Odile Bénassy

"""
from json import JSONEncoder
from copy import copy
FRANCY_NODE_TYPES = ['circle', 'diamond', 'square']


class fdict(dict):
    r"""
    A Francy Widget dictionary.
    """
    def __init__(self, *args, **kwargs):
        r"""
        Initialize a Francy Widget dictionary.
        All None values will be deleted
        at the end of initialization.
        """
        super(fdict, self).__init__(*args, **kwargs)
        to_drop = [k for k in self.keys() if self[k] is None]
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
            ('id', None),
            ('obj', None),
            ('x', 0),
            ('y', 0),
            ('type', None),
            ('size', None),
            ('title', ''),
            ('conjugate', None),
            ('color', ''),
            ('highlight', None),
            ('layer', None),
            ('parent', ''),
            ('menus', None),
            ('messages', None),
            ('callbacks', None)
        ], **kwargs)

    def __hash__(self):
        r"""
        Has to be hashable to become a graph's node.
        """
        return hash(tuple(sorted(self.items())))


class GraphEdge(fdict):
    def __init__(self, **kwargs):
        super(GraphEdge, self).__init__([
            ('source', None),
            ('weight', None),
            ('color', ''),
            ('invisible', None),
            ('length', None),
            ('target', None)
        ], **kwargs)


class Callback(fdict):
    def __init__(self, **kwargs):
        super(Callback, self).__init__([
            ('id', None), ('func', str), ('trigger', str),
            ('knownArgs', list), ('requiredArgs', dict)
        ], **kwargs)


def francy_id(i):
    return "F%d" % i


class FrancyOutput:
    r"""
    A base class for Francy JSON representable objects having an id as required attribute.

    Input:

    * counter -- an integer
    * encoder -- a JSON encoder

    Test:

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
        for k in ['obj', 'conjugate', 'node_options', 'link_options']:
            if k in d:
                # A math value or a function
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
    An adapter for representing a graph in a Francy Widget

    Examples:

    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G1 = nx.Graph(e)
    >>> a = FrancyAdapter()
    >>> a.to_dict(G1, title="Example Undirected Graph")
    {'version': '1.1.3', 'mime': 'application/vnd.francy+json', 'canvas': {'id': 'F1', 'title': 'Example Undirected Graph', 'width': 800.0, 'height': 100.0, 'zoomToFit': True, 'texTypesetting': False, 'graph': {'id': 'F2', 'simulation': True, 'collapsed': True, 'drag': False, 'showNeighbours': False, 'nodes': {'F3': {'id': 'F3', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '1', 'color': '', 'highlight': True, 'layer': 3, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}, 'F4': {'id': 'F4', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '2', 'color': '', 'highlight': True, 'layer': 4, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}, 'F5': {'id': 'F5', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '3', 'color': '', 'highlight': True, 'layer': 5, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}, 'F6': {'id': 'F6', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '4', 'color': '', 'highlight': True, 'layer': 6, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}}, 'links': {'F7': {'source': 'F3', 'weight': 1, 'color': '', 'target': 'F4', 'id': 'F7'}, 'F8': {'source': 'F4', 'weight': 1, 'color': '', 'target': 'F5', 'id': 'F8'}, 'F9': {'source': 'F5', 'weight': 1, 'color': '', 'target': 'F6', 'id': 'F9'}}, 'type': 'undirected'}, 'menus': {}, 'messages': {}}}
    """
    def __init__(self, version='1.1.3', counter=-1):
        super(FrancyAdapter, self).__init__(counter=counter)
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = None

    def to_dict(self, obj, **kws):
        canvas_kws = {}
        canvas_kws['title'] = "A Francy graph representation"  # default title
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

    Examples:

    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> FC = FrancyCanvas()
    >>> FC.set_graph(G)
    >>> FC.to_json()
    '{"id": "F1", "title": "My Canvas", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "F2", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F3": {"id": "F3", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F4": {"id": "F4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F5": {"id": "F5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F6": {"id": "F6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 6, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F7": {"source": "F3", "weight": 1, "color": "", "target": "F4", "id": "F7"}, "F8": {"source": "F4", "weight": 1, "color": "", "target": "F5", "id": "F8"}, "F9": {"source": "F5", "weight": 1, "color": "", "target": "F6", "id": "F9"}}, "type": "undirected"}, "menus": {}, "messages": {}}'
    """
    def __init__(self, counter=0, encoder=None, title="My Canvas", width=800, height=100,
                 zoomToFit=True, texTypesetting=False):
        super(FrancyCanvas, self).__init__(counter, encoder)
        self.title = title
        self.width = float(width)  # just in case we get them as objects
        self.height = float(height)
        self.zoomToFit = zoomToFit
        self.texTypesetting = texTypesetting
        self.graph = None
        self.menus = {}
        self.messages = {}

    def set_graph(self, graph, **kws):
        r"""
        Input:

        * graph -- a FrancyGraph object
        """
        self.graph = FrancyGraph(graph, self.counter, self.encoder, **kws)

    def add_menu(self, menu):
        r"""
        Input:

        * menu -- a FrancyMenu object
        """
        raise NotImplementedError

    def add_message(self, text, msgType="default", title=""):
        r"""
        Input:
        * text -- a string
        * title -- a string
        * msgType -- message type
        """
        self.counter += 1
        fid = francy_id(self.counter)
        self.messages[fid] = FrancyMessage(text=text, title=title, msgType=msgType)


class FrancyMenu(FrancyOutput):
    def __init__(self, counter, encoder, title='', callback=None, menus=None,
                 messages=None):
        r"""
        Input:

        * counter -- an integer
        * encoder -- a JSON encoder
        * title -- a string
        * callback -- a Callback named tuple
        * menus -- a list of Menu named tuples
        * messages -- a list of FrancyMessage named tuples
        """
        super(FrancyMenu, self).__init__(counter, encoder)
        self.title = title
        self.callback = callback
        self.menus = {}
        for men in menus:
            self.menus[men.id] = men
        self.messages = {}
        for msg in messages:
            self.messages[msg.id] = msg


class FrancyGraph(FrancyOutput):
    r"""
    Displays a graph (ie a networkx object)

    Examples:

    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]   # list of edges
    >>> G = nx.Graph(e)
    >>> FG = FrancyGraph(G, 15, JSONEncoder())
    >>> FG.to_json()
    '{"id": "F16", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"F17": {"id": "F17", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 17, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F18": {"id": "F18", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 18, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F19": {"id": "F19", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 19, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "F20": {"id": "F20", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 20, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"F21": {"source": "F17", "weight": 1, "color": "", "target": "F18", "id": "F21"}, "F22": {"source": "F18", "weight": 1, "color": "", "target": "F19", "id": "F22"}, "F23": {"source": "F19", "weight": 1, "color": "", "target": "F20", "id": "F23"}}, "type": "undirected"}'
    """
    def __init__(self, obj, counter, encoder, graphType='undirected',
                 simulation=True, collapsed=True, drag=False, showNeighbours=False,
                 nodeType='circle', nodeSize=10, color="", highlight=True, weight=1,
                 node_options=None, link_options=None):
        super(FrancyGraph, self).__init__(counter)
        self.obj = obj
        self.graphType = graphType
        if graphType == "tree":
            self.nodeLayer = 0
        else:
            self.nodeLayer = None
        self.simulation = simulation
        self.collapsed = collapsed
        self.drag = drag
        self.showNeighbours = showNeighbours
        if nodeType not in FRANCY_NODE_TYPES:
            raise TypeError("Node type must be one of: %s" % ', '.join(FRANCY_NODE_TYPES))
        self.nodeType = nodeType  # Default value for the nodes
        self.nodeSize = int(nodeSize)  # Default value for the nodes
        self.color = color
        self.highlight = True
        self.conjugate = None
        self.weight = int(weight)  # Default value for the links
        self.node_options = node_options  # A function of the node, returning a dictionary
        self.link_options = link_options  # A function of the link, returning a dictionary
        self.compute()

    def compute(self):
        counter = self.counter
        self.id = francy_id(counter)
        if not self.graphType:
            if self.obj.is_directed():
                self.graphType = "directed"
            else:
                self.graphType = "undirected"
        self.nodes = {}
        global FRANCY_NODE_TYPES
        # Keep track of node identifiers
        match = {}
        for n in self.obj.nodes():
            counter += 1
            ident = francy_id(counter)
            match[n] = ident
            # Calculate node options
            options = {'title': '', 'parent': ''}
            # Node parent (for trees only)
            if self.graphType == 'tree' and hasattr(n, 'parent') and n.parent():
                options['parent'] = n.parent()
            # Other options
            if self.nodeType:
                options['type'] = self.nodeType  # Initialization from graph value
            if self.nodeSize:
                options['size'] = self.nodeSize  # Initialization from graph value
            if self.nodeLayer:
                options['layer'] = self.nodeLayer  # Initialization from graph value
            for parm in ['color', 'highlight', 'conjugate']:
                if hasattr(self, parm):
                    options[parm] = getattr(self, parm)  # Initialization from graph values
            if self.node_options:
                node_specifics = self.node_options(n)
                for optname in ['layer', 'conjugate']:  # Typecasting (for Sage Integers ..)
                    if optname in node_specifics:
                        node_specifics[optname] = int(node_specifics[optname])
                for optname in ['title']:
                    if optname in node_specifics:
                        node_specifics[optname] = str(node_specifics[optname])
                if 'type' in node_specifics:
                    if node_specifics['type'] not in FRANCY_NODE_TYPES:
                        raise TypeError(
                            "Node type must be one of: %s" % ', '.join(FRANCY_NODE_TYPES))
                options.update(node_specifics)
            if 'title' not in options or not options['title']:
                options['title'] = str(n)
            if 'layer' not in options or options['layer'] is None:
                options['layer'] = int(counter)  # TODO remplacer par un compteur de nœuds
            for children_list_name in ['menus', 'messages', 'callbacks']:
                if children_list_name not in options:
                    options[children_list_name] = {}
            self.nodes[ident] = GraphNode(
                id=ident,
                **options)
        # Links
        self.links = {}
        for (src, tgt) in self.obj.edges():
            counter += 1
            ident = francy_id(counter)
            # Calculate node options
            options = {}
            for parm in ['color', 'weight']:
                if hasattr(self, parm):
                    options[parm] = getattr(self, parm)
            if self.link_options:
                options.update(self.link_options(n))
            self.links[ident] = GraphEdge(
                id=ident,
                source=match[src],
                target=match[tgt],
                **options
            )
            if self.graphType == 'tree':
                tgtNode = self.nodes[match[tgt]]
                if (not hasattr(tgtNode, 'parent') or not getattr(tgtNode, 'parent')):
                    self.nodes[match[tgt]]['parent'] = self.nodes[match[src]]['id']
        """
        if self.graphType == "tree":
            # specify node parents
            for (src, tgt) in self.obj.edges:
                tgtNode = self.nodes[match[tgt]]
                if not hasattr(tgtNode, 'parent'):
                    # NB because our GraphNodes here do no act as actual graph node
                    # but only graph node JSON representation,
                    # we can change them although they are supposedly immutable.
                    self.nodes[match[tgt]]['parent'] = self.nodes[match[src]]['id']
        """
    def to_dict(self):
        res = super(FrancyGraph, self).to_dict()
        if 'graphType' in res:
            res['type'] = res['graphType']
            del res['graphType']
        for optname in [
                'nodeType', 'nodeLayer', 'nodeSize', 'color', 'highlight', 'weight']:
            if optname in res:
                del res[optname]
        return res


class FrancyMessage(FrancyOutput):
    r"""
    Displays a message

    Examples:

    >>> m = FrancyMessage(text="There are 8 levels in this Group.")
    >>> m.to_json()
    '{"id": "F1", "type": "default", "title": "", "text": "There are 8 levels in this Group."}'
    """
    def __init__(self, counter=0, encoder=None, msgType="default", title="", text=""):
        super(FrancyMessage, self).__init__(counter)
        self.type = msgType
        self.title = title
        self.text = text
