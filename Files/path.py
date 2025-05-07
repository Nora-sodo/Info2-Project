from Files.graph import Graph, AddSegment
import matplotlib.pyplot as plt
import graph
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


def PlotPath (p, size, show_all, ax):
    g_cami = Graph()
    i = 0
    for n in p.nodes:
        plt.plot(n.x, n.y, 'o', color='red', markersize=size*5)
        # Escriu el nom dels nodes a dalt a la dreta
        if show_all:
            plt.text(n.x + size * 0.5, n.y + size * 0.5, n.name, color='blue', weight='bold', fontsize=size * 8)
        else:
            plt.text(n.x + size * 0.1, n.y + size * 0.1, n.name, color='blue', weight='bold', fontsize=size * 17)

        graph.AddNode(g_cami, n)
        if i > 0:
            AddSegment(g_cami,"Segment", g_cami.nodes[i - 1].name, g_cami.nodes[i].name)
        i += 1

    # Dibuixa segments
    for s in g_cami.segments:
        if show_all:
            graph.CreateNiceArrows(s, 'blue', 'blue', size*0.5, size*0.2, size*2, ax)
        else:
            graph.CreateNiceArrows(s, 'blue', 'blue', size * 0.2, size * 0.1, size * 2, ax)
