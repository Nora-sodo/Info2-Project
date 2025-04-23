from Files.graph import Graph, AddSegment
import matplotlib.pyplot as plt
import graph
from node import *
from segment import *
class Path:
    def __init__(self):
        self.nodes = []
        self.pathing_cost = []
        self.cost = 0

def AddNodeToPath (p, n):
    if n not in p.nodes:
        p.nodes.append(n)
    else:
        return -1

def ContainsNode (p, n):
    if n in p.nodes:
        return True
    else:
        return False

def CostToNode (p, orig):
    if ContainsNode(p, orig):
        for n in p.nodes:
            while n != orig:
                return Distance(p.nodes[0], orig)
    else:
        return -1


def PlotPath (g, p):
    g_cami = Graph()
    i = 0
    for n in p.nodes:
        plt.plot(n.x, n.y, 'o', color='red', markersize=5)
        # Escriu el nom dels nodes a dalt a la dreta
        plt.text(n.x + 0.5, n.y + 0.5, n.name, color='green', weight='bold', fontsize=6)
        #g_cami.nodes.append(n)
        graph.AddNode(g_cami, n)
        if i > 0:
            AddSegment(g_cami,"Segment", g_cami.nodes[i - 1].name, g_cami.nodes[i].name)
        i += 1

    # Dibuixa segments
    for s in g_cami.segments:
        graph.CreateNiceArrows(s, 'green', 'green', 'green', 0.7, 0.5, 3)
