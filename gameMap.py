import json

from typing import List
from tools import typeCheck, customJsonEncoder
from features.tile import Tile
from mechanics.gameMap import ProducingOutpost
from point import HexPoint


class GameMap:

    def __init__(self, size: int = 3):
        self.__size: int = size
        self.tiles: List[Tile] = []
        self.settlements: List[ProducingOutpost] = []

        nP: int = (size - 1) / 2
        nP2: int = (size - 2) / 2

        for j in range(size):
            addition: int = int(-abs(j - nP) + nP)

            for i in range(-addition, size + addition):
                self.tiles.append(Tile.generate(HexPoint(2*j, 2*i)))
                # print(2*j, 2*i)

        for j in range(size - 1):
            addition: int = int(-abs(j - nP2) + nP2)

            for i in range(-addition, size + addition + 1):
                self.tiles.append(Tile.generate(HexPoint(2*j + 1, 2*i - 1)))
                # print(2*j + 1, 2*i - 1)
    
    def getTiles(self) -> List[Tile]:
        return self.tiles
    
    def getProducingOutposts(self) -> List[ProducingOutpost]:
        return self.settlements

    def addTile(self, t: Tile):
        typeCheck(t, Tile)
        self.tiles.append(t)

    def addSettlement(self, s: ProducingOutpost):
        typeCheck(s, ProducingOutpost)
        self.settlements.append(s)

    def getAsJson(self):
        return json.dumps(self, cls=customJsonEncoder)

# m = GameMap()
# print(json.dumps(m, cls=customJsonEncoder, indent=4))
