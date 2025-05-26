import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox

from graph import *
from AirSpace import *
import os

catnav_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cat_nav.txt")
catseg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cat_seg.txt")
cataer_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cat_aer.txt")

espnav_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spain_nav.txt")
espseg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spain_seg.txt")
espaer_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spain_aer.txt")

eurnav_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ECAC_nav.txt")
eurseg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ECAC_seg.txt")
euraer_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ECAC_aer.txt")

saved_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_paths.txt")
last_path= None
with open(saved_path, "w") as f:
    f.write('')
rutasAlternativas = []  # Guardará rutas ya mostradas
origenActual = None
destinoActual = None

#####################
# VARIABLES GLOBALS #
#####################
# Dades sobre el que esta actiu
fig, ax = plt.subplots()
data_sp = fig.subplotpars
windowGraph = Graph()
activeNode = Node('',0,0)
cont_nodo = 0
node1 = Node('',0,0)
node2 = Node('',0,0)
densidad = 1 # nodes/(area*0.035)
indexNode = 0
x_max = 0
x_min = 0
y_max = 0
y_min = 0
names = True
cost = True
density = False

#####################
# FUNCIONS PROPIES: #
#####################
# Per sempre que canvi el grafic, mira si esta enfonsat el boto de node map
def SeeSunkenOn_NoNew():
    PositionFixedButChange()
    fig.clf()
    ax = fig.add_subplot(111)
    GraphChange()
    if not nButton.cget('relief') == 'sunken':
        Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
    else:
        PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad, names, cost)
    canvas.draw()

# Per sempre que es crei grafic de zero, mira si esta enfonsat el boto de node map
def SeeSunkenOn_AllNew():
    global activeNode, ax
    fig.clf()
    ax = fig.add_subplot(111)
    GraphChange()
    ax.set_xlim(windowGraph.nodes[0].x - (x_max - x_min) / densidad**2 / 2,
                windowGraph.nodes[0].x + (x_max - x_min) / densidad**2 / 2)
    ax.set_ylim(windowGraph.nodes[0].y - (y_max - y_min) / densidad**2 / 2,
                windowGraph.nodes[0].y + (y_max - y_min) / densidad**2 / 2)
    indexNode = 0
    if nButton.cget('relief') == 'sunken':
        PlotNode(windowGraph, windowGraph.nodes[indexNode].name, ax, fig, densidad, names, cost)
    else:
        activeNode = windowGraph.nodes[indexNode]
        Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
    canvas.draw()

def PositionFixedButChange(): # Neteja pantalla per si lunic que es canvia es alguna part del graph
    global ax, x_min, x_max, y_min, y_max
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    fig.clf()
    ax = fig.add_subplot(111)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

# Canvia la imatge grafico.png al grafic que toca
def GraphChange():
    global x_max, x_min, y_max, y_min, data_sp, fig, densidad
    # Actualitzem limits
    for n in windowGraph.nodes:
        if n == windowGraph.nodes[0]:
            x_max = n.x
            x_min = n.x
        elif n.x < x_min:
            x_min = n.x
        elif n.x > x_max:
            x_max = n.x

    for n in windowGraph.nodes:
        if n == windowGraph.nodes[0]:
            y_max = n.y
            y_min = n.y
        elif n.y < y_min:
            y_min = n.y
        elif n.y > y_max:
            y_max = n.y

    data_sp = fig.subplotpars
    densidad = (len(windowGraph.nodes) / ((x_max - x_min) * (y_max - y_min) * 0.035)) ** (1 / 5)
    if densidad < 1:
        densidad = 1

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

# Aixeca botons i reinicia variables
def Reset():
    global cont_nodo, node1, node2, density
    if pButton.cget('relief') == 'sunken':
        pButton.config(relief="raised", bg="lightblue")
    if sButton.cget('relief') == 'sunken':
        sButton.config(relief="raised", bg="PaleGreen1")
    if nodeButton.cget('relief') == 'sunken':
        nodeButton.config(relief="raised", bg="PaleGreen1")
    if delNodeButton.cget('relief') == 'sunken':
        delNodeButton.config(relief="raised", bg="salmon")
    if delSButton.cget('relief') == 'sunken':
        delSButton.config(relief="raised", bg="salmon")
    cont_nodo = 0
    density = False
    node1 = None
    node2 = None

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
    air_space.nav_points = NavPointsFromFile(catnav_file)
    air_space.nav_segments = NavSegmentsFromFile(catseg_file)
    air_space.nav_airports = NavAirportsFromFile(cataer_file)

    AirspaceToGraph(G, air_space)

    return G

