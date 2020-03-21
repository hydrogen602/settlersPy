from tools import InterfaceSuperType, interface
from points import HexPoint

class Outpost(InterfaceSuperType):
    '''
    Interface for Settlements and Cities
    '''
    
    def dieRolled(self, d: int) -> None:
        pass

    def getPos(self) -> HexPoint:
        pass
