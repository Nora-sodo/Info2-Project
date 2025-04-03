from segment import *
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes = []         #Llista de nodes
        self.segments = []      #Llista de segments

ejesGrafico = [-5,25,-5,25]

def AddNode(g, n): # Afegeix un node a un Graph g
    if n in g.nodes: # Mira que el node no estigui ja al Graph g
        return False
    else:
        g.nodes.append(n)
        return True

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

def GetClosest(g, x, y): # Troba el node que pertany al Graph g mes proper al punt:(x,y)
    point = Node("Point",x,y) # Node que marca el punt
    closest = g.nodes[0]
    dist = Distance(point,g.nodes[0])
    for n in g.nodes: # Mira tots els nodes de g i compara amb el que era mes proper dels anteriors
        if Distance(point,n) < dist:
            dist = Distance(point,n)
            closest = n
    return closest

def CreateNiceArrows(segment, segment_color, out_color, in_color, headArrow_l, headArrow_w):  # Crea fletxes amb el cap centrat
    # Dibuixa el segment
    plt.plot([segment.origin_n.x, segment.dest_n.x], [segment.origin_n.y, segment.dest_n.y], color = segment_color,zorder = 0)

    # Increment de x i de y
    dx = segment.dest_n.x - segment.origin_n.x
    dy = segment.dest_n.y - segment.origin_n.y

    # Normalizar la direccio per ajustar la longitud de la fletxa
    norm = (dx ** 2 + dy ** 2) ** 0.5  # Magnitud del vector
    unit_dx = dx / norm  # Direccio normalizada en x
    unit_dy = dy / norm  # Direccio normalizada en y

    # Dibuixa la fletxa
    plt.arrow(segment.origin_n.x,segment.origin_n.y,dx-headArrow_l*unit_dx,dy-headArrow_l*unit_dy,head_width = headArrow_w, head_length = headArrow_l, fc = in_color, ec = out_color)

def MidTextSegment(segment, text, text_color): # Fica un text centrat en un segment
    # Centre del segment
    mid_x = (segment.origin_n.x + segment.dest_n.x) / 2
    mid_y = (segment.origin_n.y + segment.dest_n.y) / 2

    # Escriu text
    plt.text(mid_x, mid_y, text, fontsize=8, color=text_color, weight='bold', ha='center')

def Plot(g):
    # Dibuixa els nodes
    for n in g.nodes:
        plt.plot(n.x, n.y, 'o', color='red', markersize=5)
        # Escriu el nom dels nodes a dalt a la dreta
        plt.text(n.x + 0.5, n.y + 0.5, n.name, color='green', weight='bold', fontsize=6)
    # Dibuixa segments i mostra el que mesuren
    for s in g.segments:
        CreateNiceArrows(s, 'blue', 'blue', 'blue', 0.6, 0.4)
        MidTextSegment(s, round(s.cost, 2), 'black')

    plt.axis(ejesGrafico) # Estableix limits eixos
    plt.grid(color='red', linestyle='dashed', linewidth=0.5) # Dibuixa una graella pel fons
    plt.title('Gráfico con nodos y segmentos') # Fica titol
    plt.show() # Mostra grafic

def PlotNode (g, nameOrigin):
    node = next(n for n in g.nodes if n.name == nameOrigin) # Primer node que compleixi que el seu nom es igual a nameOrigin
    i = 1 # Comptador
    if node == None: # Si no s'ha trobat cap node la funcio acaba
        return False
    else: # Si s'ha trobat creara un segment entre els nodes veins del node i el node, a mes de dibuixar tots els nodes del Graph g
        for n in g.nodes:
            if n == node:
                plt.plot(n.x, n.y, 'o', color='blue', markersize=5) # Pinta el node principal de blau
            elif n in node.neighbors:
                plt.plot(n.x, n.y, 'o', color='green', markersize=5) # Pinta els nodes veins de verd
                # Crea fletxa per unir el node amb el vei
                s = Segment('Unión vecina' + str(i), node, n)
                i += 1
                CreateNiceArrows(s,'red','red','red',0.6,0.4)
                MidTextSegment(s, round(s.cost, 2), 'black')
            else:
                plt.plot(n.x, n.y, 'o', color='grey', markersize=5) # Pinta els nodes no veins de gris
            # Escriu el nom del node
            plt.text(n.x + 0.5, n.y + 0.5, n.name, color='green', weight='bold', fontsize=6)

        plt.axis(ejesGrafico)  # Estableix limits eixos
        plt.grid(color='red', linestyle='dashed', linewidth=0.5)  # Dibuixa una graella pel fons
        plt.title('Gráfico con nodos y segmentos')  # Fica titol
        plt.show()  # Mostra grafic
        return True

def GraphFile(filename):
    # Hi haura un text que marqui Node,x,y i un altre Segment,Origin,Destination
    g = Graph() # Es crea un Graph g on es guardaran totes les dades
    with open(filename, 'r') as file:
        lines = file.readlines() # Llista amb les linies del fitxer
    reading_nodes = True # Variable que determinara si esta llegint els nodes (True) o els segments (False)
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
            name = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            # Crea node i l'afegeix a g
            node = Node(name, x, y)
            g.nodes.append(node)
        else:
            # SEGMENTS:
            seg_name = parts[0]
            origin_name = parts[1]
            dest_name = parts[2]
            # Busca quin node te de nom el esmentat en el fitxer (tant d'origen com de desti)
            origin_node = next(n for n in g.nodes if n.name == origin_name)
            dest_node = next(n for n in g.nodes if n.name == dest_name)
            # Crea segment i l'afegeix a g
            segment = Segment(seg_name, origin_node, dest_node)
            g.segments.append(segment)
            # Afegeix el node desti com a vei del node origen
            origin_node.neighbors.append(dest_node)

    return g # Retorna el Graph