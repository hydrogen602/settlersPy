from __future__ import annotations

from biome import Biome
from habitation import Habitation

import random

from tools import typeCheck
from typing import List

class Tile:

    def __init__(self, biome: Biome, dieValue: int):
        '''
        Represents one tile on the map.
        diceValue is the number that needs to be rolled for
        resources to be harvested
        '''
        typeCheck(biome, Biome)
        self.biome: Biome = biome
        #checks that the dice value is an instance of an Int 
        typeCheck(dieValue, int)
        #checks that the diceValue is between 2-12
        assert dieValue >= 2 and dieValue <= 12

        self.isBlockedByRobber: bool = False

        self.diceValue: int = dieValue 
        self.settlementList: List[Habitation] = []
    
    @classmethod
    def generate(cls) -> Tile:
        dieValue: int = random.randint(2, 12)
        biome: Biome = random.choice(Biome.biomeList)
        return cls(biome, dieValue)

    
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
        
    def diceRolled (self, valueRolled: int):
        '''
        Call this method on all tiles when the die
        are rolled for giving resources.
        '''
        typeCheck(valueRolled, int)
        
        if self.isBlockedByRobber:
            return
        
        if valueRolled == self.diceValue:
            for s in self.settlementList:
                s.giveResource(self.biome)
