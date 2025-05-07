import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from graph import *
from AirSpace import *

#####################
# VARIABLES GLOBALS #
#####################
# Dades sobre el que esta actiu
fig, ax = plt.subplots()
windowGraph = Graph()
activeNode = Node('',0,0)

indexNode = 0
catSelect = False

# Tamanys dels components del grafic
st_size = 1
sm_size = 0.3

# Variables per saber ratoli en grafic
x_limits = 0
y_limits = 0
image_size_x = int(960)
image_size_y = int(image_size_x*3/4)
# MARGENES: left 15%, right 5%, top 5%, bottom 15%
xl_margin = image_size_x * 0.15
yu_margin = image_size_y * 0.05
xr_margin = image_size_x * 0.05
yd_margin = image_size_y * 0.15

#####################
# FUNCIONS PROPIES: #
#####################
# Per sempre que canvi el grafic, mira si esta enfonsat el boto de node map
def SeeSunkenOn_NoNew():
    global ax
    fig.clf()
    ax = fig.add_subplot(111)
    if not nButton.cget('relief') == 'sunken':
        if catSelect:
            Plot(windowGraph, activeNode, 'blue', sm_size, False, ax, fig)
        else:
            Plot(windowGraph, activeNode, 'blue', st_size, True, ax, fig)
    else:
        if catSelect:
            PlotNode(windowGraph, nodeSelect.get(), sm_size, False, ax, fig)
        else:
            PlotNode(windowGraph, nodeSelect.get(), st_size, True, ax, fig)

# Per sempre que es crei grafic de zero, mira si esta enfonsat el boto de node map
def SeeSunkenOn_AllNew():
    global activeNode, ax
    fig.clf()
    ax = fig.add_subplot(111)
    if nButton.cget('relief') == 'sunken':
        if catSelect:
            PlotNode(windowGraph, nodeSelect.get(), sm_size, False, ax, fig)
        else:
            PlotNode(windowGraph, nodeSelect.get(), st_size, True, ax, fig)
    else:
        indexNode = 0
        activeNode = windowGraph.nodes[indexNode]
        if catSelect:
            Plot(windowGraph, activeNode, 'blue', sm_size, False, ax, fig)
        else:
            Plot(windowGraph, activeNode, 'blue', st_size, True, ax, fig)

# Canvia la imatge grafico.png al grafic que toca
def GraphChange():
    global x_limits, y_limits, image_size_x, image_size_y, fig
    # Actualitzem limits
    x_limits = ax.get_xlim()
    y_limits = ax.get_ylim()

    # Fiquem nova imatge, la escalem i la fiquem en format TKinter
    imagenGrafico = Image.open("grafico.png")
    nuevaImagen = imagenGrafico.resize((image_size_x, image_size_y), Image.Resampling.LANCZOS)
    nueva_imagen_tk = ImageTk.PhotoImage(nuevaImagen)

    # Actualitzem imatge
    label_imagen.config(image=nueva_imagen_tk)
    label_imagen.image = nueva_imagen_tk

# Passa de Airspace a Graph
def AirspaceToGraph(g, a):
    origin = ''
    destination = ''
    for n in a.nav_points:
        AddNode(g, Node(n.name,n.lon,n.lat))
    for s in a.nav_segments:
        for navPoint in a.nav_points:
            if navPoint.number == s.o_number:
                origin = navPoint.name
            elif navPoint.number == s.d_number:
                destination = navPoint.name
        AddSegment(g, "Segment", origin, destination)

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


#############################
# FUNCIONS BOTONS O EVENTS: #
#############################
# Funcio per quan exampleButton pressionat
def ExampleButtonClick():
    global windowGraph, activeNode, catSelect
    catSelect = False
    windowGraph = CreateGraph_1()
    SeeSunkenOn_AllNew()
    fig.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio per quan inventedButton pressionat
def InventedButtonClick():
    fig.clf()
    fig.savefig('grafico.png')
    plt.close(fig)
    global windowGraph, activeNode, catSelect
    catSelect = False
    windowGraph = CreateGraph_2()
    SeeSunkenOn_AllNew()
    fig.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio per quan catButton pressionat
def CatButtonClick():
    global windowGraph, activeNode, catSelect
    catSelect = True
    windowGraph = CreateCatGraph()
    SeeSunkenOn_AllNew()
    fig.savefig('grafico.png')
    plt.show()
    GraphChange()

# Funcio per quan loadButton pressionat
def LoadButtonClick():
    global windowGraph, activeNode, catSelect
    catSelect = False
    # Obrir per seleccionar arxiu
    file_path = filedialog.askopenfilename(title = "Select a file",filetypes = [("Text files", "*.txt"), ("All files", "*.*")])
    windowGraph = GraphFile(file_path)
    SeeSunkenOn_AllNew()
    fig.savefig('grafico.png')
    plt.show()
    GraphChange()

