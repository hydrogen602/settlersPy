
from typing import List
from tools import typeCheck
from tile import Tile
from habitation import Habitation

class Map:

    def __init__(self, n: int = 3):
        self.__n = n
        self.tiles: List[Tile] = []
        self.settlements: List[Habitation] = []
    
    def addTile(self, t: Tile):
        typeCheck(t, Tile)
        self.tiles.append(t)
    
    def addSettlement(self, s: Habitation):
        typeCheck(s, Habitation)
        self.settlements.append(s)
    

