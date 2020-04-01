from tools import InterfaceSuperType, interface
from points import HexPoint
from biome import Biome

class Outpost(InterfaceSuperType):
    '''
    Interface for Settlements and Cities
    '''
    
    def giveResource(self, b: Biome) -> None:
        pass

    def getPos(self) -> HexPoint:
        pass
