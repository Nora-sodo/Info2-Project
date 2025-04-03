import math

class Node:
    def __init__(self, name,x,y):
        self.name = name    # Nom
        self.x = float(x)   # Punt x
        self.y = float(y)   # Punt y
        self.neighbors = [] # Llista de veins

def AddNeighbor(n1, n2): # Afegeix n2 a la llista de veins de n1
    if n2 in n1.neighbors:
        return True
    else:
        n1.neighbors.append(n2)
        return False

def Distance(n1, n2): # Determina la distancia entre n1 i n2
    # Increment de distancia entre eixos
    dx = n1.x - n2.x
    dy = n1.y - n2.y
    return math.sqrt(dx**2 + dy**2)
