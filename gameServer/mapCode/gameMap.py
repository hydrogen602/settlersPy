from __future__ import annotations

from typing import List, Dict, Tuple, Optional, TYPE_CHECKING, Union
import json

if TYPE_CHECKING:
    from ..playerCode.player import Player
    from ..playerCode.turn import Turn
    
from .tiles import Tile
from .pointMapFeatures import Settlement
from .lineMapFeatures import Road
from ..extraCode import HexPoint, JsonSerializable, ActionError, customJsonEncoder

class GameMap(JsonSerializable):

    def __init__(self, tiles: List[Tile] = []) -> None:
        self.__tiles: Dict[Tuple[int, int], Tile] = {}
        for t in tiles:
            self.__tiles[t.position.getAsTuple()] = t
        
        self.__pointFeatures: Dict[Tuple[int, int], Settlement] = {}
        self.__lineFeatures: Dict[Tuple[Tuple[int, int], Tuple[int, int]], Road] = {}

        self.__robberPosition: Optional[HexPoint] = None
    
    @property
    def tiles(self) -> List[Tile]:
        return list(self.__tiles.values())
    
    @property
    def pointFeatures(self) -> List[Settlement]:
        return list(self.__pointFeatures.values())
    
    @property
    def lineFeatures(self) -> List[Road]:
        return list(self.__lineFeatures.values())
    
    def generateHexagonalArea(self, size: int, startPoint: HexPoint = HexPoint(0, 0)):
        nP: float = (size - 1) / 2
        nP2: float = (size - 2) / 2

        for j in range(size):
            addition: int = int(-abs(j - nP) + nP)

            for i in range(-addition, size + addition):
                self.addTile(
                    Tile.generate(
                        HexPoint(2*i, 2*j) + startPoint
                    )
                )

        for j in range(size - 1):
            addition = int(-abs(j - nP2) + nP2)

            for i in range(-addition, size + addition + 1):
                self.addTile(
                    Tile.generate(
                        HexPoint(2*i - 1, 2*j + 1) + startPoint
                    )
                )
    
    # def isLegalPosition(self, thing: Union[Road, Settlement]):
    #     if isinstance(thing, Road):
    #         r: Road = thing

    #     elif isinstance(thing, Settlement): # TODO
    #         s: Settlement = thing
        
    #     else:
    #         raise TypeError(f"Argument of wrong type, got {type(thing)}, but expected Union[Road, Settlement]")
    
    def moveRobber(self, position: HexPoint):
        '''
        moves the robber from the last recorded postion
        to the new position. Calls robberDeparts()
        on the old tile and robberArrives() on the new
        tile. If the robber doesn't have a location yet,
        no attempt will be made to get the old tile
        as that would result in a KeyError.

        Raises a `KeyError` if no tile exists at position. 
        '''

        newTile = self.getTile(position)
        # if the tile does not exist, nothing else should change about the map
        if newTile is None:
            return ActionError("No tile found at given position")

        if self.__robberPosition is not None:
            oldTile = self.getTile(self.__robberPosition)
            if oldTile is None:
                raise RuntimeError("This shouldn't happen")
            oldTile.robberDeparts()
        
        newTile.robberArrives()

        self.__robberPosition = position

    def addTile(self, elem: Tile):
        '''
        Add a tile to the map. Tiles cannot
        be placed where there already is a tile.
        Raises a `KeyError` if the tile already exists.
        '''
        key = elem.position.getAsTuple()
        if key in self.__tiles:
            raise KeyError(f'A tile already exists at postion {key}')
        self.__tiles[key] = elem

    def getTile(self, position: HexPoint) -> Optional[Tile]:
        '''
        Fetches a tile from the map given the postion.
        Returns `None` if the tile does not exist
        '''
        key = position.getAsTuple()
        if key not in self.__tiles:
            return None
            #raise KeyError(f'No tile found at postion {key}')
        return self.__tiles[position.getAsTuple()]
    
    def __contains__(self, position: HexPoint) -> bool:
        '''
        For checking if a tile exists at some point
        '''
        return position.getAsTuple() in self.__tiles

    def addPointElement(self, elem: Settlement, turn: Turn):
        point: Tuple[int, int] = elem.position.getAsTuple()

        if elem.owner != turn.currentPlayer:
            raise ActionError("Things may only be placed on your turn")

        if point in self.__pointFeatures:
            raise ActionError("A settlement exists here already")

        # check neighbors -> there must be none
        neighbors: List[Tuple[int, int]] = [p.getAsTuple() for p in elem.position.getNeighbors()]

        for n in neighbors:
            if n in self.__pointFeatures:
                raise ActionError("Too close to other settlement, needs at least one space in between")

        if turn.roundNum >= 2:
            # check for roads -> there must be one of owner
            foundOwnedRoad = False
            for p in neighbors:
                if (point, p) in self.__lineFeatures and self.__lineFeatures[(point, p)].owner == elem.owner:
                    foundOwnedRoad = True
                    break
                if (p, point) in self.__lineFeatures and self.__lineFeatures[(p, point)].owner == elem.owner:
                    foundOwnedRoad = True
                    break
            
            if not foundOwnedRoad:
                raise ActionError("Settlements must be connected to an owned road")
        
        adjacentTiles: Tuple[HexPoint, HexPoint, HexPoint] = elem.position.getNeighboringTiles()
        
        foundOne = False
        for hp in adjacentTiles:
            t = self.getTile(hp)
            if t is not None:
                foundOne = True
                t.addSettlement(elem)

            pass # self.g
        
        if not foundOne:
            # not next to any tiles, so in the ocean
            raise ActionError("Settlement not placed on map")

        self.__pointFeatures[point] = elem
    
    def addLineElement(self, elem: Road, turn: Turn):
        p1: Tuple[int, int] = elem.point1.getAsTuple()
        p2: Tuple[int, int] = elem.point2.getAsTuple()

        if elem.owner != turn.currentPlayer:
            raise ActionError("Things may only be placed on your turn")

        if (p1, p2) in self.__lineFeatures or (p2, p1) in self.__lineFeatures:
            # remember to check both orders
            raise ActionError("A road exists here already")

        if not elem.point1.isNeighbor(elem.point2):
            raise ActionError("A road cannot be placed between these points")

        neighbors1: List[Tuple[int, int]] = [p.getAsTuple() for p in elem.point1.getNeighbors()]
        neighbors2: List[Tuple[int, int]] = [p.getAsTuple() for p in elem.point2.getNeighbors()]

        # check for connection to road or settlement
        foundOwnedConnection = False
        for nGroup, point in ((neighbors1, p1), (neighbors2, p2)):
            if point in self.__pointFeatures and self.__pointFeatures[point].owner == elem.owner:
                foundOwnedConnection = True
                break

            for n in nGroup:
                if (point, n) in self.__lineFeatures and self.__lineFeatures[(point, n)].owner == elem.owner:
                    foundOwnedConnection = True
                    break
                if (n, point) in self.__lineFeatures and self.__lineFeatures[(n, point)].owner == elem.owner:
                    foundOwnedConnection = True
                    break
            if foundOwnedConnection:
                break
        
        if not foundOwnedConnection:
            raise ActionError("Roads must be connected to an owned road or settlement")

        self.__lineFeatures[(p1, p2)] = elem
    
    def toJsonSerializable(self):
        '''
        Format:
        {
            'tiles': List[Tile],
            'points': List[Settlement],
            'lines': List[Road]
        }
        '''
        return {
            'tiles': self.tiles,
            'points': self.pointFeatures,
            'lines': self.lineFeatures,
            **super().toJsonSerializable()
        }

    def getAsJson(self):
        return json.dumps(self, cls=customJsonEncoder)
