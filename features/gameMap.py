import json

from typing import List
from tools import typeCheck, customJsonEncoder

import mechanics.gameMap as gameMap
import mechanics.util as util

from .tile import Tile

from point import HexPoint

class GameMap:

    def __init__(self, tiles: List[Tile]):
        self.__tilesMap: List[Tile] = tiles

        self.__cornerElems: List[gameMap.CornerMapFeature] = []
        self.__lineElems: List[gameMap.LineMapFeature] = []

        self.__tileElems: List[gameMap.TileMapFeature] = []
        '''
        This is for things that go on top of the map tiles
        '''
    
    def addProducingOutput(self, elem: gameMap.ProducingOutpost):
        self.__cornerElems.append(elem)
    
    def addCornerElem(self, elem: gameMap.CornerMapFeature):
        self.__cornerElems.append(elem)
    
    def addLineElem(self, elem: gameMap.LineMapFeature):
        self.__lineElems.append(elem)
    
    def addTileElem(self, elem: gameMap.TileMapFeature):
        self.__tileElems.append(elem)

    # def getAsJson(self):
    #     return json.dumps(self, cls=customJsonEncoder)