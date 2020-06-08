from __future__ import annotations
from typing import Dict, List, Iterable
from enum import Enum


class HexPoint:
    def __init__(self, col: int, row: int):
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


class Resource(Enum):
    Wheat = 0
    Sheepie = 1
    Lumber = 2
    Ore = 3
    Brick = 4


class IterableCls(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'getIterable'):
            raise TypeError(f'IterableCls {name} must have method getIterable')

    def __iter__(cls):
        return iter(cls.getIterable())
    
    def __getitem__(cls, key):
        return cls.getIterable()[key]


class Biome(metaclass=IterableCls):
    __biomeList: Dict[str, Biome] = {}

    def __init__(self, name: str, primaryResource: Resource, color: str):
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
