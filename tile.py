from __future__ import annotations

from biome import Biome
from habitation import Habitation
from point import HexPoint

import random

from tools import typeCheck, subclassCheck
from typing import List

class Tile:

    def __init__(self, biome: Biome, dieValue: int, location: HexPoint):
        '''
        Represents one tile on the map.
        diceValue is the number that needs to be rolled for
        resources to be harvested
        '''
        subclassCheck(biome, Biome)
        self.biome: Biome = biome
        #checks that the dice value is an instance of an Int 
        typeCheck(dieValue, int)
        #checks that the diceValue is between 2-12
        assert dieValue >= 2 and dieValue <= 12

        self.isBlockedByRobber: bool = False

        self.diceValue: int = dieValue 
        self.settlementList: List[Habitation] = []

        typeCheck(location, HexPoint)
        self.location = location

    @classmethod
    def generate(cls, location: HexPoint) -> Tile:
        dieValue: int = random.randint(2, 12)
        biome: Biome = random.choice(Biome.biomeList)
        return cls(biome, dieValue, location)
    
    def toJsonSerializable(self):
        return {
            'biome': self.biome.__name__,
            'diceValue': self.diceValue,
            'location': self.location
        }

    def addSettlement(self, settlement: Habitation):
        '''
        Adds a settlement to the tile.
        If a settlement is placed, then this method
        should be called on all neighboring tiles
        so that when the die are rolled the tiles
        know who to give resources to.
        '''
        typeCheck(settlement, Habitation)
        self.settlementList.append(settlement)

    def robberArrives(self):
        self.isBlockedByRobber = True

    def robberDeparts(self):
        self.isBlockedByRobber = False

    def isRobberHere(self) -> bool:
        return self.isBlockedByRobber

    def diceRolled(self, valueRolled: int):
        '''
        Call this method on all tiles when the die
        are rolled for giving resources.
        '''
        # diceValueChoices = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12]
        typeCheck(valueRolled, int)

        if self.isBlockedByRobber:
            return

        if valueRolled == self.diceValue:
            for s in self.settlementList:
                s.giveResource(self.biome)
