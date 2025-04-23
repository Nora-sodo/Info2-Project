import tkinter as tk
from PIL import Image, ImageTk
from graph import *
from AirSpace import *

#####################
# FUNCIONS PROPIES: #
#####################
# Canvia la imatge grafico.png al grafic que toca
def GraphChange():
    imagenGrafico = Image.open("grafico.png")  # Reemplaza con tu nueva imagen
    nuevaImagen = imagenGrafico.resize((500, 400))

    # Convertir la imagen a un formato compatible con Tkinter
    nueva_imagen_tk = ImageTk.PhotoImage(nuevaImagen)

    # Actualizar la imagen del Label
    label_imagen.config(image=nueva_imagen_tk)
    label_imagen.image = nueva_imagen_tk

windowGraph = Graph()

# Passa de Airspace a Graph
def AirspaceToGraph(g, a):
    for n in a.nav_points:
        AddNode(g, Node(n.name,n.lon,n.lat))
    for s in a.nav_segments:
        AddSegment(g, "Segment", FindNodeName(g, s.o_number), FindNodeName(g, s.d_number))
        print(FindNodeName(g, s.o_number).name, FindNodeName(g, s.d_number).name)

######################################################################################################


##############################
# FUNCIONS PER CREAR GRAFICS #
##############################
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
def CreateGraph_2():
    G = Graph()
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))
    AddDobleSegment(G, "AB", "A", "B")
    AddDobleSegment(G, "AE", "A", "E")
    AddDobleSegment(G, "AK", "A", "K")
    AddDobleSegment(G, "BC", "B", "C")
    AddDobleSegment(G, "BF", "B", "F")
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
    AddDobleSegment(G, "AC", "A", "C")
    AddDobleSegment(G, "JD", "J", "D")
    AddDobleSegment(G, "FH", "F", "H")

    return G

# Crear graph de catalunya
def CreateCatGraph():
    G = Graph()

    air_space = AirSpace()
    air_space.nav_points = NavPointsFromFile("Cat_nav.txt")
    air_space.nav_segments = NavSegmentsFromFile("Cat_seg.txt")
    air_space.nav_airports = NavAirportsFromFile("Cat_aer.txt")

    AirspaceToGraph(G, air_space)

    return G

###########################################################################################################



# Crear finestra principal
root = tk.Tk()
root.title("Graph")
root.geometry("800x800")

# Crear una etiqueta
title = tk.Label(root, text="Main options:", font=("Arial", 10, "bold"))
title.pack(pady=10)  # Empaqueta el widget con espacio vertical



####################
# FUNCIONS BOTONS: #
####################
# Funcio per quan exampleButton pressionat
def ExampleButtonClick():
    global windowGraph
    windowGraph = CreateGraph_1()
    if nButton.cget('relief') == 'sunken':
        PlotNode(windowGraph, nodeSelect.get())
    else:
        Plot(windowGraph)
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio per quan inventedButton pressionat
def InventedButtonClick():
    global windowGraph
    windowGraph = CreateGraph_2()
    if nButton.cget('relief') == 'sunken':
        PlotNode(windowGraph, nodeSelect.get())
    else:
        Plot(windowGraph)
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio per quan catButton pressionat
def CatButtonClick():
    global windowGraph
    windowGraph = CreateCatGraph()
    if nButton.cget('relief') == 'sunken':
        PlotNode(windowGraph, nodeSelect.get())
    else:
        Plot(windowGraph)
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio per quan loadButton pressionat
def LoadButtonClick():
    global windowGraph
    windowGraph = GraphFile(fileName.get())
    if nButton.cget('relief') == 'sunken':
        PlotNode(windowGraph, nodeSelect.get())
    else:
        Plot(windowGraph)
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio per quan nButton pressionat
def NButtonClick():
    if PlotNode(windowGraph,nodeSelect.get()):
        if nButton.cget('relief') == 'sunken':
            # Si está presionado, lo dejamos normal
            Plot(windowGraph)
            nButton.config(relief="raised", bg="lightblue",text="Node Graph: OFF")

        else:
            # Si está normal, lo dejamos presionado
            PlotNode(windowGraph, nodeSelect.get())
            nButton.config(relief="sunken", bg="gray64",text="Node Graph: ON")
        plt.savefig("grafico.png")
        plt.show()
        GraphChange()

def AddNButtonClick():
    node = Node(nameSelect_n.get(),float(xSelect_n.get()),float(ySelect_n.get()))
    AddNode(windowGraph, node)
    if not nButton.cget('relief') == 'sunken':
        Plot(windowGraph)
    else:
        PlotNode(windowGraph, nodeSelect.get())
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()

def AddSButtonClick():
    AddSegment(windowGraph, nameSelect_s.get(), xSelect_s.get(), ySelect_s.get())
    if not nButton.cget('relief') == 'sunken':
        Plot(windowGraph)
    else:
        PlotNode(windowGraph, nodeSelect.get())
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()

def AddPButtonClick():
    Plot(windowGraph)
    PlotPath(windowGraph, FindShortestPath(windowGraph,xSelect_p.get(),ySelect_p.get()))
    plt.savefig("grafico.png")
    plt.show()
    GraphChange()



#####################################
# CREACIO BOTONS, ETIQUETES, ETC... #
#####################################
#Creacio fila per escollir el grafic
graphFrame = tk.Frame(root)
graphFrame.pack(pady=10)
exampleButton = tk.Button(graphFrame, bg="lightblue", text="Example Graph", command=ExampleButtonClick)
inventedButton = tk.Button(graphFrame, bg="lightblue", text="Invented Graph", command=InventedButtonClick)
cataloniaButton = tk.Button(graphFrame, bg="lightblue", text="Catalonia Graph", command=CatButtonClick)
exampleButton.pack(side="left", padx=5)
inventedButton.pack(side="left", padx=5)
cataloniaButton.pack(side="left", padx=5)

# Escollir filepath
loadFrame = tk.Frame(root)
loadFrame.pack(pady=10)
infLabel1 = tk.Label(loadFrame, text="File path:", font=("Arial", 7, "bold"))
loadButton = tk.Button(loadFrame, bg="lightblue", text="Load File", command=LoadButtonClick)
fileName = tk.Entry(loadFrame, width=30)
infLabel1.pack(side="left", padx=3)
fileName.pack(side="left", padx=3)
loadButton.pack(side="left", padx=3)

# Mode node
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

#Creacio fila per crear cami
pFrame = tk.Frame(root)
pFrame.pack(pady=10)
infXLabel_p = tk.Label(pFrame, text="Origin:", font=("Arial", 7, "bold"))
xSelect_p = tk.Entry(pFrame, width=10)
infYLabel_p = tk.Label(pFrame, text="Destiny:", font=("Arial", 7, "bold"))
ySelect_p = tk.Entry(pFrame, width=10)
pButton = tk.Button(pFrame, bg="lightblue", text="Find Shortest Path", command=AddPButtonClick)
infXLabel_p.pack(side="left", padx=2)
xSelect_p.pack(side="left", padx=4)
infYLabel_p.pack(side="left", padx=2)
ySelect_p.pack(side="left", padx=4)
pButton.pack(side="left", padx=5)

# Grafic en pantalla
imagenGrafico = Image.open("no_grafico.png")
imagenGrafico = imagenGrafico.resize((500, 400))
imagen_tk = ImageTk.PhotoImage(imagenGrafico)
label_imagen = tk.Label(root, image=imagen_tk)
label_imagen.pack(pady=20)
label_imagen.pack()

# Executar finestra
root.mainloop()
