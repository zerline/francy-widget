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


def canvas_id():
    r"""
    A random string to serve as a random canvas identifier

    Test:

    >>> a = canvas_id()
    >>> len(a)
    32
    """
    from hashlib import md5
    from random import randint
    return md5(str(randint(1, 100)).encode('utf8')).hexdigest()


def francy_id(base_id='', output_type='node', counter=0):
    r"""
    Id for Francy outputs.

    Input:

    * base_id -- a string
    * output_type -- a string
    * counter -- an integer

    Test:

    >>> francy_id("mycanvas", 'menu', 42)
    'mycanvas_menu42'
    >>> len(francy_id(None, None, 42424))
    42
    """
    if not base_id:
        base_id = canvas_id()
    if output_type == 'canvas':
        return base_id
    return "%s_%s%d" % (base_id, output_type, counter)


def default_id(counter):
    r"""
    Default id (francy-style) for Francy outputs.

    Test:

    >>> default_id(42)
    'F42'
    """
    return "F%d" % counter


class FrancyOutput:
    r"""
    A base class for Francy JSON representable objects having an id as required attribute.
    """

    def __init__(self, base_id=None, output_type=None, counter=0, encoder=None):
        r"""
        Input:

        * counter -- an integer
        * encoder -- a JSON encoder

        Test:

        >>> o = FrancyOutput('mycanvas', 'node', 3)
        >>> o.encoder.__class__
        <class 'json.encoder.JSONEncoder'>
        >>> o.id
        'mycanvas_node4'
        """
        counter += 1
        self.counter = counter
        if not encoder:
            encoder = JSONEncoder()
        self.encoder = encoder
        self.obj = None
        if output_type: # Do not give an id to the adapter object
            self.id = francy_id(base_id, output_type, counter)

    def to_dict(self):
        r"""
        Strip out unrequired attributes
        before passing the object to its JSON encoder.

        Test:

        >>> o = FrancyOutput('mycanvas', 'node', 3)
        >>> o.to_dict()
        {'id': 'mycanvas_node4'}
        """
        d = copy(self.__dict__)
        del d['counter']
        del d['encoder']
        for k in ['obj', 'conjugate', 'node_options', 'link_options', 'is_method']:
            if k in d:
                # A math value or a function
                del d[k]
        for k in ['canvas', 'graph', 'callback']:
            if k in d and d[k] and not isinstance(d[k], dict):
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
        r"""
        JSON serialization.

        Test:

        >>> o = FrancyOutput('mycanvas', 'node', 3)
        >>> o.to_json()
        '{"id": "mycanvas_node4"}'
        """
        return self.encoder.encode(self.to_dict())


