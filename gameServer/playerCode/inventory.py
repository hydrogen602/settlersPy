
from typing import Dict

from ..mapCode.util import Biome, Resource

class Inventory:

    def __init__(self):
        self.__inventory: Dict[Resource, int] = dict([(r, 0) for r in Resource])
        
        # for debug
        self.addResource(Resource.Brick, 1)
        self.addResource(Resource.Lumber, 1)
    
    def getCount(self, resourceType: Resource) -> int:
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")
        return self.__inventory[resourceType]
    
    def hasResource(self, resourceType: Resource, minimum: int) -> bool:
        return self.getCount(resourceType) >= minimum
    
    def addResource(self, resourceType: Resource, count: int):
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")

        self.__inventory[resourceType] += count
    
    def removeResource(self, resourceType: Resource, count: int):
        if not isinstance(resourceType, Resource):
            raise TypeError(f"Expected type Resource but got type {type(resourceType)}")

        self.__inventory[resourceType] -= count
        if self.__inventory[resourceType] < 0:
            raise ValueError('negative value in inventory')
    
    def totalResourceCount(self) -> int:
        return sum(self.__inventory.values())

