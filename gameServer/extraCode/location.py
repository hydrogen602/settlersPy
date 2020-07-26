from __future__ import annotations
from enum import Enum
from typing import Dict, Iterable, Tuple, List

from .util import IterableCls, JsonSerializable


class HexPoint(JsonSerializable):
    def __init__(self, row: int, col: int) -> None:
        self.__row: int = row
        self.__col: int = col
    
    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'row': self.__row, 
            'col': self.__col,
            **super().toJsonSerializable()
            }
    
    @classmethod
    def fromJson(cls, o: Dict[str, str]) -> HexPoint:
        if o.get('__name__') != 'HexPoint':
            raise SyntaxError('Wrong __name__ property')
        if 'row' not in o or 'col' not in o:
            raise SyntaxError('Missing fields row or col')
        
        return cls(int(o['row']), int(o['col']))

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col
    
    def getAsTuple(self) -> Tuple[int, int]:
        return (self.__row, self.__col)
    
    def copy(self) -> HexPoint:
        return HexPoint(self.row, self.col)
    
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
    
    def __hash__(self):
        return hash(self.getAsTuple())
    
    def __str__(self):
        return f"HexPoint({self.__row}, {self.__col})"
    
    def __repr__(self):
        return self.__str__()
    
    def isNeighbor(self, other: HexPoint) -> bool:
        '''
        If point other is a next to this point.
        Taken from the typescript version, it worked there so I hope it works here
        '''
        if other.col == self.col and other.row == self.row + 1:
            return True

        if other.col == self.col and other.row == self.row - 1:
            return True

        if abs(self.col % 2) == abs(self.row % 2):
            # check right
            if other.col == self.col + 1 and other.row == self.row:
                return True
        else:
            if other.col == self.col - 1 and other.row == self.row:
                return True

        return False

    def getNeighbors(self) -> Tuple[HexPoint, HexPoint, HexPoint]:
        '''
        Gets all points adjacent to this point
        '''
        first = HexPoint(row=self.row + 1, col=self.col)
        second = HexPoint(row=self.row - 1, col=self.col)

        if abs(self.col % 2) == abs(self.row % 2):
            # right
            third = HexPoint(row=self.row, col=self.col + 1)
        else:
            # left
            third = HexPoint(row=self.row, col=self.col - 1)
        
        return first, second, third
    
    def getNeighboringTiles(self) -> Tuple[HexPoint, HexPoint, HexPoint]:
        '''
        Get all the tiles adjacent to a point
        '''
        # right
        #           * --- *
        #          /       \
        #   * --- *         *
        #  /       \\      /
        # *         X === *
        #  \       //      \
        #   * --- *         *
        #          \       /
        #           * --- *

        # left
        #   * --- *
        #  /       \
        # *         * --- *
        #  \       //      \
        #   * === X         *
        #  /       \\      /
        # *         * --- *
        #  \       /
        #   * --- *

        if abs(self.col % 2) == abs(self.row % 2):
            # two right, one left
            first = HexPoint(row=self.row, col=self.col)
            second = HexPoint(row=self.row-2, col=self.col)
            third = HexPoint(row=self.row-1, col=self.col-1)
        else:
            # two left, one right
            first = HexPoint(row=self.row-1, col=self.col)
            second = HexPoint(row=self.row, col=self.col-1)
            third = HexPoint(row=self.row-2, col=self.col-1)
        
        return first, second, third


class Resource(Enum):
    NoResource = 0
    Wheat = 1
    Sheepie = 2
    Lumber = 3
    Ore = 4
    Brick = 5


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
Biome('desert', Resource.NoResource, 'yellow')