# Funcio per quan nButton pressionat
def NPlotButtonClick():
    if nButton.cget('relief') == 'sunken':
        # Si está presionado, lo dejamos normal
        if catSelect:
            Plot(windowGraph, activeNode, 'blue', sm_size, False, ax, fig)
        else:
            Plot(windowGraph, activeNode, 'blue', st_size, True, ax, fig)
        nButton.config(relief="raised", bg="lightblue",text="Node Graph: OFF")

    else:
        # Si está normal, lo dejamos presionado
        if nodeSelect.get() == '' or FindNodeName(windowGraph, nodeSelect.get()) == None:
            if catSelect:
                Plot(windowGraph, activeNode, 'blue', sm_size, False, ax, fig)
            else:
                Plot(windowGraph, activeNode, 'blue', st_size, True, ax, fig)
        else:
            if catSelect:
                PlotNode(windowGraph, nodeSelect.get(), sm_size, False, ax, fig)
            else:
                PlotNode(windowGraph, nodeSelect.get(), st_size, True, ax, fig)
        nButton.config(relief="sunken", bg="gray64",text="Node Graph: ON")
    fig.savefig("grafico.png")
    plt.show()
    GraphChange()

# Boto per afegir node
def AddNButtonClick():
    node = Node(nameSelect_n.get(),float(xSelect_n.get()),float(ySelect_n.get()))
    AddNode(windowGraph, node)
    SeeSunkenOn_NoNew()
    fig.savefig("grafico.png")
    plt.show()
    GraphChange()

# Boto per afegir segment
def AddSButtonClick():
    AddSegment(windowGraph, nameSelect_s.get(), xSelect_s.get(), ySelect_s.get())
    SeeSunkenOn_NoNew()
    fig.savefig("grafico.png")
    plt.show()
    GraphChange()

# Boto per trobar cami mes curt
def ShortPathButtonClick():
    if catSelect:
        Plot(windowGraph, activeNode, 'lightgray', sm_size, False, ax, fig)
        PlotPath(FindShortestPath(windowGraph, xSelect_p.get(), ySelect_p.get()), sm_size, False, fig)
    else:
        Plot(windowGraph, activeNode, 'lightgray', st_size, True, ax, fig)
        PlotPath(FindShortestPath(windowGraph, xSelect_p.get(), ySelect_p.get()), st_size, True, fig)

    fig.savefig("grafico.png")
    plt.show()
    GraphChange()

# Funcio que fara que aparegui en pantalla una pantalla per preguntar el nom del node
def NameNodeWindow(x,y):
    # Crear finestra emergent
    text_window = tk.Toplevel(root)

    # Etiqueta
    label = tk.Label(text_window, text="Node name:")
    label.pack(padx=10, pady=10)

    # Camp de texto (Entry)
    entry = tk.Entry(text_window, width=30)
    entry.pack(padx=10, pady=10)

    # Función para obtener el texto cuando se presiona un botón
    def get_text():
        AddNode(windowGraph, Node(entry.get(), x, y))
        SeeSunkenOn_NoNew()
        fig.savefig('grafico.png')
        plt.show()
        GraphChange()
        text_window.destroy()  # Cerrar la ventana emergente

    # Botón para confirmar el ingreso del texto
    submit_button = tk.Button(text_window, text="Confirm", command=get_text)
    submit_button.pack(padx=10, pady=10)

# Detecta les fletxes, per canviar node actiu
def KeyEvent(event):
    global activeNode, indexNode, ax
    fig.clf()
    ax = fig.add_subplot(111)
    tecla = event.keysym
    if tecla == "Left":
        if indexNode == 0:
            indexNode = len(windowGraph.nodes) - 1
        else:
            indexNode -= 1
    elif tecla == "Right":
        if indexNode == len(windowGraph.nodes) - 1:
            indexNode = 0
        else:
            indexNode += 1
    activeNode = windowGraph.nodes[indexNode]

    # Actualitzar pantalla

    if nButton.cget('relief') == 'sunken':
        if nodeSelect.get() == '' or FindNodeName(windowGraph, nodeSelect.get()) == None:
            if catSelect:
                PlotNode(windowGraph, activeNode.name, sm_size, False, ax, fig)
            else:
                PlotNode(windowGraph, activeNode.name, st_size, True, ax, fig)
        else:
            if catSelect:
                PlotNode(windowGraph, nodeSelect.get(), sm_size, False, ax, fig)
            else:
                PlotNode(windowGraph, nodeSelect.get(), st_size, True, ax, fig)
                PlotNode(windowGraph, nodeSelect.get(), st_size, True, ax, fig)
    else:
        if catSelect:
            Plot(windowGraph, activeNode,'blue', sm_size, False, ax, fig)
        else:
            Plot(windowGraph, activeNode,'blue', st_size, True, ax, fig)
    fig.savefig('grafico.png')
    plt.show()
    GraphChange()

