from node import *
from segment import *
from path import *
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.nodes = []         #Llista de nodes
        self.segments = []      #Llista de segments

##################
# FUNCIONS GRAPH #
##################
def AddNode(g, n): # Afegeix un node a un Graph g
    if n in g.nodes: # Mira que el node no estigui ja al Graph g
        return False
    else:
        g.nodes.append(n)
        return True

def DelNode(g, n): # Afegeix un node a un Graph g
    # eliminar node
    g.nodes = [node for node in g.nodes if node.name != n.name]

    # eliminar segments
    g.segments = [s for s in g.segments if s.origin_n != n and s.dest_n != n]

def FindNodeName(g, name): # Troba a un Graph el node amb el nom indicat
    for n in g.nodes:
        if n.name == name:
            return n
    return None

def AddSegment(g, segmentName, nameOriginNode, nameDestinationNode): # Afegeix un segment a un Graph g
    foundOrigin = False
    originNode = g.nodes[0]
    foundDestination = False
    destinationNode = g.nodes[0]
    for n in g.nodes: # Busca que es trobi el nom de l'origen i el nom del desti
        if n.name == nameOriginNode: # Trobar origen
            foundOrigin = True
            originNode = n
        elif n.name == nameDestinationNode: # Trobar desti
            foundDestination = True
            destinationNode = n

    if foundOrigin and foundDestination: # Si els ha trobat afegira un segment al Graph g i retornara True
        s = Segment(segmentName, originNode, destinationNode)
        g.segments.append(s)
        AddNeighbor(originNode, destinationNode)
        return True
    else: # Si no ha trobat els dos retornara False
        return False

def DelSegment(g, nameOriginNode, nameDestinationNode):  # Elimina un segment del Graph g
    foundOrigin = False
    originNode = g.nodes[0]
    foundDestination = False
    destinationNode = g.nodes[0]

    # busca nodes
    for n in g.nodes:
        if n.name == nameOriginNode:
            foundOrigin = True
            originNode = n
        elif n.name == nameDestinationNode:
            foundDestination = True
            destinationNode = n

    if foundOrigin and foundDestination:
        for s in g.segments:
            if (s.origin_n == originNode and s.dest_n == destinationNode):
                g.segments.remove(s)
                return True
        return False  # si no es troba el segment exacte
    else:
        return False  # si no s'han trobat els dos nodes

def AddDobleSegment(g, segmentName, n1, n2): # Afegeix un segment en doble direccio
    AddSegment(g, segmentName, n1, n2)
    AddSegment(g, segmentName, n2, n1)

def GetClosest(g, x, y): # Troba el node que pertany al Graph g mes proper al punt:(x,y)
    point = Node("Point",x,y) # Node que marca el punt
    closest = g.nodes[0]
    dist = Distance(point,g.nodes[0])
    for n in g.nodes: # Mira tots els nodes de g i compara amb el que era mes proper dels anteriors
        if Distance(point,n) < dist:
            dist = Distance(point,n)
            closest = n
    return closest

def Plot(g, active_n, color, ax, fig, densidad, names, cost):
    # Dibuixa els nodes
    for n in g.nodes:
        if n == active_n:
            ax.plot(n.x, n.y, 'o', color='darkblue', markersize=7)
        else:
            ax.plot(n.x, n.y, 'o', color='red', markersize=5)
        # Escriu el nom dels nodes a dalt a la dreta
        if names:
            ax.text(n.x + 0.1/densidad**2, n.y + 0.1/densidad**2, n.name, color='black', weight='bold', fontsize=6, clip_on=True)

    # Dibuixa segments i mostra el que mesuren
    for s in g.segments:
        CreateNiceArrows(s, color, color, 0.5/densidad**3, 0.2/densidad**3, 1.5, ax)
        if cost:
            MidTextSegment(s, round(s.cost, 2), 8, 'black', ax)

    ax.grid(color='red', linestyle='dashed', linewidth=0.5) # Dibuixa una graella pel fons

def PlotNode (g, nameOrigin, ax, fig, densidad, names, cost):
    node = next(n for n in g.nodes if n.name == nameOrigin) # Primer node que compleixi que el seu nom es igual a nameOrigin
    i = 1
    if node == None: # Si no s'ha trobat cap node la funcio acaba
        return False
    else: # Si s'ha trobat creara un segment entre els nodes veins del node i el node, a mes de dibuixar tots els nodes del Graph g
        for n in g.nodes:
            if n == node:
                ax.plot(n.x, n.y, 'o', color='blue', markersize=5) # Pinta el node principal de blau
            elif n in node.neighbors:
                ax.plot(n.x, n.y, 'o', color='green', markersize=5) # Pinta els nodes veins de verd
                # Crea fletxa per unir el node amb el vei
                s = Segment('Unión vecina' + str(i), node, n)
                i += 1
                CreateNiceArrows(s, 'red', 'red', 0.5/densidad**3, 0.2/densidad**3, 1.5, ax)
                if cost:
                    MidTextSegment(s, round(s.cost, 2), 8,'black', ax)
            else:
                ax.plot(n.x, n.y, 'o', color='grey', markersize=5) # Pinta els nodes no veins de gris
            # Escriu el nom del node
            if names:
                ax.text(n.x + 0.1/densidad**2, n.y + 0.1/densidad**2, n.name, color='green', weight='bold', fontsize=6, clip_on=True)

        ax.grid(color='blue', linestyle='dashed', linewidth=0.5)  # Dibuixa una graella pel fons

        return True