class FrancyAdapter(FrancyOutput):
    r"""
    An adapter for representing a graph in a Francy Widget

    Examples:

    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G1 = nx.Graph(e)
    >>> a = FrancyAdapter()
    >>> a.to_dict(G1, title="Example Undirected Graph", base_id="mycanvas")
    {'version': '1.1.3', 'mime': 'application/vnd.francy+json', 'canvas': {'id': 'mycanvas', 'title': 'Example Undirected Graph', 'width': 800.0, 'height': 100.0, 'zoomToFit': True, 'texTypesetting': False, 'graph': {'id': 'mycanvas_graph2', 'simulation': True, 'collapsed': True, 'drag': False, 'showNeighbours': False, 'nodes': {'mycanvas_node3': {'id': 'mycanvas_node3', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '1', 'color': '', 'highlight': True, 'layer': 3, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}, 'mycanvas_node4': {'id': 'mycanvas_node4', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '2', 'color': '', 'highlight': True, 'layer': 4, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}, 'mycanvas_node5': {'id': 'mycanvas_node5', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '3', 'color': '', 'highlight': True, 'layer': 5, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}, 'mycanvas_node6': {'id': 'mycanvas_node6', 'x': 0, 'y': 0, 'type': 'circle', 'size': 10, 'title': '4', 'color': '', 'highlight': True, 'layer': 6, 'parent': '', 'menus': {}, 'messages': {}, 'callbacks': {}}}, 'links': {'mycanvas_edge7': {'source': 'mycanvas_node3', 'weight': 1, 'color': '', 'target': 'mycanvas_node4', 'id': 'mycanvas_edge7'}, 'mycanvas_edge8': {'source': 'mycanvas_node4', 'weight': 1, 'color': '', 'target': 'mycanvas_node5', 'id': 'mycanvas_edge8'}, 'mycanvas_edge9': {'source': 'mycanvas_node5', 'weight': 1, 'color': '', 'target': 'mycanvas_node6', 'id': 'mycanvas_edge9'}}, 'type': 'undirected'}, 'menus': {}, 'messages': {}}}
    """
    def __init__(self, version='1.1.3', counter=-1):
        super(FrancyAdapter, self).__init__(None, None, counter)
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = FrancyCanvas()

    def to_dict(self, obj, **kws):
        r"""
        Test:

        >>> import networkx as nx
        >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
        >>> G1 = nx.Graph(e)
        >>> a = FrancyAdapter()
        >>> def node_options(n):
        ...   options = {}
        ...   options['type'] = 'square'
        ...   options['modal_menus'] = [{
        ...     'title': 'cardinality',
        ...     'funcname': 'cardinality',
        ...     'is_method': True
        ...   }]
        ...   return options
        >>> a.to_dict(G1, base_id='mycanvas', title="Example Undirected Graph", node_options=node_options)
        {'version': '1.1.3', 'mime': 'application/vnd.francy+json', 'canvas': {'id': 'mycanvas', 'title': 'Example Undirected Graph', 'width': 800.0, 'height': 100.0, 'zoomToFit': True, 'texTypesetting': False, 'graph': {'id': 'mycanvas_graph2', 'simulation': True, 'collapsed': True, 'drag': False, 'showNeighbours': False, 'nodes': {'mycanvas_node3': {'id': 'mycanvas_node3', 'x': 0, 'y': 0, 'type': 'square', 'size': 10, 'title': '1', 'color': '', 'highlight': True, 'layer': 3, 'parent': '', 'menus': {'mycanvas_menu4': {'id': 'mycanvas_menu4', 'title': 'cardinality', 'callback': {'id': 'mycanvas_callback4', 'funcname': 'cardinality', 'trigger': 'click', 'knownArgs': [], 'requiredArgs': {}}, 'menus': {}, 'messages': {}}}, 'messages': {}, 'callbacks': {}}, 'mycanvas_node4': {'id': 'mycanvas_node4', 'x': 0, 'y': 0, 'type': 'square', 'size': 10, 'title': '2', 'color': '', 'highlight': True, 'layer': 4, 'parent': '', 'menus': {'mycanvas_menu5': {'id': 'mycanvas_menu5', 'title': 'cardinality', 'callback': {'id': 'mycanvas_callback5', 'funcname': 'cardinality', 'trigger': 'click', 'knownArgs': [], 'requiredArgs': {}}, 'menus': {}, 'messages': {}}}, 'messages': {}, 'callbacks': {}}, 'mycanvas_node5': {'id': 'mycanvas_node5', 'x': 0, 'y': 0, 'type': 'square', 'size': 10, 'title': '3', 'color': '', 'highlight': True, 'layer': 5, 'parent': '', 'menus': {'mycanvas_menu6': {'id': 'mycanvas_menu6', 'title': 'cardinality', 'callback': {'id': 'mycanvas_callback6', 'funcname': 'cardinality', 'trigger': 'click', 'knownArgs': [], 'requiredArgs': {}}, 'menus': {}, 'messages': {}}}, 'messages': {}, 'callbacks': {}}, 'mycanvas_node6': {'id': 'mycanvas_node6', 'x': 0, 'y': 0, 'type': 'square', 'size': 10, 'title': '4', 'color': '', 'highlight': True, 'layer': 6, 'parent': '', 'menus': {'mycanvas_menu7': {'id': 'mycanvas_menu7', 'title': 'cardinality', 'callback': {'id': 'mycanvas_callback7', 'funcname': 'cardinality', 'trigger': 'click', 'knownArgs': [], 'requiredArgs': {}}, 'menus': {}, 'messages': {}}}, 'messages': {}, 'callbacks': {}}}, 'links': {'mycanvas_edge7': {'source': 'mycanvas_node3', 'weight': 1, 'color': '', 'target': 'mycanvas_node4', 'id': 'mycanvas_edge7'}, 'mycanvas_edge8': {'source': 'mycanvas_node4', 'weight': 1, 'color': '', 'target': 'mycanvas_node5', 'id': 'mycanvas_edge8'}, 'mycanvas_edge9': {'source': 'mycanvas_node5', 'weight': 1, 'color': '', 'target': 'mycanvas_node6', 'id': 'mycanvas_edge9'}}, 'type': 'undirected'}, 'menus': {}, 'messages': {}}}
        """
        canvas_kws = {}
        canvas_kws['title'] = "A Francy graph representation"  # default title
        for k in ['title', 'width', 'height', 'zoomToFit', 'texTypesetting', 'base_id']:
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
        if obj:
            self.canvas.set_graph(obj, **kws)
        d = super(FrancyAdapter, self).to_dict()
        return d

    def to_json(self, obj, **kws):
        r"""
        Test:

        >>> import networkx as nx
        >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
        >>> G1 = nx.Graph(e)
        >>> a = FrancyAdapter()
        >>> m = FrancyMenu.from_dict('mycanvas', 1, {'title': 'My function call'})
        >>> a.to_json(G1, base_id='mycanvas', title="With menu", menus=[m])
        '{"version": "1.1.3", "mime": "application/vnd.francy+json", "canvas": {"id": "mycanvas", "title": "With menu", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "mycanvas_graph2", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node3": {"id": "mycanvas_node3", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node4": {"id": "mycanvas_node4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node5": {"id": "mycanvas_node5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node6": {"id": "mycanvas_node6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 6, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge7": {"source": "mycanvas_node3", "weight": 1, "color": "", "target": "mycanvas_node4", "id": "mycanvas_edge7"}, "mycanvas_edge8": {"source": "mycanvas_node4", "weight": 1, "color": "", "target": "mycanvas_node5", "id": "mycanvas_edge8"}, "mycanvas_edge9": {"source": "mycanvas_node5", "weight": 1, "color": "", "target": "mycanvas_node6", "id": "mycanvas_edge9"}}, "type": "undirected"}, "menus": {"mycanvas_menu2": {"id": "mycanvas_menu2", "title": "My function call", "callback": {"id": "mycanvas_callback2", "funcname": "Unknown", "trigger": "click", "knownArgs": ["python"], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}}}'
        >>> def node_options(n):
        ...   options = {}
        ...   options['type'] = 'square'
        ...   options['modal_menus'] = [{
        ...     'title': 'cardinality',
        ...     'funcname': 'cardinality',
        ...     'is_method': True
        ...   }]
        ...   return options
        >>> a.to_json(G1, base_id='mycanvas', title="Example Undirected Graph", node_options=node_options)
        '{"version": "1.1.3", "mime": "application/vnd.francy+json", "canvas": {"id": "mycanvas", "title": "Example Undirected Graph", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "mycanvas_graph2", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node3": {"id": "mycanvas_node3", "x": 0, "y": 0, "type": "square", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {"mycanvas_menu4": {"id": "mycanvas_menu4", "title": "cardinality", "callback": {"id": "mycanvas_callback4", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node4": {"id": "mycanvas_node4", "x": 0, "y": 0, "type": "square", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {"mycanvas_menu5": {"id": "mycanvas_menu5", "title": "cardinality", "callback": {"id": "mycanvas_callback5", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node5": {"id": "mycanvas_node5", "x": 0, "y": 0, "type": "square", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {"mycanvas_menu6": {"id": "mycanvas_menu6", "title": "cardinality", "callback": {"id": "mycanvas_callback6", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node6": {"id": "mycanvas_node6", "x": 0, "y": 0, "type": "square", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 6, "parent": "", "menus": {"mycanvas_menu7": {"id": "mycanvas_menu7", "title": "cardinality", "callback": {"id": "mycanvas_callback7", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge7": {"source": "mycanvas_node3", "weight": 1, "color": "", "target": "mycanvas_node4", "id": "mycanvas_edge7"}, "mycanvas_edge8": {"source": "mycanvas_node4", "weight": 1, "color": "", "target": "mycanvas_node5", "id": "mycanvas_edge8"}, "mycanvas_edge9": {"source": "mycanvas_node5", "weight": 1, "color": "", "target": "mycanvas_node6", "id": "mycanvas_edge9"}}, "type": "undirected"}, "menus": {}, "messages": {}}}'
        """
        return self.encoder.encode(self.to_dict(obj, **kws))


