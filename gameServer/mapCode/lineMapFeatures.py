
from typing import Dict, Optional

from ..extraCode.location import HexPoint, Resource
from ..extraCode.util import isNotNone, JsonSerializable, ArgumentMissingError, NotSetupException, AlreadySetupException
from ..extraCode.modifiers import Placeable, Ownable, Purchaseable
from ..playerCode.player import Player
from ..playerCode.turn import Turn

class Road(Placeable, Purchaseable, Ownable, JsonSerializable):

    _cost = {
        Resource.Lumber: 1,
        Resource.Brick: 1
    }

    _isLineFeature = True

    def __init__(self, point1: HexPoint = None, point2: HexPoint = None, **kwargs) -> None:
        '''
        If both point1 and point2 are None, then it assumes that this is an unplaced Road.
        If both are not None, this is a placed road
        '''
        self.__point1: Optional[HexPoint] = point1
        self.__point2: Optional[HexPoint] = point2

        hasLocation = False
        if point1 is not None and point2 is not None:
            # fully specified
            hasLocation = True
        elif point1 is not None:
            # specified only point1
            raise ArgumentMissingError('__init__', 'point2')
        elif point2 is not None:
            # specified only point2
            raise ArgumentMissingError('__init__', 'point1')
        
        super().__init__(isPlaced=hasLocation, **kwargs)

    def __str__(self):
        if self._isPlaced:
            return f"Road({self.__point1, self.__point2})"
        else:
            return f"Road()"
    
    def place(self, point1: HexPoint, point2: HexPoint, turn: Turn):
        if self._isPlaced:
            raise AlreadySetupException("This road has already been placed")

        self.__point1 = point1.copy()
        self.__point2 = point2.copy()

        turn.gameMap.addLineElement(self, turn) # raises ActionError

        self._place()

    @property
    def point1(self) -> HexPoint:
        if self.__point1 is None:
            raise NotSetupException("This road hasn't been given a position yet")
        return self.__point1
    
    @property
    def point2(self) -> HexPoint:
        if self.__point2 is None:
            raise NotSetupException("This road hasn't been given a position yet")
        return self.__point2
    
    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'point1': self.__point1,
            'point2': self.__point2,
            **super().toJsonSerializable()
        }