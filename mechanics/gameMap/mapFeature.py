from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from point import HexPoint
    from mechanics.player import Player


class MapFeature(ABC):
    
    @property
    @abstractmethod
    def owner(self) -> Union[Player, None]:
        ...
    
    @property
    @abstractmethod
    def point(self) -> HexPoint:
        ...
    
    @property
    @abstractmethod
    def color(self) -> str:
        ...


class CornerMapFeature(MapFeature):

    def __init__(self, point: HexPoint):
        self.__point: HexPoint = point

    @property
    def point(self) -> HexPoint: 
        return self.__point


class TileMapFeature(MapFeature):

    def __init__(self, point: HexPoint):
        self.__point: HexPoint = point
    
    @property
    def point(self) -> HexPoint: 
        return self.__point


class LineMapFeature(MapFeature):

    def __init__(self, point1: HexPoint, point2: HexPoint):
        self.__point1: HexPoint = point1
        self.__point2: HexPoint = point2

    @property
    def point1(self) -> HexPoint: 
        return self.__point1
    
    @property
    def point2(self) -> HexPoint: 
        return self.__point2
    
    @property
    def point(self) -> HexPoint:
        '''Lines have two points
        so the first will be what point returns
        '''
        return self.__point1
