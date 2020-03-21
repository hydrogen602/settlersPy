'''
All point classes
'''
from __future__ import annotations

from tools import InterfaceSuperType, interface

class Point(InterfaceSuperType):
    def getHexPoint(self) -> HexPoint: pass
    def getRelPoint(self) -> RelPoint: pass
    def getAbsPoint(self) -> AbsPoint: pass

@interface(Point)
class HexPoint:
    def __init__(self, row, col):
        self.__row = row
        self.__col = col
    
    def getHexPoint(self) -> HexPoint:
        return HexPoint(self.__row, self.__col)
    
    def getRelPoint(self) -> RelPoint: pass
    def getAbsPoint(self) -> AbsPoint: pass

@interface(Point)
class RelPoint:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    def getHexPoint(self) -> HexPoint: pass
    def getRelPoint(self) -> RelPoint: pass
    def getAbsPoint(self) -> AbsPoint: pass

@interface(Point)
class AbsPoint:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    def getHexPoint(self) -> HexPoint: pass
    def getRelPoint(self) -> RelPoint: pass
    def getAbsPoint(self) -> AbsPoint: pass
