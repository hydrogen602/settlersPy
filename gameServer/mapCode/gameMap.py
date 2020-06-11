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

    def __init__(self, tiles: List[Tile]) -> None:
        self.__tiles: Dict[Tuple[int, int], Tile] = {}
        for t in tiles:
            self.__tiles[t.position.getAsTuple()] = t
        
        self.__pointFeatures: List[Settlement] = []
        self.__lineFeatures: List[Road] = []

        self.__robberPosition: Union[HexPoint, None] = None
    
    def generateHexagonalArea(self, size: int, startPoint: HexPoint = HexPoint(0, 0)):
        nP: float = (size - 1) / 2
        nP2: float = (size - 2) / 2

        for j in range(size):
            addition: int = int(-abs(j - nP) + nP)

            for i in range(-addition, size + addition):
                self.addTile(
                    Tile.generate(
                        HexPoint(2*j, 2*i) + startPoint
                    )
                )

        for j in range(size - 1):
            addition = int(-abs(j - nP2) + nP2)

            for i in range(-addition, size + addition + 1):
                self.addTile(
                    Tile.generate(
                        HexPoint(2*j + 1, 2*i - 1) + startPoint
                    )
                )
    
    def moveRobber(self, position: HexPoint):
        '''
        moves the robber from the last recorded postion
        to the new position. Calls robberDeparts()
        on the old tile and robberArrives() on the new
        tile. If the robber doesn't have a location yet,
        no attempt will be made to get the old tile
        as that would result in a KeyError
        '''

        if self.__robberPosition is not None:
            oldTile = self.getTile(self.__robberPosition)
            oldTile.robberDeparts()
        

        newTile = self.getTile(position)
        newTile.robberArrives()

        self.__robberPosition = position

    def addTile(self, elem: Tile):
        '''
        Add a tile to the map. Tiles cannot
        be placed where there already is a tile.
        '''
        key = elem.position.getAsTuple()
        if key in self.__tiles:
            raise KeyError(f'A tile already exists at postion {key}')
        self.__tiles[key] = elem

    def getTile(self, position: HexPoint) -> Tile:
        '''
        Fetches a tile from the map given the postion
        '''
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
