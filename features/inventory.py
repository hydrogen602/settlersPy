import 


from typing import Dict

import biome
from tools import typeCheck

class Inventory:

    def __init__(self):
        self.__inventory: Dict[biome.Resource, int] = dict([(r, 0) for r in biome.Resource])
        self.addResource(biome.Resource.Brick, 1)
        self.addResource(biome.Resource.Lumber, 1)
    
    def getCount(self, resourceType: biome.Resource) -> int:
        typeCheck(resourceType, biome.Resource)
        return self.__inventory[resourceType]
    
    def hasResource(self, resourceType: biome.Resource, minimum: int) -> bool:
        return self.getCount(resourceType) >= minimum
    
    def addResource(self, resourceType: biome.Resource, count: int):
        typeCheck(resourceType, biome.Resource)
        self.__inventory[resourceType] += count
    
    def removeResource(self, resourceType: biome.Resource, count: int):
        typeCheck(resourceType, biome.Resource)
        self.__inventory[resourceType] -= count
        if self.__inventory[resourceType] < 0:
            raise ValueError('negative value in inventory')
    
    def totalResourceCount(self) -> int:
        return sum(self.__inventory.values())

