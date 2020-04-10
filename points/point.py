'''
All point classes
'''
from __future__ import annotations

from tools import InterfaceSuperType, interface

class HexPoint:
    def __init__(self, row, col):
        self.__row = row
        self.__col = col

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col
