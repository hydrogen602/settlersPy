from __future__ import annotations

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.gameMap.advancedMapFeature import ProducingOutpost

from mechanics.gameMap.mapFeature import TileMapFeature
from biome import Biome
from point import HexPoint

import random

from tools import typeCheck, subclassCheck


class Tile(TileMapFeature):

    def __init__(self, biome: Biome, dieValue: int, location: HexPoint):
        '''
        Represents one tile on the map.
        diceValue is the number that needs to be rolled for
        resources to be harvested
        '''
        subclassCheck(biome, Biome)
        self.__biome: Biome = biome
        #checks that the dice value is an instance of an Int 
        typeCheck(dieValue, int)
        #checks that the diceValue is between 2-12
        if not dieValue >= 2 and dieValue <= 12:
            raise ValueError(f'Invalid dieValue, got {dieValue} but expected in range [2, 12], inclusive')

        self.__isBlockedByRobber: bool = False

        self.__diceValue: int = dieValue 
        self.__settlementList: List[ProducingOutpost] = []

        super().__init__(location)

    @property
    def owner(self) -> None:
        '''
        required to be implemented by the abstract base class.
        Returns `None` as `Tile` has no owner
        '''
        return None

    @classmethod
    def generate(cls, location: HexPoint) -> Tile:
        dieValue: int = random.randint(2, 12)
        biome: Biome = random.choice(Biome.biomeList)
        return cls(biome, dieValue, location)
    
    def toJsonSerializable(self):
        return {
            'biome': self.__biome.__name__,
            'diceValue': self.__diceValue,
            'location': self.point
        }

    def addSettlement(self, settlement: ProducingOutpost):
        '''
        Adds a settlement to the tile.
        If a settlement is placed, then this method
        should be called on all neighboring tiles
        so that when the die are rolled the tiles
        know who to give resources to.
        '''
        self.__settlementList.append(settlement)

    def robberArrives(self):
        self.__isBlockedByRobber = True

    def robberDeparts(self):
        self.__isBlockedByRobber = False

    def isRobberHere(self) -> bool:
        return self.__isBlockedByRobber

    def diceRolled(self, valueRolled: int):
        '''
        Call this method on all tiles when the die
        are rolled for giving resources.
        '''
        # diceValueChoices = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12]
        typeCheck(valueRolled, int)

        if self.__isBlockedByRobber:
            return

        if valueRolled == self.__diceValue:
            for s in self.__settlementList:
                s.harvestResource(self.__biome)
