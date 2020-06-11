from __future__ import annotations
from enum import Enum
from typing import Dict, Iterable, Tuple, List

from .util import IterableCls



class HexPoint:
    def __init__(self, row: int, col: int) -> None:
        self.__row: int = row
        self.__col: int = col
    
    def toJsonSerializable(self) -> Dict[str, int]:
        return {'row': self.__row, 'col': self.__col}

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col
    
    def getAsTuple(self) -> Tuple[int, int]:
        return (self.__row, self.__col)
    
    def __add__(self, other: HexPoint) -> HexPoint:
        return HexPoint(self.row + other.row, self.col + other.col)

    def __sub__(self, other: HexPoint) -> HexPoint:
        return HexPoint(self.row - other.row, self.col - other.col)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HexPoint):
            return False
        return self.row == other.row and self.col == other.col
    
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, HexPoint):
            return True
        return self.row != other.row or self.col != other.col


class Resource(Enum):
    Wheat = 0
    Sheepie = 1
    Lumber = 2
    Ore = 3
    Brick = 4


class Biome(metaclass=IterableCls):
    __biomeList: Dict[str, Biome] = {}

    def __init__(self, name: str, primaryResource: Resource, color: str) -> None:
        '''
        Create a new biome. The instance doesn't have to be kept track
        of as the class will remember its instances
        '''
        self.__biomeName: str = name
        self.__primaryResource: Resource = primaryResource
        self.__color: str = color

        Biome.__biomeList[name] = self
    
    @classmethod
    def getBiomeDict(cls) -> Dict[str, Biome]:
        '''
        Returns the dict containing all the biomes
        created so far
        '''
        return cls.__biomeList
    
    @classmethod
    def getBiomeList(cls) -> List[Biome]:
        '''
        Returns a list of all the biomes
        created so far
        '''
        return list(cls.__biomeList.values())
    
    @classmethod
    def getIterable(cls) -> Iterable[str]:
        '''
        For the `IterableCls` metaclass.
        This helps in making `Biome` iterable
        '''
        return cls.__biomeList

    @property
    def name(self) -> str:
        return self.__biomeName
    
    @property
    def primaryResource(self) -> Resource:
        return self.__primaryResource
    
    @property
    def color(self) -> str:
        return self.__color
    
    def __repr__(self) -> str:
        return f'Biome({self.__biomeName}, {self.__primaryResource}, {self.__color})'

    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'name': self.__biomeName,
            'primaryResource': self.__primaryResource,
            'color': self.__color
        }


Biome('farmland', Resource.Wheat, 'goldenrod')
Biome('grassland', Resource.Sheepie, 'limegreen')
Biome('forest', Resource.Lumber, 'forestgreen')
Biome('mountain', Resource.Ore, 'dimgray')
Biome('quarry', Resource.Brick, 'firebrick')
