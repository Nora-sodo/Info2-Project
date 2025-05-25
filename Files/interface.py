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
        Plot(windowGraph, activeNode, 'blue', ax, fig, densidad)
    else:
        PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad)
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
        PlotNode(windowGraph, windowGraph.nodes[indexNode].name, ax, fig, densidad)
    else:
        activeNode = windowGraph.nodes[indexNode]
        Plot(windowGraph, activeNode, 'blue', ax, fig, densidad)
    canvas.draw()

def PositionFixedButChange():
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
    densidad = (len(windowGraph.nodes)/((x_max-x_min)*(y_max-y_min)*0.035))**(1/5)

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
    global cont_nodo, node1, node2
    if pButton.cget('relief') == 'sunken':
        pButton.config(relief="raised", bg="lightblue")
    if sButton.cget('relief') == 'sunken':
        sButton.config(relief="raised", bg="lightblue")
    if nodeButton.cget('relief') == 'sunken':
        nodeButton.config(relief="raised", bg="lightblue")
    cont_nodo = 0
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

# Funcio per quan nButton pressionat
def NPlotButtonClick():
    PositionFixedButChange()
    if nButton.cget('relief') == 'sunken':
        # Si está presionado, lo dejamos normal
        Plot(windowGraph, activeNode, 'blue', ax, fig, densidad)
        nButton.config(relief="raised", bg="lightblue",text="Node Graph: OFF")

    else:
        # Si está normal, lo dejamos presionado
        if nodeSelect.get() == '':
            PlotNode(windowGraph, activeNode.name,ax, fig, densidad)
        else:
            try:
                PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad)
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
    sButton.config(relief="raised", bg="lightblue")
    pButton.config(relief="raised", bg="lightblue")
    if xSelect_n.get() == '' or ySelect_n.get() == '':
        if cont_nodo == 0:
            if nodeButton.cget('relief') == 'sunken':
                nodeButton.config(relief="raised", bg="lightblue")
            else:
                nodeButton.config(relief="sunken", bg="gray64")
            return False
        elif cont_nodo == 1 and nodeButton.cget('relief') == 'sunken':
            AddSegment(windowGraph, "Seg", node1.name, node2.name)
            nodeButton.config(relief="raised", bg="lightblue")
            cont_nodo = 0
    else:
        node = Node(nameSelect_n.get(), float(xSelect_n.get()), float(ySelect_n.get()))
        AddNode(windowGraph, node)
        activeNode = node
    PositionFixedButChange()
    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad)
    canvas.draw()

# Boto per afegir segment
def AddSButtonClick():
    global cont_nodo, node1, node2
    pButton.config(relief="raised", bg="lightblue")
    nodeButton.config(relief="raised", bg="lightblue")
    if xSelect_s.get() == '' or ySelect_s.get() == '':
        if cont_nodo == 0:
            if sButton.cget('relief') == 'sunken':
                sButton.config(relief="raised", bg="lightblue")
            else:
                sButton.config(relief="sunken", bg="gray64")
            return False
        elif cont_nodo == 1 and sButton.cget('relief') == 'sunken':
            AddSegment(windowGraph, "Seg", node1.name, node2.name)
            sButton.config(relief="raised", bg="lightblue")
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
    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad)
    canvas.draw()

# Boto per trobar cami mes curt
def ShortPathButtonClick():
    global cont_nodo
    sButton.config(relief="raised", bg="lightblue")
    nodeButton.config(relief="raised", bg="lightblue")
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
                PlotPath(FindShortestPath(windowGraph, node1.name, node2.name), windowGraph, ax, densidad)
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error", f"Non reachable path!")
                return None
    else:
        try:
            PlotPath(FindShortestPath(windowGraph, xSelect_p.get(), ySelect_p.get()), windowGraph, ax, densidad)
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Non reachable path!")
            return None
    nButton.config(relief="raised", bg="lightblue", text="Node Graph: OFF")
    canvas.draw()

# Boto per guardar KML
def KmlButton():
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
        Plot(windowGraph, node, 'blue', ax, fig, densidad)
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
            PlotNode(windowGraph, activeNode.name, ax, fig, densidad)
        else:
            PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad)
    else:
        Plot(windowGraph, activeNode,'blue', ax, fig, densidad)
    canvas.draw()

# Funcio executada quan es clica al grafic
def PlotClicked(event):
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
                            else:
                                AddSButtonClick()
                    else:
                        activeNode = n
                    hay_punto = True
                    break
            if not hay_punto and densidad < 3 and nodeButton.cget('relief') == 'sunken':
                NameNodeWindow(x_grafic,y_grafic)
                nodeButton.config(relief="raised", bg="lightblue")

            if pButton.cget('relief') != 'sunken' and sButton.cget('relief') != 'sunken':
                fig.clf()
                ax = fig.add_subplot(111)
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
                GraphChange()
                if not nButton.cget('relief') == 'sunken':
                    Plot(windowGraph, activeNode, 'blue', ax, fig, densidad)
                else:
                    PlotNode(windowGraph, nodeSelect.get(), ax, fig, densidad)
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
    """xdata = event.xdata
    ydata = event.ydata"""

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
root.columnconfigure(1, weight=4)   # 4/5 para canvas
root.rowconfigure(0, weight=1)      # Principal
root.rowconfigure(1, weight=0)      # Toolbar

# --- Panel lateral izquierdo ---
sidebar = tk.Frame(root, bg="#ffffff")
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)  # Evita que el contenido lo expanda

# Título
title = tk.Label(sidebar, text="Graph options:", font=("Arial", 10, "bold"))
title.pack(pady=(10, 5), fill="x")

# Botones de selección de gráfico
for text, command in [
    ("Example Graph", ExampleButtonClick),
    ("Invented Graph", InventedButtonClick),
    ("Catalonia Graph", CatButtonClick),
    ("Spain Graph", EspButtonClick),
    ("Europe Graph", EurButtonClick),
    ("Load File", LoadButtonClick),
    ("Save KML", KmlButton)
]:
    tk.Button(sidebar, bg="lightblue", text=text, command=command).pack(fill="x", padx=10, pady=4)

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
nodeButton = tk.Button(sidebar, bg="lightblue", text="Create Node", command=AddNButtonClick)
nodeButton.pack(fill="x", padx=10, pady=4)

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
sButton = tk.Button(sidebar, bg="lightblue", text="Create Segment", command=AddSButtonClick)
sButton.pack(fill="x", padx=10, pady=4)

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

# --- Node Graph Mode ---
nFrame = tk.Frame(sidebar)
nFrame.pack(pady=10, fill="x")
tk.Label(nFrame, text="Node name:", font=("Arial", 7, "bold")).pack(side="left", padx=3)
nodeSelect = tk.Entry(nFrame, width=10)
nodeSelect.pack(side="left", padx=5)
# Node Mode Button
nButton = tk.Button(sidebar, bg="lightblue", text="Node Graph: OFF", command=NPlotButtonClick)
nButton.pack(fill="x", padx=10, pady=4)

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
