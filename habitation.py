
from biome import Resource, Biome
from point import HexPoint
from typing import List

from tile import Tile

class Player:
    def giveResource(self, resource: Resource):
        NotImplemented

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

    def __init_subclass__(cls):
        assert hasattr(cls, "harvestTile")

    def getPos(self) -> HexPoint:
        return self.__pos


class Settlement(Habitation):

    def __init__(self, pos: HexPoint, owner: Player):
        super().__init__(pos, owner)
    
    def harvestTile(self, b: Biome):
        self.owner.giveResource(b.primaryRes)


class City(Habitation):

    def __init__(self, pos: HexPoint, owner: Player):
        super().__init__(pos, owner)
    
    def harvestTile(self, b: Biome):
        self.owner.giveResource(b.primaryRes)
        self.owner.giveResource(b.primaryRes)