class FrancyCanvas(FrancyOutput):
    r"""
    Displays a canvas

    Examples:

    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]  # list of edges
    >>> G = nx.Graph(e)
    >>> FC = FrancyCanvas(base_id='mycanvas')
    >>> FC.set_graph(G)
    >>> FC.to_json()
    '{"id": "mycanvas", "title": "My Canvas", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "mycanvas_graph2", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node3": {"id": "mycanvas_node3", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node4": {"id": "mycanvas_node4", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node5": {"id": "mycanvas_node5", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node6": {"id": "mycanvas_node6", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 6, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge7": {"source": "mycanvas_node3", "weight": 1, "color": "", "target": "mycanvas_node4", "id": "mycanvas_edge7"}, "mycanvas_edge8": {"source": "mycanvas_node4", "weight": 1, "color": "", "target": "mycanvas_node5", "id": "mycanvas_edge8"}, "mycanvas_edge9": {"source": "mycanvas_node5", "weight": 1, "color": "", "target": "mycanvas_node6", "id": "mycanvas_edge9"}}, "type": "undirected"}, "menus": {}, "messages": {}}'
    """
    def __init__(self, counter=0, encoder=None, title="My Canvas", width=800, height=100,
                 zoomToFit=True, texTypesetting=False, **kws):
        base_id = None
        if 'base_id' in kws: # Useful for testing
            base_id = kws['base_id']
        super(FrancyCanvas, self).__init__(base_id, 'canvas', counter)
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
        >>> FC = FrancyCanvas(base_id='mycanvas')
        >>> FC.set_graph(G, node_options=node_options)
        >>> FC.to_json()
        '{"id": "mycanvas", "title": "My Canvas", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": {"id": "mycanvas_graph2", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node3": {"id": "mycanvas_node3", "x": 0, "y": 0, "type": "square", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {"mycanvas_menu4": {"id": "mycanvas_menu4", "title": "cardinality", "callback": {"id": "mycanvas_callback4", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node4": {"id": "mycanvas_node4", "x": 0, "y": 0, "type": "square", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {"mycanvas_menu5": {"id": "mycanvas_menu5", "title": "cardinality", "callback": {"id": "mycanvas_callback5", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node5": {"id": "mycanvas_node5", "x": 0, "y": 0, "type": "square", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {"mycanvas_menu6": {"id": "mycanvas_menu6", "title": "cardinality", "callback": {"id": "mycanvas_callback6", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node6": {"id": "mycanvas_node6", "x": 0, "y": 0, "type": "square", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 6, "parent": "", "menus": {"mycanvas_menu7": {"id": "mycanvas_menu7", "title": "cardinality", "callback": {"id": "mycanvas_callback7", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge7": {"source": "mycanvas_node3", "weight": 1, "color": "", "target": "mycanvas_node4", "id": "mycanvas_edge7"}, "mycanvas_edge8": {"source": "mycanvas_node4", "weight": 1, "color": "", "target": "mycanvas_node5", "id": "mycanvas_edge8"}, "mycanvas_edge9": {"source": "mycanvas_node5", "weight": 1, "color": "", "target": "mycanvas_node6", "id": "mycanvas_edge9"}}, "type": "undirected"}, "menus": {}, "messages": {}}'
        """
        self.graph = FrancyGraph(graph, self.id, self.counter, **kws)

    def add_menu(self, menu):
        r"""
        Input:

        * menu -- a FrancyMenu object

        Test:

        >>> FC = FrancyCanvas(base_id='mycanvas')
        >>> m = FrancyMenu.from_dict('mycanvas', 1, {'title': 'My function call'})
        >>> FC.add_menu(m)
        >>> FC.to_json()
        '{"id": "mycanvas", "title": "My Canvas", "width": 800.0, "height": 100.0, "zoomToFit": true, "texTypesetting": false, "graph": null, "menus": {"mycanvas_menu2": {"id": "mycanvas_menu2", "title": "My function call", "callback": {"id": "mycanvas_callback2", "funcname": "Unknown", "trigger": "click", "knownArgs": ["python"], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}}'
        """
        self.menus[menu.id] = menu

    def add_message(self, text, msgType="default", title=""):
        r"""
        Input:
        * text -- a string
        * title -- a string
        * msgType -- message type
        """
        self.counter += 1
        fid = francy_id(self.id, 'message', self.counter)
        self.messages[fid] = FrancyMessage(text=text, title=title, msgType=msgType)


class FrancyCallback(FrancyOutput):
    r"""
    A Callback for a menu entry.

    Test:

    >>> c = FrancyCallback('mycanvas', 1, 'cardinality', knownArgs=["<object>", "{1,2,3}"])
    >>> c.funcname
    'cardinality'
    >>> c.trigger
    'click'
    >>> c.to_json()
    '{"id": "mycanvas_callback2", "funcname": "cardinality", "trigger": "click", "knownArgs": ["<object>", "{1,2,3}"], "requiredArgs": {}}'
    """
    def __init__(self, canvas_id=None, counter=0, funcname=None, is_method=False, trigger="click", knownArgs=[], requiredArgs={}):
        r"""
        Input:

        * canvas_id -- a string
        * funcname -- a string
        * is_method -- a boolean
        * counter -- an integer to count callbacks
        * funcname -- a string
        * trigger -- a string
        * knownArgs -- a list of strings
        * requiredArgs -- a dict
        """
        super(FrancyCallback, self).__init__(canvas_id, 'callback', counter)
        self.funcname = funcname
        self.is_method = is_method
        self.trigger = trigger
        self.knownArgs = knownArgs
        self.requiredArgs = requiredArgs


class FrancyMenu(FrancyOutput):
    def __init__(self, canvas_id=None, counter=0, title='', callback=None, menus=[],
                 messages=[]):
        r"""
        Input:

        * canvas_id -- a string
        * counter -- an integer to count menus
        * title -- a string
        * callback -- a FrancyCallback object
        * menus -- a list of FrancyMenu objects
        * messages -- a list of FrancyMessage objects

        Test:

        >>> c = FrancyCallback('mycanvas', 1, 'cardinality', knownArgs=["<object>", "{1,2,3}"])
        >>> m = FrancyMenu('mycanvas', 1, 'cardinality', c)
        >>> m.to_json()
        '{"id": "mycanvas_menu2", "title": "cardinality", "callback": {"id": "mycanvas_callback2", "funcname": "cardinality", "trigger": "click", "knownArgs": ["python", "<object>", "{1,2,3}"], "requiredArgs": {}}, "menus": {}, "messages": {}}'
        >>> c1 = FrancyCallback('mycanvas', 2, None, knownArgs=["SymmetricGroup(4)"])
        >>> m1 = FrancyMenu('mycanvas', 3, 'All Subgroups', c1)
        >>> m1.to_json()
        '{"id": "mycanvas_menu4", "title": "All Subgroups", "callback": {"id": "mycanvas_callback3", "funcname": null, "trigger": "click", "knownArgs": ["python", "SymmetricGroup(4)"], "requiredArgs": {}}, "menus": {}, "messages": {}}'
        >>> m2 = FrancyMenu('mycanvas', 4, 'Subgroup Lattice')
        >>> m2.to_json()
        '{"id": "mycanvas_menu5", "title": "Subgroup Lattice", "callback": null, "menus": {}, "messages": {}}'
        """
        super(FrancyMenu, self).__init__(canvas_id, 'menu', counter)
        self.title = title
        self.callback = callback
        self.menus = {}
        for men in menus:
            self.menus[men.id] = men
        self.messages = {}
        for msg in messages:
            self.messages[msg.id] = msg

    @classmethod
    def from_dict(cls, canvas_id='', counter=0, data={}):
        r"""
        Create a Francy menu

        Input:

        * data : a dictionary of all menu and associated callback attributes

        Test:

        >>> m = FrancyMenu.from_dict('mycanvas', 1, {'title': 'My function call'})
        >>> m.to_json()
        '{"id": "mycanvas_menu2", "title": "My function call", "callback": {"id": "mycanvas_callback2", "funcname": "Unknown", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}'
        """
        try:
            title = data['title']
        except:
            raise KeyError("Missing Title")
        if 'funcname' in data:
            funcname = data["funcname"]
        else:
            funcname = "Unknown"
        if 'is_method' in data:
            is_method = data['is_method']
        else:
            is_method = False
        if 'known_args' in data:
            known_args = data['known_args']
        else:
            known_args = []
        if 'required_args' in data:
            required_args = data['required_args']
        else:
            required_args = {}
        return cls(canvas_id, counter, title=title, callback=FrancyCallback(
            canvas_id, counter, funcname=funcname, is_method=is_method, knownArgs=known_args,
            requiredArgs=required_args)
        )


class FrancyGraph(FrancyOutput):
    r"""
    Displays a graph (ie a networkx object)

    Examples:

    >>> import networkx as nx
    >>> e = [(1, 2), (2, 3), (3, 4)]   # list of edges
    >>> G = nx.Graph(e)
    >>> FG = FrancyGraph(G, 'mycanvas', 15)
    >>> FG.to_json()
    '{"id": "mycanvas_graph16", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node17": {"id": "mycanvas_node17", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 17, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node18": {"id": "mycanvas_node18", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 18, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node19": {"id": "mycanvas_node19", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 19, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}, "mycanvas_node20": {"id": "mycanvas_node20", "x": 0, "y": 0, "type": "circle", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 20, "parent": "", "menus": {}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge21": {"source": "mycanvas_node17", "weight": 1, "color": "", "target": "mycanvas_node18", "id": "mycanvas_edge21"}, "mycanvas_edge22": {"source": "mycanvas_node18", "weight": 1, "color": "", "target": "mycanvas_node19", "id": "mycanvas_edge22"}, "mycanvas_edge23": {"source": "mycanvas_node19", "weight": 1, "color": "", "target": "mycanvas_node20", "id": "mycanvas_edge23"}}, "type": "undirected"}'
    """
    def __init__(self, obj, canvas_id=None, counter=0, graphType='undirected',
                 simulation=True, collapsed=True, drag=False, showNeighbours=False,
                 nodeType='circle', nodeSize=10, color="", highlight=True, weight=1,
                 node_options=None, link_options=None):
        super(FrancyGraph, self).__init__(canvas_id, 'graph', counter)
        self.canvas_id = canvas_id
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
        r"""
        Build graph nodes and edges.

        Test:

        >>> from networkx import Graph
        >>> G = Graph([(1, 2), (2, 3), (3, 4)])
        >>> def node_options(n):
        ...   options = {}
        ...   options['type'] = 'diamond'
        ...   options['modal_menus'] = [{
        ...     'title': 'cardinality',
        ...     'funcname': 'cardinality',
        ...     'is_method': True
        ...   }]
        ...   return options
        >>> g = FrancyGraph(G, canvas_id='mycanvas', node_options=node_options)
        >>> g.compute()
        >>> g.to_json()
        '{"id": "mycanvas_graph1", "simulation": true, "collapsed": true, "drag": false, "showNeighbours": false, "nodes": {"mycanvas_node2": {"id": "mycanvas_node2", "x": 0, "y": 0, "type": "diamond", "size": 10, "title": "1", "color": "", "highlight": true, "layer": 2, "parent": "", "menus": {"mycanvas_menu3": {"id": "mycanvas_menu3", "title": "cardinality", "callback": {"id": "mycanvas_callback3", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node3": {"id": "mycanvas_node3", "x": 0, "y": 0, "type": "diamond", "size": 10, "title": "2", "color": "", "highlight": true, "layer": 3, "parent": "", "menus": {"mycanvas_menu4": {"id": "mycanvas_menu4", "title": "cardinality", "callback": {"id": "mycanvas_callback4", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node4": {"id": "mycanvas_node4", "x": 0, "y": 0, "type": "diamond", "size": 10, "title": "3", "color": "", "highlight": true, "layer": 4, "parent": "", "menus": {"mycanvas_menu5": {"id": "mycanvas_menu5", "title": "cardinality", "callback": {"id": "mycanvas_callback5", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}, "mycanvas_node5": {"id": "mycanvas_node5", "x": 0, "y": 0, "type": "diamond", "size": 10, "title": "4", "color": "", "highlight": true, "layer": 5, "parent": "", "menus": {"mycanvas_menu6": {"id": "mycanvas_menu6", "title": "cardinality", "callback": {"id": "mycanvas_callback6", "funcname": "cardinality", "trigger": "click", "knownArgs": [], "requiredArgs": {}}, "menus": {}, "messages": {}}}, "messages": {}, "callbacks": {}}}, "links": {"mycanvas_edge6": {"source": "mycanvas_node2", "weight": 1, "color": "", "target": "mycanvas_node3", "id": "mycanvas_edge6"}, "mycanvas_edge7": {"source": "mycanvas_node3", "weight": 1, "color": "", "target": "mycanvas_node4", "id": "mycanvas_edge7"}, "mycanvas_edge8": {"source": "mycanvas_node4", "weight": 1, "color": "", "target": "mycanvas_node5", "id": "mycanvas_edge8"}}, "type": "undirected"}'
        """
        counter = self.counter
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
            ident = francy_id(self.canvas_id, 'node', counter)
            match[n] = ident
            # Calculate node options
            options = {'title': '', 'parent': ''}
            menus = None
            messages = None
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
                if 'modal_menus' in node_specifics:
                    menus = {}
                    for m in node_specifics['modal_menus']:
                        men = FrancyMenu.from_dict(self.canvas_id, counter, data=m)
                        menus[men.id] = men.to_dict()
                    options['menus'] = menus
                    del node_specifics['modal_menus']
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
            ident = francy_id(self.canvas_id, 'edge', counter)
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
                'nodeType', 'nodeLayer', 'nodeSize', 'color', 'highlight', 'weight', 'canvas_id']:
            if optname in res:
                del res[optname]
        return res


class FrancyMessage(FrancyOutput):
    r"""
    Displays a message

    Examples:

    >>> m = FrancyMessage("mycanvas", text="There are 8 levels in this Group.")
    >>> m.to_json()
    '{"id": "mycanvas_message1", "type": "default", "title": "", "text": "There are 8 levels in this Group."}'
    """
    def __init__(self, canvas_id=None, counter=0, msgType="default", title="", text=""):
        super(FrancyMessage, self).__init__(canvas_id, 'message', counter)
        self.type = msgType
        self.title = title
        self.text = text
