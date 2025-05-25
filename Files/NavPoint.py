class NavPoint:
    def __init__(self, number, name, lat, lon):
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon

def NavPointsFromFile(filename):
    NavPoints = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip()
            parts = parts.split()
            if line != "" and len(parts) == 4:
                NavPoints.append(NavPoint(parts[0]  , parts[1], float(parts[2]), float(parts[3])))
            else:
                continue
    return NavPoints