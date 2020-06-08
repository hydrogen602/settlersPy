from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .util import HexPoint, Biome
    # from mechanics.player import Player
    Player = None


class Settlement:

    def __init__(self, pos: HexPoint, owner: Player):
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
            'owner': self._owner
        }


class City(Settlement):

    def __init__(self, pos: HexPoint, owner: Player):
        super().__init__(pos, owner)
    
    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource, count=2)
