import copy

class NavAirport:
    def __init__(self, name):
        self.name = name
        self.sid = []
        self.star = []

def NavAirportsFromFile(filename):
    NavAirports = []
    count = 0
    actual_airport = NavAirport('')
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip()
            parts = parts.split('.')
            if len(parts) == 1:
                if count > 0:
                    NavAirports.append(copy.copy(actual_airport))
                actual_airport.name = parts[0]
            elif len(parts) == 2:
                if parts[1] == 'D':
                    actual_airport.sid.append(line)
                elif parts[1] == 'A':
                    actual_airport.star.append(line)
            else:
                continue
            count += 1
    return NavAirports