# Crear graph de catalunya
def CreateEspGraph():
    G = Graph()

    air_space = AirSpace()
    air_space.nav_points = NavPointsFromFile(espnav_file)
    air_space.nav_segments = NavSegmentsFromFile(espseg_file)
    air_space.nav_airports = NavAirportsFromFile(espaer_file)

    AirspaceToGraph(G, air_space)

    return G

# Crear graph de catalunya
def CreateEurGraph():
    G = Graph()

    air_space = AirSpace()
    air_space.nav_points = NavPointsFromFile(eurnav_file)
    air_space.nav_segments = NavSegmentsFromFile(eurseg_file)
    air_space.nav_airports = NavAirportsFromFile(euraer_file)

    AirspaceToGraph(G, air_space)

    return G

###########################################################################################################


#############################
# FUNCIONS BOTONS O EVENTS: #
#############################
# Funcio per quan exampleButton pressionat
def ExampleButtonClick():
    global windowGraph, activeNode
    windowGraph = CreateGraph_1()
    SeeSunkenOn_AllNew()
    Reset()

# Funcio per quan inventedButton pressionat
def InventedButtonClick():
    global windowGraph, activeNode
    windowGraph = CreateGraph_2()
    SeeSunkenOn_AllNew()
    Reset()

# Funcio per quan catButton pressionat
def CatButtonClick():
    global windowGraph, activeNode
    windowGraph = CreateCatGraph()
    SeeSunkenOn_AllNew()
    Reset()

def EspButtonClick():
    global windowGraph, activeNode
    windowGraph = CreateEspGraph()
    SeeSunkenOn_AllNew()
    Reset()

def EurButtonClick():
    global windowGraph, activeNode
    windowGraph = CreateEurGraph()
    SeeSunkenOn_AllNew()
    Reset()

# Funcio per quan loadButton pressionat
def LoadButtonClick():
    global windowGraph, activeNode
    # Obrir per seleccionar arxiu
    file_path = filedialog.askopenfilename(title = "Select a file",filetypes = [("Text files", "*.txt"), ("All files", "*.*")])
    windowGraph = GraphFile(file_path)
    SeeSunkenOn_AllNew()
    Reset()

def BlankButtonClick():
    global windowGraph, activeNode
    windowGraph = Graph()
    global activeNode, ax
    fig.clf()
    ax = fig.add_subplot(111)
    GraphChange()
    Reset()
    canvas.draw()

# Funcio per quan nButton pressionat
def NPlotButtonClick():
    PositionFixedButChange()
    if nButton.cget('relief') == 'sunken':
        # Si está presionado, lo dejamos normal
        Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
        nButton.config(relief="raised", bg="lightblue",text="Node Graph: OFF")

    else:
        # Si está normal, lo dejamos presionado
        if nodeSelect.get() == '':
            PlotNode(windowGraph, activeNode.name,ax, fig, densidad, names, cost)
        else:
            try:
                PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad, names, cost)
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error", f"Name not found in plot!")
                return None
        nButton.config(relief="sunken", bg="gray64",text="Node Graph: ON")
    canvas.draw()

# Boto per afegir node
def AddNButtonClick():
    global cont_nodo, node1, node2, activeNode
    sButton.config(relief="raised", bg="PaleGreen1")
    pButton.config(relief="raised", bg="lightblue")
    delNodeButton.config(relief="raised", bg="salmon")
    delSButton.config(relief="raised", bg="salmon")
    if xSelect_n.get() == '' or ySelect_n.get() == '':
        if cont_nodo == 0:
            if nodeButton.cget('relief') == 'sunken':
                nodeButton.config(relief="raised", bg="PaleGreen1")
            else:
                nodeButton.config(relief="sunken", bg="gray64")
            return False
        elif cont_nodo == 1 and nodeButton.cget('relief') == 'sunken':
            AddSegment(windowGraph, "Seg", node1.name, node2.name)
            nodeButton.config(relief="raised", bg="PaleGreen1")
            cont_nodo = 0
    else:
        node = Node(nameSelect_n.get(), float(xSelect_n.get()), float(ySelect_n.get()))
        AddNode(windowGraph, node)
        activeNode = node
    PositionFixedButChange()
    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
    canvas.draw()

