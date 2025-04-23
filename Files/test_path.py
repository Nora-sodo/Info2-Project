import matplotlib.pyplot as plt

from graph import *

def CreateGraph_1 (): # Crea el Graph d'exemple
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddDobleSegment(G, "AB","A","B")
    AddDobleSegment(G, "AE","A","E")
    AddDobleSegment(G, "AK","A","K")
    AddDobleSegment(G, "BC","B","C")
    AddDobleSegment(G, "BF","B","F")
    AddDobleSegment(G, "BK", "B", "K")
    AddDobleSegment(G, "BG", "B", "G")
    AddDobleSegment(G, "CD", "C", "D")
    AddDobleSegment(G, "CG", "C", "G")
    AddDobleSegment(G, "DG", "D", "G")
    AddDobleSegment(G, "DH", "D", "H")
    AddDobleSegment(G, "DI", "D", "I")
    AddDobleSegment(G, "EF", "E", "F")
    AddDobleSegment(G, "FL", "F", "L")
    AddDobleSegment(G, "GF", "G", "F")
    AddDobleSegment(G, "GH", "G", "H")
    AddDobleSegment(G, "IJ", "I", "J")
    AddDobleSegment(G, "KL", "K", "L")

    return G

G = CreateGraph_1()
P = FindShortestPath(G,'A','I')
PlotPath(G, P)
plt.show()