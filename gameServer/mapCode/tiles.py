from __future__ import annotations

from typing import Set, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .pointMapFeatures import Settlement

from ..extraCode.location import Biome, HexPoint
from ..playerCode.turn import Turn


class Tile:
    __diceValueChoices = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12]

    def __init__(self, biome: Biome, dieValue: int, position: HexPoint) -> None:
        '''
        Represents one tile on the map.
        diceValue is the number that needs to be rolled for
        resources to be harvested and should be within 2 to 12, inclusive
        '''

        self._biome: Biome = biome
        self._position: HexPoint = position
        
        #checks that the dice value is an instance of an Int 
        if not isinstance(dieValue, int):
            raise TypeError(f'Expected type int but got {type(dieValue)} in argument dieValue')
        #checks that the diceValue is between 2-12
        if not dieValue >= 2 and dieValue <= 12:
            raise ValueError(f'Invalid dieValue, got {dieValue} but expected in range [2, 12], inclusive')

        self.__isBlockedByRobber: bool = False

        self.__diceValue: int = dieValue 

        self.__settlementList: Set[HexPoint] = set()
    
    def __str__(self):
        return f'Tile({self._position}, {self._biome.name},  {self.__diceValue})'
    
    @property
    def position(self) -> HexPoint:
        return self._position
    
    @property
    def biome(self) -> Biome:
        return self._biome
    
    @property
    def diceValue(self) -> int:
        return self.__diceValue

    @classmethod
    def generate(cls, position: HexPoint) -> Tile:
        dieValue: int = random.choice(cls.__diceValueChoices)
        biome: Biome = random.choice(Biome.getBiomeList())
        return cls(biome, dieValue, position)
    
    def toJsonSerializable(self):
        return {
            'biome': self._biome.name,
            'diceValue': self.__diceValue,
            'location': self._position,
            'isDisabledByRobber': self.__isBlockedByRobber
        }

    def addSettlement(self, settlement: Settlement):
        '''
        Adds a settlement to the tile.
        If a settlement is placed, then this method
        should be called on all neighboring tiles
        so that when the die are rolled the tiles
        know who to give resources to.
        '''
        self.__settlementList.add(settlement.position)

    def robberArrives(self):
        self.__isBlockedByRobber = True

    def robberDeparts(self):
        self.__isBlockedByRobber = False

    def isRobberHere(self) -> bool:
        return self.__isBlockedByRobber

    def diceRolled(self, valueRolled: int, turn: Turn):
        '''
        Call this method on all tiles when the die
        are rolled for giving resources.
        '''
        if not isinstance(valueRolled, int):
            raise TypeError(f'Expected int but got {type(valueRolled)} in argument valueRolled')
        if valueRolled < 2 or valueRolled > 12:
            raise ValueError(f'Invalid dieValue, got {valueRolled} but expected in range [2, 12], inclusive')

        if self.__isBlockedByRobber:
            # nothing is produced if robbers are here
            return

        if valueRolled == self.__diceValue:
            for hp in self.__settlementList:
                settlementRef = turn.gameMap.getPointFeature(hp)

                if not settlementRef:
                    raise ValueError("Invalid state: Tile has point which contains no point feature")
                
                settlementRef.harvestResource(self._biome)
                
