from __future__ import annotations

from typing import TYPE_CHECKING, List
from abc import abstractmethod

from mechanics.gameMap.mapFeature import CornerMapFeature
from tools import requireNotNone

if TYPE_CHECKING:
    from point import HexPoint
    from mechanics.player import Player
    #from tile import Tile
    from biome import Biome


class ProducingOutpost(CornerMapFeature):
    '''
    Any settlement or city or whatever that
    lives on a corner of a tile and produces resources
    based on the surrounding tiles
    '''

    def __init__(self, point: HexPoint, owner: Player):
        requireNotNone(owner)
        super().__init__(point)
        self.__owner: Player = owner
    
    @property
    def owner(self) -> Player:
        return self.__owner
    
    @abstractmethod
    def harvestResource(self, biome: Biome):
        '''
        Called when a nearby tile produces resources
        '''
        ...

