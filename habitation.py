
from point import HexPoint
from typing import List
# from outpost import Outpost
from tools import interface

from tile import Tile


class Player:
    pass

# @interface(Outpost)
class Habitation:
    '''
    Super class for Settlements and Cities

    Needs a method to be implemented:
        def harvestTile(self, b: Biome) -> None:
            # give the owner the appropriate resources
            # i.e. one resource for settlement, two for cities 
    '''

    def __init__(self, pos: HexPoint, owner: Player):
        self.__pos: HexPoint = pos
        self.owner: Player = owner

    def __init_subclass__(subCls):
        assert hasattr(subCls, "harvestTile")

    def getPos(self) -> HexPoint:
        return self.__pos
