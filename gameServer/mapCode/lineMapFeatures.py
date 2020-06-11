
from typing import Dict

from .util import HexPoint, isNotNone, JsonSerializable, Resource
from .baseMapFeatures import Placeable, Ownable
from ..playerCode.player import Player
from ..playerCode.playerAction import Purchaseable

class Road(Placeable, Purchaseable, Ownable, JsonSerializable):

    def __init__(self, point1: HexPoint = None, point2: HexPoint = None, **kwargs) -> None:
        isNotNone('__init__', point1=point1, point2=point2)
        super().__init__(**kwargs)

        self.__point1: HexPoint = point1
        self.__point2: HexPoint = point2

        self.setupPurchase(Road, {
            Resource.Lumber: 1,
            Resource.Brick: 1
        }, isLineFeature=True)

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
            **super().toJsonSerializable()
        }