# Boto per afegir node
def DelNButtonClick():
    global cont_nodo, node1, node2, activeNode
    sButton.config(relief="raised", bg="PaleGreen1")
    pButton.config(relief="raised", bg="lightblue")
    nodeButton.config(relief="raised", bg="PaleGreen1")
    delSButton.config(relief="raised", bg="salmon")
    if cont_nodo == 0:
        if delNodeButton.cget('relief') == 'sunken':
            delNodeButton.config(relief="raised", bg="salmon")
        else:
            delNodeButton.config(relief="sunken", bg="gray64")
        return False
    elif cont_nodo == 1 and delNodeButton.cget('relief') == 'sunken':
        AddSegment(windowGraph, "Seg", node1.name, node2.name)
        delNodeButton.config(relief="raised", bg="salmon")
        cont_nodo = 0

    PositionFixedButChange()
    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
    canvas.draw()

# Boto per afegir segment
def AddSButtonClick():
    global cont_nodo, node1, node2
    pButton.config(relief="raised", bg="lightblue")
    nodeButton.config(relief="raised", bg="PaleGreen1")
    delNodeButton.config(relief="raised", bg="salmon")
    delSButton.config(relief="raised", bg="salmon")
    if xSelect_s.get() == '' or ySelect_s.get() == '':
        if cont_nodo == 0:
            if sButton.cget('relief') == 'sunken':
                sButton.config(relief="raised", bg="PaleGreen1")
            else:
                sButton.config(relief="sunken", bg="gray64")
            return False
        elif cont_nodo == 1 and sButton.cget('relief') == 'sunken':
            AddSegment(windowGraph, "Seg", node1.name, node2.name)
            sButton.config(relief="raised", bg="PaleGreen1")
            cont_nodo = 0
    else:
        try:
            AddSegment(windowGraph, "Seg", xSelect_s.get(), ySelect_s.get())
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Non existing nodes")
            return None
    PositionFixedButChange()
    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
    canvas.draw()

# Boto per afegir segment
def DelSButtonClick():
    global cont_nodo, node1, node2

    # Restaurar estado de los otros botones
    sButton.config(relief="raised", bg="PaleGreen1")
    pButton.config(relief="raised", bg="lightblue")
    delNodeButton.config(relief="raised", bg="salmon")
    nodeButton.config(relief="raised", bg="PaleGreen1")

    # Modo selección por menú desplegable
    if xSelect_s.get() and ySelect_s.get():
        origin = xSelect_s.get()
        destination = ySelect_s.get()
        success = DelSegment(windowGraph, origin, destination)
        if not success:
            messagebox.showerror("Error", "Segment not found or nodes do not exist.")
            return
    # Modo selección por clics en nodos
    elif cont_nodo == 1 and delSButton.cget('relief') == 'sunken':
        success = DelSegment(windowGraph, node1.name, node2.name)
        if not success:
            messagebox.showerror("Error", "Segment not found between selected nodes.")
            return
        cont_nodo = 0
    else:
        # Activar/desactivar modo selección
        if delSButton.cget('relief') == 'sunken':
            delSButton.config(relief="raised", bg="salmon")
        else:
            delSButton.config(relief="sunken", bg="gray64")
        return

    # Actualizar visualización
    delSButton.config(relief="raised", bg="salmon")
    PositionFixedButChange()
    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
    canvas.draw()

