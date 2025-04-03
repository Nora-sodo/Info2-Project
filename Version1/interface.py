import tkinter as tk
from graph import *

# Crear Graph exemple
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
    AddSegment(G, "AB","A","B")
    AddSegment(G, "AE","A","E")
    AddSegment(G, "AK","A","K")
    AddSegment(G, "BA","B","A")
    AddSegment(G, "BC","B","C")
    AddSegment(G, "BF","B","F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")
    return G

# Crear Graph inventat
def CreateGraph_2 ():
    G = Graph()
    AddNode(G, Node("A", 9, 2))
    AddNode(G, Node("B", 20, 17))
    AddNode(G, Node("C", 3, 6))
    AddNode(G, Node("D", 19, 7))
    AddNode(G, Node("E", -1, 20))
    AddNode(G, Node("F", 8, 15))
    AddNode(G, Node("G", 7, 7))
    AddNode(G, Node("H", 12, 8))
    AddNode(G, Node("I", 19, 1))
    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")

    return G

windowGraph = Graph()

# Crear finestra principal
root = tk.Tk()
root.title("Graph")
root.geometry("650x450")

# Crear una etiqueta
title = tk.Label(root, text="Main options:", font=("Arial", 10, "bold"))
title.pack(pady=10)  # Empaqueta el widget con espacio vertical

# FUNCIONS BOTONS:
# Funcio per quan exampleButton pressionat
def ShowExampleButtonClick():
    global windowGraph
    windowGraph = CreateGraph_1()
    Plot(windowGraph)
# Funcio per quan inventedButton pressionat
def ShowInventedButtonClick():
    global windowGraph
    windowGraph = CreateGraph_2()
    Plot(windowGraph)
# Funcio per quan loadButton pressionat
def LoadButtonClick():
    global windowGraph
    windowGraph = GraphFile(fileName.get())
    Plot(windowGraph)

# Funcio per quan nButton pressionat
def NButtonClick():
    if nButton.cget('relief') == 'sunken':
        # Si está presionado, lo dejamos normal
        Plot(windowGraph)
        nButton.config(relief="raised", bg="lightblue",text="Node Graph: OFF")

    else:
        # Si está normal, lo dejamos presionado
        PlotNode(windowGraph, nodeSelect.get())
        nButton.config(relief="sunken", bg="gray64",text="Node Graph: ON")

def AddNButtonClick():
    node = Node(nameSelect_n.get(),float(xSelect_n.get()),float(ySelect_n.get()))
    AddNode(windowGraph, node)
    if not nButton.cget('relief') == 'sunken':
        Plot(windowGraph)
    else:
        PlotNode(windowGraph, nodeSelect.get())

def AddSButtonClick():
    AddSegment(windowGraph, nameSelect_s.get(), xSelect_s.get(), ySelect_s.get())
    if not nButton.cget('relief') == 'sunken':
        Plot(windowGraph)
    else:
        PlotNode(windowGraph, nodeSelect.get())

# Crear un botons
showExampleButton = tk.Button(root, bg="lightblue", text="Example Graph", command=ShowExampleButtonClick)
showExampleButton.pack(pady=10)

showInventedButton = tk.Button(root, bg="lightblue", text="Invented Graph", command=ShowInventedButtonClick)
showInventedButton.pack(pady=10)

#Creacio de frame per contenir entrada i boto
loadFrame = tk.Frame(root)
loadFrame.pack(pady=10)
infLabel1 = tk.Label(loadFrame, text="File path:", font=("Arial", 7, "bold"))
loadButton = tk.Button(loadFrame, bg="lightblue", text="Load File", command=LoadButtonClick)
fileName = tk.Entry(loadFrame, width=30)
infLabel1.pack(side="left", padx=3)
fileName.pack(side="left", padx=3)
loadButton.pack(side="left", padx=3)

nFrame = tk.Frame(root)
nFrame.pack(pady=10)
infLabel2 = tk.Label(nFrame, text="Node name:", font=("Arial", 7, "bold"))
nButton = tk.Button(nFrame, bg="lightblue", text="Node Graph: OFF", command=NButtonClick)
nodeSelect = tk.Entry(nFrame, width=10)
infLabel2.pack(side="left", padx=3)
nodeSelect.pack(side="left", padx=5)
nButton.pack(side="left", padx=5)

#Creacio fila per crear node
nodeFrame = tk.Frame(root)
nodeFrame.pack(pady=10)
infNameLabel_n = tk.Label(nodeFrame, text="Node name:", font=("Arial", 7, "bold"))
nameSelect_n = tk.Entry(nodeFrame, width=10)
infXLabel_n = tk.Label(nodeFrame, text="X:", font=("Arial", 7, "bold"))
xSelect_n = tk.Entry(nodeFrame, width=10)
infYLabel_n = tk.Label(nodeFrame, text="Y:", font=("Arial", 7, "bold"))
ySelect_n = tk.Entry(nodeFrame, width=10)
nodeButton = tk.Button(nodeFrame, bg="lightblue", text="Create Node", command=AddNButtonClick)
infNameLabel_n.pack(side="left", padx=2)
nameSelect_n.pack(side="left", padx=4)
infXLabel_n.pack(side="left", padx=2)
xSelect_n.pack(side="left", padx=4)
infYLabel_n.pack(side="left", padx=2)
ySelect_n.pack(side="left", padx=4)
nodeButton.pack(side="left", padx=5)

#Creacio fila per crear segment
sFrame = tk.Frame(root)
sFrame.pack(pady=10)
infNameLabel_s = tk.Label(sFrame, text="Segment name:", font=("Arial", 7, "bold"))
nameSelect_s = tk.Entry(sFrame, width=10)
infXLabel_s = tk.Label(sFrame, text="Origin:", font=("Arial", 7, "bold"))
xSelect_s = tk.Entry(sFrame, width=10)
infYLabel_s = tk.Label(sFrame, text="Destiny:", font=("Arial", 7, "bold"))
ySelect_s = tk.Entry(sFrame, width=10)
sButton = tk.Button(sFrame, bg="lightblue", text="Create Segment", command=AddSButtonClick)
infNameLabel_s.pack(side="left", padx=2)
nameSelect_s.pack(side="left", padx=4)
infXLabel_s.pack(side="left", padx=2)
xSelect_s.pack(side="left", padx=4)
infYLabel_s.pack(side="left", padx=2)
ySelect_s.pack(side="left", padx=4)
sButton.pack(side="left", padx=5)

# Executar finestra
root.mainloop()
