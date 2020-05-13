from __future__ import annotations

import json

from typing import List, TYPE_CHECKING
from tools import customJsonEncoder

if TYPE_CHECKING:
    import mechanics.gameMap.mapFeature as mapFeature
    import mechanics.gameMap.advancedMapFeature as advancedMapFeature
    from mechanics.player import Player

    from point import HexPoint


class GameMap:

    def __init__(self, tiles: List[mapFeature.TileMapFeature]):
        self.__tiles = tiles
        self._mapElements: List[mapFeature.MapFeature] = []
    
    def __init_subclass__(cls):
        if not hasattr(cls, 'getAsJson'):
            raise TypeError(f"Missing method 'getAsJson' in {cls.__name__}")

    def addMapElement(self, elem: mapFeature.MapFeature):
        self._mapElements.append(elem)

    # def getAsJson(self):
    #     return json.dumps(self, cls=customJsonEncoder)
