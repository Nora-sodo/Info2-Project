from node import *

class Segment:
    def __init__(self,name, origin_n, dest_n):
        self.name = name                                # Nom
        self.origin_n = origin_n                        # Origen
        self.dest_n = dest_n                            # Final
        self.cost = float(Distance(origin_n, dest_n))   # Modul segment