import tkinter as tk
from tkinter import messagebox

def GraphFile(filename):
    # Hi haura un text que marqui Node,x,y i un altre Segment,Origin,Destination
    g = Graph() # Es crea un Graph g on es guardaran totes les dades
    try:
        with open(filename, 'r') as file:
            lines = file.readlines() # Llista amb les linies del fitxer
    except Exception:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Could not open the file")
        root.destroy()
        return None

    reading_nodes = True # Variable que determinara si esta llegint els nodes (True) o els segments (False)
    try:
        for line in lines:
            line = line.strip() # Elimina espais inicials

            # Mira en quin cas es troba: linia buida, node o segment
            if not line:
                continue
            if line == "Segment, Origin, Destination:":
                reading_nodes = False
                continue
            elif line == "Node, x, y:":
                reading_nodes = True
                continue

            parts = line.split(",") # Separa les paraules per la coma

            if reading_nodes:
                # NODES:
                if len(parts) != 3:
                    raise ValueError("Wrong node format")
                name = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                # Crea node i l'afegeix a g
                node = Node(name, x, y)
                g.nodes.append(node)
            else:
                # SEGMENTS:
                if len(parts) != 3:
                    raise ValueError("Wrong segment format")
                seg_name = parts[0]
                origin_name = parts[1]
                dest_name = parts[2]

                # Busca quin node te de nom el esmentat en el fitxer (tant d'origen com de desti)
                origin_node = next((n for n in g.nodes if n.name == origin_name), None)
                dest_node = next((n for n in g.nodes if n.name == dest_name), None)
                if origin_node is None or dest_node is None:
                    raise ValueError("origin or destiny node not found")

                # Crea segment i l'afegeix a g
                segment = Segment(seg_name, origin_node, dest_node)
                g.segments.append(segment)

                # Afegeix el node desti com a vei del node origen
                origin_node.neighbors.append(dest_node)

        return g # Retorna el Graph

    except Exception:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Wrong file format")
        root.destroy()
        return None


def FindShortestPath(g, n_orig, n_dest, rutas_descartadas=[]):
    orig = FindNodeName(g, n_orig)
    dest = FindNodeName(g, n_dest)

    short_paths = [Path()]
    AddNodeToPath(short_paths[0], orig)
    short_paths[0].cost = Distance(orig, dest)

    visited_paths = []

    while short_paths:
        # ordena pel cost
        short_paths.sort(key=lambda p: p.cost)
        current_path = short_paths.pop(0)
        current_node = current_path.nodes[-1]

        # Si ja s'ha arribat
        if current_node == dest:
            # es mira si la ruta ja esta descartada
            current_route_names = [n.name for n in current_path.nodes]
            for descartada in rutas_descartadas:
                if current_route_names == [n.name for n in descartada.nodes]:
                    break
            else:
                return current_path  # Ruta nova

        # s'expandeixen neighbors
        for neighbor in current_node.neighbors:
            if neighbor not in current_path.nodes:
                new_path = Path()
                new_path.nodes = current_path.nodes.copy()
                new_path.nodes.append(neighbor)

                # Calcular cost
                cost = 0
                for i in range(len(new_path.nodes) - 1):
                    cost += Distance(new_path.nodes[i], new_path.nodes[i + 1])
                cost += Distance(new_path.nodes[-1], dest)
                new_path.cost = cost

                short_paths.append(new_path)

    # Si no es troba ruta nova
    raise Exception("Path already shown")

#####################
# FUNCIONS PER PLOT #
#####################
def CreateNiceArrows(segment, segment_color, head_color, headArrow_l, headArrow_w, l_width, ax):  # Crea fletxes amb el cap centrat
    # Dibuixa el segment
    ax.plot([segment.origin_n.x, segment.dest_n.x], [segment.origin_n.y, segment.dest_n.y], color = segment_color, linewidth = l_width, zorder = 0)

    # Increment de x i de y
    dx = segment.dest_n.x - segment.origin_n.x
    dy = segment.dest_n.y - segment.origin_n.y

    # Dibuixa la fletxa
    ax.arrow(segment.origin_n.x, segment.origin_n.y, dx, dy, length_includes_head = True, head_length = headArrow_l, head_width = headArrow_w, color = head_color)

def MidTextSegment(segment, text, size, text_color, ax): # Fica un text centrat en un segment
    # Centre del segment
    mid_x = (segment.origin_n.x + segment.dest_n.x) / 2
    mid_y = (segment.origin_n.y + segment.dest_n.y) / 2

    # Escriu text
    ax.text(mid_x, mid_y, text, fontsize=size, color=text_color, weight='bold', ha='center', clip_on=True)