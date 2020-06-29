from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

from ..extraCode.location import Biome, Resource
from ..extraCode.util import ActionError
from ..extraCode.util import JsonSerializable

if TYPE_CHECKING:
    from ..mapCode.pointMapFeatures import Settlement
    from ..mapCode.lineMapFeatures import Road
    from ..extraCode.location import HexPoint
    from .turn import Turn


class Inventory(JsonSerializable):

    def __init__(self):
        self.__inventory: Dict[Resource, int] = dict([(r, 0) for r in Resource])
        
        # for debug
        # self.addResource(Resource.Brick, 1)
        # self.addResource(Resource.Lumber, 1)
    
    def getCount(self, resourceType: Resource) -> int:
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")
        return self.__inventory[resourceType]
    
    def hasResource(self, resourceType: Resource, minimum: int) -> bool:
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")
        return self.getCount(resourceType) >= minimum
    
    def addResource(self, resourceType: Resource, count: int):
        assert count >= 0
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")

        self.__inventory[resourceType] += count
    
    def removeResource(self, resourceType: Resource, count: int):
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")

        if self.__inventory[resourceType] < count:
            raise ValueError(f'Asked for {count} of {resourceType.name}, but the inventory only has {self.__inventory[resourceType]}')
        
        self.__inventory[resourceType] -= count
    
    def totalResourceCount(self) -> int:
        return sum(self.__inventory.values())
    
    def __str__(self) -> str:
        return "Inv: " + '; '.join([f"{resource.name}: {count}" for resource, count in self.__inventory.items()])

    def toJsonSerializable(self):
        d = {}
        for key, value in self.__inventory.items():
            d[key.name] = value

        return {
            **d,
            **super().toJsonSerializable()
        }

class ExpandedInventory(Inventory):
    '''
    Inventory that also keeps track of
    purchased roads, settlements, etc.
    that haven't been placed yet
    '''

    def __init__(self):
        super().__init__()

        self.__ownedPointFeatures: List[Settlement] = []
        self.__ownedLineFeatures: List[Road] = []

    def addPointFeature(self, s: Settlement):
        self.__ownedPointFeatures.append(s)
    
    def addLineFeature(self, r: Road):
        self.__ownedLineFeatures.append(r)
    
    @property
    def ownedPointFeatures(self) -> List[Settlement]:
        return self.__ownedPointFeatures
    
    @property
    def ownedLineFeatures(self) -> List[Road]:
        return self.__ownedLineFeatures
    
    def placePointFeature(self, index: int, point: HexPoint, turn: Turn):
        if len(self.__ownedPointFeatures) == 0:
            raise ActionError("You have no settlements or cities to place")
        if index < 0 or index >= len(self.__ownedPointFeatures):
            raise IndexError(f"Index out of bounds: {index}")

        s = self.__ownedPointFeatures[index]
        s.place(point, turn)

        self.__ownedPointFeatures.pop(index)
    
    def placeLineFeature(self, index: int, point1: HexPoint, point2: HexPoint, turn: Turn):
        if len(self.__ownedLineFeatures) == 0:
            raise ActionError("You have no roads to place")
        if index < 0 or index >= len(self.__ownedLineFeatures):
            raise IndexError(f"Index out of bounds: {index}")

        r = self.__ownedLineFeatures[index]
        r.place(point1, point2, turn)

        self.__ownedLineFeatures.pop(index)
    
    def __str__(self) -> str:
        s = super().__str__()
        return s + f" | PointFeatures: [{', '.join([str(e) for e in self.__ownedPointFeatures])}]; LineFeatures: [{', '.join([str(e) for e in self.__ownedLineFeatures])}]"

    def toJsonSerializable(self):
        return {
            'pointFeatures': self.__ownedPointFeatures,
            'lineFeatures': self.__ownedLineFeatures,
            **super().toJsonSerializable()
        }