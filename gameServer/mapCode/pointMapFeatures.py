from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from ..extraCode.modifiers import Placeable, Ownable, Purchaseable
from ..extraCode.util import isNotNone, JsonSerializable, ArgumentMissingError, NotSetupException, AlreadySetupException
from ..extraCode.location import Resource

if TYPE_CHECKING:
    from ..extraCode.location import HexPoint, Biome
    from ..playerCode.player import Player
    from ..playerCode.turn import Turn

class Settlement(Placeable, Purchaseable, Ownable, JsonSerializable):

    _cost: Dict[Resource, int] = {
        Resource.Brick: 1,
        Resource.Lumber: 1,
        Resource.Sheepie: 1,
        Resource.Wheat: 1
    }

    _isPointFeature = True

    def __init__(self, pos: Optional[HexPoint] = None, **kwargs) -> None:
        self._pos: Optional[HexPoint] = pos

        hasLocation = False
        if pos is not None:
            hasLocation = True

        super().__init__(isPlaced=hasLocation, **kwargs)

    def __str__(self):
        if self._isPlaced:
            return f"Settlement({self._pos})"
        else:
            return f"Settlement()"
    
    def place(self, position: HexPoint, turn: Turn):
        if self._isPlaced:
            raise AlreadySetupException("This settlement has already been placed")

        self._pos = position.copy()

        turn.gameMap.addPointElement(self, turn) # raises ActionError

        self._place()

    @property
    def position(self) -> HexPoint:
        if self._pos is None:
            raise NotSetupException("This settlement hasn't been given a location yet")
        return self._pos

    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource)

    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'position': self._pos,
            **super().toJsonSerializable()
        }


class City(Settlement):

    _cost = {
        Resource.Ore: 3,
        Resource.Wheat: 2
    }

    _isPointFeature = True

    def harvestResource(self, biome: Biome):
        self._owner.giveResource(biome.primaryResource, count=2)
    
    def __str__(self):
        if self._isPlaced:
            return f"City({self._pos})"
        else:
            return f"City()"
