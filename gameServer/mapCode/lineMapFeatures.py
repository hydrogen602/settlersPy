
from typing import Dict

from .util import HexPoint, isNotNone, JsonSerializable
from .baseMapFeatures import Placeable
from ..playerCode.player import Player

class Road(Placeable, JsonSerializable):

    def __init__(self, point1: HexPoint = None, point2: HexPoint = None, owner: Player = None, **kwargs) -> None:
        isNotNone('__init__', point1=point1, point2=point2, owner=owner)
        super().__init__(**kwargs)

        self.__point1: HexPoint = point1
        self.__point2: HexPoint = point2
        self._owner: Player = owner

    @property
    def point1(self) -> HexPoint: 
        return self.__point1
    
    @property
    def point2(self) -> HexPoint: 
        return self.__point2
    
    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'point1': self.__point1,
            'point2': self.__point2,
            'owner': self._owner,
            **super().toJsonSerializable()
        }