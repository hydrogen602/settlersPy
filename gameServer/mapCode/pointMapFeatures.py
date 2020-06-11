from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .baseMapFeatures import Placeable, Ownable
from .util import isNotNone, JsonSerializable, Resource
from ..playerCode.playerAction import Purchaseable

if TYPE_CHECKING:
    from .util import HexPoint, Biome
    from ..playerCode.player import Player


class Settlement(Placeable, Purchaseable, Ownable, JsonSerializable):

    def __init__(self, pos: HexPoint = None, **kwargs) -> None:
        isNotNone('__init__', pos=pos)
        super().__init__(**kwargs)
        self._pos: HexPoint = pos

        self.setupPurchase(Settlement, {
            Resource.Brick: 1,
            Resource.Lumber: 1,
            Resource.Sheepie: 1,
            Resource.Wheat: 1
        }, isPointFeature=True)

    @property
    def position(self) -> HexPoint:
        return self._pos

    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource)

    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'position': self._pos,
            **super().toJsonSerializable()
        }


class City(Settlement):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.setupPurchase(City, {
            Resource.Ore: 3,
            Resource.Wheat: 2
        }, isPointFeature=True)

    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource, count=2)