# Boto per trobar cami mes curt
def ShortPathButtonClick():
    global cont_nodo, last_path, rutasAlternativas, origenActual, destinoActual
    sButton.config(relief="raised", bg="lightblue")
    nodeButton.config(relief="raised", bg="lightblue")
    delNodeButton.config(relief="raised", bg="salmon")
    PositionFixedButChange()
    if xSelect_p.get() == '' or ySelect_p.get() == '':
        if cont_nodo == 0:
            if pButton.cget('relief') == 'sunken':
                pButton.config(relief="raised", bg="lightblue")
            else:
                pButton.config(relief="sunken", bg="gray64")
                return False
            return False
        elif cont_nodo == 1 and pButton.cget('relief') == 'sunken':
            cont_nodo = 0
            pButton.config(relief="raised", bg="lightblue")
            try:
                rutasAlternativas=[]
                altPathButton.config(state="normal", text="Alternative Path")
                origenActual = xSelect_p.get()
                destinoActual = ySelect_p.get()
                last_path = FindShortestPath(windowGraph, origenActual, destinoActual, rutasAlternativas)
                rutasAlternativas.append(last_path)
                PlotPath(last_path, windowGraph, ax, densidad)
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error", f"Non reachable path!")
                return None
    else:
        try:
            rutasAlternativas=[]
            altPathButton.config(state="normal", text="Alternative Path")
            origenActual = xSelect_p.get()
            destinoActual = ySelect_p.get()
            last_path = FindShortestPath(windowGraph, origenActual, destinoActual, rutasAlternativas)
            rutasAlternativas.append(last_path)
            PlotPath(last_path, windowGraph, ax, densidad)

        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Non reachable path!")
            return None
    nButton.config(relief="raised", bg="lightblue", text="Node Graph: OFF")
    canvas.draw()

def SavePath():
    global last_path
    if not last_path:
        messagebox.showerror("Error", "No path to save!")
        return

    with open(saved_path, "a") as f:
        f.write("Path:\n")
        for n in last_path.nodes:
            f.write(f"{n.name} ({n.x}, {n.y})\n")
        f.write(f"Total distance: {round(last_path.cost, 2)}\n")
        f.write("-----\n")

    messagebox.showinfo("Saved", "Path saved.")

def AlternativePathClick():
    global rutasAlternativas, last_path, origenActual, destinoActual, altPathButton

    if origenActual is None or destinoActual is None:
        messagebox.showerror("Error", "Primero genera una ruta con 'Find Shortest Path'")
        return

    try:
        nuevaRuta = FindShortestPath(windowGraph, origenActual, destinoActual, rutasAlternativas)
    except Exception as e:
        altPathButton.config(state="disabled", text="No more paths")
        messagebox.showinfo("Info", "No hay más rutas alternativas.")
        return

    rutasAlternativas.append(nuevaRuta)
    last_path = nuevaRuta
    PositionFixedButChange()
    PlotPath(last_path, windowGraph, ax, densidad)
    canvas.draw()

# Boto per guardar KML
def KmlButtonClick():
    """
    Genera un archivo KML con los puntos dados y opcionalmente una ruta que los conecta.

    :param nombre_archivo: Nombre del archivo .kml a generar (ej: "mapa.kml")
    :param puntos: Lista de tuplas (nombre, descripcion, latitud, longitud)
    :param incluir_ruta: Booleano. Si es True, dibuja una línea conectando los puntos en orden.
    """
    def escapar(texto):
        return texto.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
'''

    # Añadir puntos
    for n in windowGraph.nodes:
        kml += (f'''
<Placemark> <name>{escapar(n.name)}</name>
    <Point>
        <coordinates>
            {n.x},{n.y}
        </coordinates>
    </Point>
</Placemark>
''')

    # Añadir ruta si se desea
    n1 = Node("",0,0)
    n2 = Node("",0,0)
    for s in windowGraph.segments:
        for n in windowGraph.nodes:
            if s.origin_n == n.name:
                n1 = n
            elif s.dest_n == n.name:
                n2 = n

    Name = f"Route {n1.name} - {n2.name}"
    coord1 = f"{n1.x},{n1.y}"
    coord2 = f"{n2.x},{n2.y}"
    kml += (f'''
<Placemark>
    <name>{Name}</name>
    <LineString>
        <tessellate>1</tessellate>
        <coordinates>
            {coord1}
            {coord2}
        </coordinates>
    </LineString>
