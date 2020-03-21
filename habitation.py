
import points
from typing import List
from outpost import Outpost
from tools import interface

HexPoint = points.HexPoint

class Tile:
    pass

class Player:
    pass

@interface(Outpost)
class Habitation:
    
    def __init__(self):
        self.pos: HexPoint = None
        self.diceValue: int = None
        self.neighboringTiles: List[Tile] = None
        self.owner: Player = None
    
    def dieRolled(self, d: int) -> None:
        # check if diceValue matches, then give resource
        pass

    def getPos(self) -> HexPoint:
        pass
