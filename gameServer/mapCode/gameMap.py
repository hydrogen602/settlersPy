from __future__ import annotations

from typing import List, Dict, Tuple, Union, TYPE_CHECKING
#from tools import customJsonEncoder

if TYPE_CHECKING:
    # from mechanics.player import Player
    Player = None
    from .tiles import Tile
    from .pointMapFeatures import Settlement
    from .lineMapFeatures import Road

from .util import HexPoint


class GameMap:

    def __init__(self, tiles: List[Tile]):
        self.__tiles: Dict[Tuple[int, int], Tile] = {}
        for t in tiles:
            self.__tiles[t.position.getAsTuple()] = t
        
        self.__pointFeatures: List[Settlement] = []
        self.__lineFeatures: List[Road] = []

        self.__robberPosition: Union[HexPoint, None] = None
    
    def moveRobber(self, position: HexPoint):
        # this can cause a crash if there is no tile at (0, 0)

        if self.__robberPosition is not None:
            oldTile = self.getTile(self.__robberPosition)
            oldTile.robberDeparts()
        

        newTile = self.getTile(position)
        newTile.robberArrives()

        self.__robberPosition = position

    def addTile(self, elem: Tile):
        key = elem.position.getAsTuple()
        if key in self.__tiles:
            raise KeyError(f'A tile already exists at postion {key}')
        self.__tiles[key] = elem

    def getTile(self, position: HexPoint) -> Tile:
        key = position.getAsTuple()
        if key not in self.__tiles:
            raise KeyError(f'No tile found at postion {key}')
        return self.__tiles[position.getAsTuple()]

    def addPointElement(self, elem: Settlement):
        self.__pointFeatures.append(elem)
    
    def addLineElement(self, elem: Road):
        self.__lineFeatures.append(elem)
    
    def toJsonSerializable(self):
        pass
        r = {
            'tiles': [t.toJsonSerializable() for t in self.__tiles.values()],

        }

    # def getAsJson(self):
    #     return json.dumps(self, cls=customJsonEncoder)