</Placemark>
''')

    print(kml)
    kml += ('</Document>\n</kml>')

    archivo = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("Archivos KML", "*.kml")],
        title="Guardar archivo KML"
    )

    if archivo:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(kml)
        print(f"KML guardado en: {archivo}")
    else:
        print("Operación cancelada.")

def DensityButtonClick():
    global density
    density = True
    PositionFixedButChange()
    fig.clf()
    ax = fig.add_subplot(111)
    GraphChange()
    for n in windowGraph.nodes:
        ax.plot(n.x, n.y, 'o', color='red', markersize=4 + 2*len(n.neighbors))
        # Escriu el nom dels nodes a dalt a la dreta
        if names:
            ax.text(n.x + 0.1/densidad**2, n.y + 0.1/densidad**2, n.name, color='black', weight='bold', fontsize=6, clip_on=True)

    # Dibuixa segments i mostra el que mesuren
    for s in windowGraph.segments:
        CreateNiceArrows(s, "blue", "blue", 0.5/densidad**3, 0.2/densidad**3, 1.5, ax)
        if cost:
            MidTextSegment(s, round(s.cost, 2), 8, 'black', ax)

    ax.grid(color='red', linestyle='dashed', linewidth=0.5) # Dibuixa una graella pel fons
    canvas.draw()

def QNamesButtonClick():
    global names
    if names == True:
        names = False
        qNamesButton.config(relief="sunken", bg="gray64", text="Quit Names: ON")
    else:
        names = True
        qNamesButton.config(relief="raised", bg="lightblue", text="Quit Names: OFF")
    PositionFixedButChange()
    if density == False:
        SeeSunkenOn_NoNew()
    else:
        DensityButtonClick()

def QCostButtonClick():
    global cost
    if cost == True:
        cost = False
        qCostButton.config(relief="sunken", bg="gray64", text="Quit Cost: ON")
    else:
        cost = True
        qCostButton.config(relief="raised", bg="lightblue", text="Quit Cost: OFF")
    PositionFixedButChange()
    if density == False:
        SeeSunkenOn_NoNew()
    else:
        DensityButtonClick()

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
        global activeNode
        node = Node(entry.get(), x, y)
        AddNode(windowGraph, node)
        activeNode = node
        PositionFixedButChange()
        Plot(windowGraph, node, 'blue', ax, fig, densidad, names, cost)
        canvas.draw()
        text_window.destroy()  # Cerrar la ventana emergente

    # Botón para confirmar el ingreso del texto
    submit_button = tk.Button(text_window, text="Confirm", command=get_text)
    submit_button.pack(padx=10, pady=10)

# Detecta les fletxes, per canviar node actiu
def KeyEvent(event):
    global activeNode, indexNode, ax
    PositionFixedButChange()
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
    canvas.draw()

    # Actualitzar pantalla
    if nButton.cget('relief') == 'sunken':
        if nodeSelect.get() == '' or FindNodeName(windowGraph, nodeSelect.get()) == None:
            PlotNode(windowGraph, activeNode.name, ax, fig, densidad, names, cost)
        else:
            PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad, names, cost)
    else:
        Plot(windowGraph, activeNode,'blue', ax, fig, densidad, names, cost)
    canvas.draw()

# Funcio executada quan es clica al grafic
def PlotClicked(event):
    nodo_clickado = Node("",0,0)
    if toolbar.mode != 'pan/zoom' and toolbar.mode != 'zoom rect':
        global activeNode, ax, x_min,x_max,y_min,y_max, node1, node2, cont_nodo
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        hitbox_x = 0.3/densidad**4
        hitbox_y = 0.3/densidad**4

        x_grafic = event.xdata
        y_grafic = event.ydata

        hay_punto = False

        if x_grafic > x_min and x_grafic < x_max and y_grafic > y_min and y_grafic < y_max: # Per saber si es troba entre els limits
            for n in windowGraph.nodes:
                if n.x > x_grafic-hitbox_x and n.x < x_grafic+hitbox_x and n.y > y_grafic-hitbox_y and n.y < y_grafic+hitbox_y:
                    if pButton.cget('relief') == 'sunken' or sButton.cget('relief') == 'sunken':
                        if cont_nodo == 0:
                            node1 = n
                            cont_nodo = 1
                        elif cont_nodo == 1:
                            node2 = n
                            if pButton.cget('relief') == 'sunken':
                                ShortPathButtonClick()
                            elif sButton.cget('relief') == 'sunken':
                                AddSButtonClick()
                            elif delSButton.cget('relief') == 'sunken':
                                DelSButtonClick()
                    else:
                        activeNode = n
                    nodo_clickado = n
                    hay_punto = True
                    break
            if not hay_punto and nodeButton.cget('relief') == 'sunken':
                NameNodeWindow(x_grafic,y_grafic)
                nodeButton.config(relief="raised", bg="PaleGreen1")
            elif hay_punto and delNodeButton.cget('relief') == 'sunken':
                DelNode(windowGraph,nodo_clickado)
                activeNode = windowGraph.nodes[0]
                SeeSunkenOn_NoNew()
                canvas.draw()

            if pButton.cget('relief') != 'sunken' and sButton.cget('relief') != 'sunken' and delSButton.cget('relief') != 'sunken':
                fig.clf()
                ax = fig.add_subplot(111)
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
                GraphChange()
                if not nButton.cget('relief') == 'sunken':
                    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad, names, cost)
                else:
                    PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad, names, cost)
                canvas.draw()

# Per fer zoom
def OnScroll(event):
    ax = event.inaxes
    if ax is None:
        return  # No hacer nada si el mouse no está sobre un eje

    base_scale = 1.2
    scale_factor = 1 / base_scale if event.step > 0 else base_scale

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    xdata = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    ydata = (ax.get_ylim()[0] + ax.get_ylim()[1]) / 2

    new_width = (xlim[1] - xlim[0]) * scale_factor
    new_height = (ylim[1] - ylim[0]) * scale_factor

    ax.set_xlim([xdata - new_width / 2, xdata + new_width / 2])
    ax.set_ylim([ydata - new_height / 2, ydata + new_height / 2])
    canvas.draw()

# Per sortir de sunken
def EscButton(event):
    Reset()

##################################################################################################################


####################
# CREACIO FINESTRA #
####################

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# --- Ventana principal ---
root = tk.Tk()
root.title("Graph")
root.state('zoomed')
root.configure(bg="#ffffff")
root.bind("<Left>", KeyEvent)
root.bind("<Right>", KeyEvent)
root.bind('<Escape>', EscButton)
root.focus_set()

# Configuración de layout principal
root.columnconfigure(0, weight=1)   # 1/5 para botones
root.columnconfigure(1, weight=100)   # 4/5 para canvas
root.rowconfigure(0, weight=1)      # Principal
root.rowconfigure(1, weight=0)      # Toolbar

# --- Panel lateral izquierdo ---
sidebar = tk.Frame(root, bg="#ffffff")
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)  # Evita que el contenido lo expanda

# Título
title = tk.Label(sidebar, text="Graph main options:", font=("Arial", 10, "bold"))
title.pack(pady=(10, 5), fill="x")

# Crear un sub-frame dentro del sidebar para el grid de botones
button_grid = tk.Frame(sidebar)
button_grid.pack(fill="both", expand=True, padx=10, pady=10)

# Lista de botones
buttons = [
    ("Example Graph", ExampleButtonClick),
    ("Invented Graph", InventedButtonClick),
    ("Catalonia Graph", CatButtonClick),
    ("Spain Graph", EspButtonClick),
    ("Europe Graph", EurButtonClick),
    ("Load File", LoadButtonClick),
    ("Blank Graph", BlankButtonClick)
]

# Distribuir botones en 2 columnas dentro del sub-frame
for index, (text, command) in enumerate(buttons):
    row = index // 2
    col = index % 2
    tk.Button(
        button_grid, bg="lightblue", text=text, command=command
    ).grid(row=row, column=col, sticky="ew", padx=5, pady=4)

# Hacer que las columnas del sub-frame se expandan igualmente
button_grid.grid_columnconfigure(0, weight=1)
button_grid.grid_columnconfigure(1, weight=1)

# --- Crear Node ---
nodeFrame = tk.Frame(sidebar)
nodeFrame.pack(pady=10, fill="x")
tk.Label(nodeFrame, text="Node name:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
nameSelect_n = tk.Entry(nodeFrame, width=10)
nameSelect_n.pack(side="left", padx=4)
tk.Label(nodeFrame, text="X:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
xSelect_n = tk.Entry(nodeFrame, width=10)
xSelect_n.pack(side="left", padx=4)
tk.Label(nodeFrame, text="Y:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
ySelect_n = tk.Entry(nodeFrame, width=10)
ySelect_n.pack(side="left", padx=4)
# Node Button
nodeButton = tk.Button(sidebar, bg="PaleGreen1", text="Create Node", command=AddNButtonClick)
nodeButton.pack(fill="x", padx=10, pady=4)
delNodeButton = tk.Button(sidebar, bg="salmon", text="Delete Node", command=DelNButtonClick)
delNodeButton.pack(fill="x", padx=10, pady=4)

# --- Crear Segment ---
sFrame = tk.Frame(sidebar)
sFrame.pack(pady=10, fill="x")
tk.Label(sFrame, text="Origin:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
xSelect_s = tk.Entry(sFrame, width=10)
xSelect_s.pack(side="left", padx=4)
tk.Label(sFrame, text="Destiny:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
ySelect_s = tk.Entry(sFrame, width=10)
ySelect_s.pack(side="left", padx=4)
# Segment Button
sButton = tk.Button(sidebar, bg="PaleGreen1", text="Create Segment", command=AddSButtonClick)
sButton.pack(fill="x", padx=10, pady=4)
delSButton = tk.Button(sidebar, bg="salmon", text="Delete Segment", command=DelSButtonClick)
delSButton.pack(fill="x", padx=10, pady=4)

# --- Shortest Path ---
pFrame = tk.Frame(sidebar)
pFrame.pack(pady=10, fill="x")
tk.Label(pFrame, text="Origin:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
xSelect_p = tk.Entry(pFrame, width=10)
xSelect_p.pack(side="left", padx=4)
tk.Label(pFrame, text="Destiny:", font=("Arial", 7, "bold")).pack(side="left", padx=2)
ySelect_p = tk.Entry(pFrame, width=10)
ySelect_p.pack(side="left", padx=4)
# Path Button
pButton = tk.Button(sidebar, bg="lightblue", text="Find Shortest Path", command=ShortPathButtonClick)
pButton.pack(fill="x", padx=10, pady=4)
altPathButton = tk.Button(sidebar, bg="pink", text="Alternative Path", command=AlternativePathClick)
altPathButton.pack(fill="x", padx=10, pady=4)
tk.Button(sidebar, bg="lightyellow", text="Save path to file", command=SavePath).pack(fill="x", padx=10, pady=4)

# --- Node Graph Mode ---
nFrame = tk.Frame(sidebar)
nFrame.pack(pady=10, fill="x")
tk.Label(nFrame, text="Node name:", font=("Arial", 7, "bold")).pack(side="left", padx=3)
nodeSelect = tk.Entry(nFrame, width=10)
nodeSelect.pack(side="left", padx=5)
# Node Mode Button
nButton = tk.Button(sidebar, bg="lightblue", text="Node Graph: OFF", command=NPlotButtonClick)
nButton.pack(fill="x", padx=10, pady=4)

# Título Otros
title = tk.Label(sidebar, text="Other options:", font=("Arial", 10, "bold"))
title.pack(pady=(10, 5), fill="x")

for text, command in [
    ("Save KML", KmlButtonClick),
    ("Density Graph", DensityButtonClick)
]:
    tk.Button(sidebar, bg="lightblue", text=text, command=command).pack(fill="x", padx=10, pady=4)

qNamesButton = tk.Button(sidebar, bg="lightblue", text="Quit Names: OFF", command=QNamesButtonClick)
qNamesButton.pack(fill="x", padx=10, pady=4)

qCostButton = tk.Button(sidebar, bg="lightblue", text="Quit Cost: OFF", command=QCostButtonClick)
qCostButton.pack(fill="x", padx=10, pady=4)


# --- Canvas para el gráfico ---
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=1, sticky="nsew")
canvas.mpl_connect('scroll_event', OnScroll)
canvas.mpl_connect("button_press_event", PlotClicked)

# --- Toolbar ---
toolbar_frame = tk.Frame(root)
toolbar_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Ejecutar ventana
root.mainloop()
