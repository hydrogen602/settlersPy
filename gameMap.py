import json

from typing import List
from tools import typeCheck, customJsonEncoder
from tile import Tile
from habitation import Habitation
from point import HexPoint

class GameMap:

    def __init__(self, size: int = 3):
        self.__size = size
        self.tiles: List[Tile] = []
        self.settlements: List[Habitation] = []

        nP: int = (size - 1) // 2
        nP2: int = (size - 2) // 2

        for j in range(size):    
            addition: int = -abs(j - nP) + nP

            for i in range(-addition, size + addition):
                self.tiles.append(Tile.generate(HexPoint(2*j, 2*i)))

        for j in range(size - 1):
            addition: int = -abs(j - nP2) + nP2

            for i in range(-addition, size + addition + 1):
                self.tiles.append(Tile.generate(HexPoint(2*j + 1, 2*i - 1)))

    def addTile(self, t: Tile):
        typeCheck(t, Tile)
        self.tiles.append(t)

    def addSettlement(self, s: Habitation):
        typeCheck(s, Habitation)
        self.settlements.append(s)
    
    def getAsJson(self):
        return json.dumps(self, cls=customJsonEncoder)

# m = GameMap()
# print(json.dumps(m, cls=customJsonEncoder, indent=4))
