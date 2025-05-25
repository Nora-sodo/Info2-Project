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


def PlotPath (p, g, ax, densidad):
    g_cami = Graph()
    i = 0
    for n in g.nodes:
        plt.plot(n.x, n.y, 'o', color='gray', markersize=5)
        # Escriu el nom dels nodes a dalt a la dreta
        ax.text(n.x + 0.1 / densidad ** 2, n.y + 0.1 / densidad ** 2, n.name, color='gray', weight='bold', fontsize=6, clip_on=True)
    for n in p.nodes:
        plt.plot(n.x, n.y, 'o', color='blue', markersize=7)
        # Escriu el nom dels nodes a dalt a la dreta
        ax.text(n.x + 0.1 / densidad ** 2, n.y + 0.1 / densidad ** 2, n.name, color='black', weight='bold', fontsize=6, clip_on=True)

        graph.AddNode(g_cami, n)
        if i > 0:
            AddSegment(g_cami,"Segment", g_cami.nodes[i - 1].name, g_cami.nodes[i].name)
        i += 1

    # Dibuixa segments
    for s in g_cami.segments:
        graph.CreateNiceArrows(s, 'coral', 'coral', 0.5/densidad**2, 0.2/densidad**2, 2, ax)
        graph.MidTextSegment(s, round(s.cost, 2), 8, 'black', ax)

    ax.grid(color='red', linestyle='dashed', linewidth=0.5)  # Dibuixa una graella pel fons
