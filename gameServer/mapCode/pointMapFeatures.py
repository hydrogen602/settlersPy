from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .baseMapFeatures import Placeable
from .util import isNotNone, JsonSerializable

if TYPE_CHECKING:
    from .util import HexPoint, Biome
    from ..playerCode.player import Player


class Settlement(Placeable, JsonSerializable):

    def __init__(self, pos: HexPoint = None, owner: Player = None, **kwargs) -> None:
        isNotNone('__init__', pos=pos, owner=owner)
        super().__init__(**kwargs)
        self._pos: HexPoint = pos
        self._owner: Player = owner

    @property
    def position(self) -> HexPoint:
        return self._pos

    @property
    def owner(self) -> Player:
        return self._owner

    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource)

    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'position': self._pos,
            'owner': self._owner,
            **super().toJsonSerializable()
        }


class City(Settlement):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource, count=2)
