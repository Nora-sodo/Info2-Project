import math

class NavSegment:
    def __init__(self, o_number, d_number, dist):
        self.o_number = o_number
        self.d_number = d_number
        self.dist = dist

def NavSegmentsFromFile(filename):
    NavSegments = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip()
            parts = parts.split()
            if line != "" and len(parts) == 3:
                NavSegments.append(NavSegment(parts[0], parts[1], float(parts[2])))
            else:
                continue
    return NavSegments