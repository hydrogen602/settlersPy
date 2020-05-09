
import json

from typing import List
from tools import typeCheck, customJsonEncoder

import mechanics.gameMap as gameMap

from point import HexPoint


class GameMap:

    def __init__(self, tiles: List[gameMap.TileMapFeature]):
        self.__tiles = tiles
        self._mapElements = []

    def addMapElement(self, elem: gameMap.MapFeature):
        self._mapElements.append(elem)

    # def getAsJson(self):
    #     return json.dumps(self, cls=customJsonEncoder)
