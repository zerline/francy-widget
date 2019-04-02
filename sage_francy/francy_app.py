# -*- coding: utf-8 -*-
r"""
A Francy Widget for the Jupyter Notebook.

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from json import JSONEncoder

class FrancyApp:
    r"""
    To be displayed in a Francy Widget
    """
    def __init__(self, version='1.1.1'):
        self.version = version
        self.mime = "application/vnd.francy+json"
        self.canvas = None

    def add_canvas(self, c):
        self.canvas = c

    def to_json(self, encoder):
        if not encoder:
            encoder = JSONEncoder()
        return encoder.encode(self.__dict__)

class FrancyCanvas:
    r"""
    Displays a canvas
    """
    def __init__(self, title="My Canvas", width=800, height=100, zoomToFit=True, texTypesetting=False):
        self.title = title
        self.width = width
        self.height = height
        self.zoomToFit = zommToFit
        self.texTypesetting = texTypesetting
        self.menus = []
        self.graph = None
        self.chart = None
        self.messages = []

    def to_json(self, encoder):
        return encoder.encode(self.__dict__)

class FrancyMenu:
    def to_json(self, encoder):
        return encoder.encode(self.__dict__)

class FrancyGraph:
    r"""
    Displays a graph (ie a Sage object)
    """
    def __init__(self, graph, simulation=True, collapsed=True, drag=False, showNeighbours=False):
        self.graph = graph
        self.simulation = simulation
        self.collapsed = collapsed
        self.drag = drag
        self.showNeighbours = showNeighbours

    def to_json(self, encoder):
        return encoder.encode(self.__dict__)

class FrancyChart:
    r"""
    Displays a chart (ie a Sage object)
    """
    def __init__(self, chart):
        self.chart = chart

    def to_json(self, encoder):
        return encoder.encode(self.__dict__)

class Message:
    r"""
    Displays a message
    """
    def __init__(self, msgtype='default', title='', text=''):
        self.msgtype = msgtype
        self.title = title
        self.text = text

    def to_json(self, encoder):
        return encoder.encode(self.__dict__)