# Funcio executada quan es clica al grafic
def ImageClicked(event):
    global activeNode, x_limits, y_limits
    # Obtener las coordenadas del clic dentro del label
    conversion_x = (x_limits[1]-x_limits[0])/(image_size_x-xr_margin-xl_margin)
    conversion_y = (y_limits[1]-y_limits[0])/(image_size_y-yu_margin-yd_margin)

    hitbox_x = 0.25
    hitbox_y = 0.25

    x_grafic = x_limits[0] + (event.x - xl_margin)*conversion_x
    y_grafic = y_limits[1] - (event.y - yu_margin) * conversion_y
    hay_punto = False

    if x_grafic > x_limits[0] and x_grafic < x_limits[1] and y_grafic > y_limits[0] and y_grafic < y_limits[1]: # Per saber si es troba entre els limits
        for n in windowGraph.nodes:
            if n.x > x_grafic-hitbox_x and n.x < x_grafic+hitbox_x and n.y > y_grafic-hitbox_y and n.y < y_grafic+hitbox_y:
                activeNode = n
                hay_punto = True
                break
        if not hay_punto:
            NameNodeWindow(x_grafic,y_grafic)

        SeeSunkenOn_NoNew()
        fig.savefig('grafico.png')
        plt.show()
        GraphChange()


##################################################################################################################


####################
# CREACIO FINESTRA #
####################
# Crear finestra principal
root = tk.Tk()
root.title("Graph")
root.state('zoomed')
root.configure(bg = "#ffffff")
root.bind("<Left>", KeyEvent)
root.bind("<Right>", KeyEvent)
root.focus_set()

# Agrupacio de tot
allFrame = tk.Frame(root)
allFrame.configure(bg = "#ffffff")
allFrame.pack(pady=20)

# Agrupacio botons
buttonFrame = tk.Frame(allFrame)
buttonFrame.configure(bg = "#ffffff")
buttonFrame.pack(side="left", pady=20)

# Crear una etiqueta
title = tk.Label(buttonFrame, text="Graph options:", font=("Arial", 10, "bold"))
title.pack(pady=10)  # Empaqueta el widget con espacio vertical
title.config(bg = "#ffffff")

#Creacio fila per escollir el grafic
graphFrame = tk.Frame(buttonFrame)
graphFrame.pack(pady=10)
exampleButton = tk.Button(graphFrame, bg="lightblue", text="Example Graph", command=ExampleButtonClick)
inventedButton = tk.Button(graphFrame, bg="lightblue", text="Invented Graph", command=InventedButtonClick)
cataloniaButton = tk.Button(graphFrame, bg="lightblue", text="Catalonia Graph", command=CatButtonClick)
loadButton = tk.Button(graphFrame, bg="lightblue", text="Load File", command=LoadButtonClick)
exampleButton.pack(side="left", padx=5)
inventedButton.pack(side="left", padx=5)
cataloniaButton.pack(side="left", padx=5)
loadButton.pack(side="left", padx=5)

# Mode node
nFrame = tk.Frame(buttonFrame)
nFrame.pack(pady=10)
infLabel2 = tk.Label(nFrame, text="Node name:", font=("Arial", 7, "bold"))
nButton = tk.Button(nFrame, bg="lightblue", text="Node Graph: OFF", command=NPlotButtonClick)
nodeSelect = tk.Entry(nFrame, width=10)
infLabel2.pack(side="left", padx=3)
nodeSelect.pack(side="left", padx=5)
nButton.pack(side="left", padx=5)

#Creacio fila per crear node
nodeFrame = tk.Frame(buttonFrame)
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
sFrame = tk.Frame(buttonFrame)
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

#Creacio fila per trobar cami mes curt
pFrame = tk.Frame(buttonFrame)
pFrame.pack(pady=10)
infXLabel_p = tk.Label(pFrame, text="Origin:", font=("Arial", 7, "bold"))
xSelect_p = tk.Entry(pFrame, width=10)
infYLabel_p = tk.Label(pFrame, text="Destiny:", font=("Arial", 7, "bold"))
ySelect_p = tk.Entry(pFrame, width=10)
pButton = tk.Button(pFrame, bg="lightblue", text="Find Shortest Path", command=ShortPathButtonClick)
infXLabel_p.pack(side="left", padx=2)
xSelect_p.pack(side="left", padx=4)
infYLabel_p.pack(side="left", padx=2)
ySelect_p.pack(side="left", padx=4)
pButton.pack(side="left", padx=5)

# Grafic en pantalla
imagenGrafico = Image.open("no_grafico.png")
imagenGrafico = imagenGrafico.resize((image_size_x, image_size_y), Image.Resampling.LANCZOS)
imagen_tk = ImageTk.PhotoImage(imagenGrafico)
label_imagen = tk.Label(allFrame, image = imagen_tk, bd = 0)
label_imagen.bind("<Button-1>", ImageClicked)
label_imagen.pack(side="left", pady=20)

# Executar finestra
root.mainloop()
