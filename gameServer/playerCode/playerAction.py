
from .player import Player
from ..mapCode import Resource, Road, Settlement, City
from typing import Dict, Optional

class ActionError(Exception):
    # TODO: move to a util package
    '''
    For when some action isn't allowed by
    game rules, like buying something
    the player can't afford or placing
    something where it is not allowed to
    be placed
    '''
    pass

class NotSetupException(Exception):
    # TODO: move to a util package
    '''
    For when something cannot be used yet
    because some setup action hasn't happened yet
    '''
    pass

class Purchaseable:
    # TODO: move to a util package

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__cost: Optional[Dict[Resource, int]] = None
        self.__cls: Optional[type] = None

    def setupPurchase(self, clsOfObjectBeingPurchased: type, cost: Dict[Resource, int], isLineFeature: bool = False, isPointFeature: bool = False):
        assert not isLineFeature and isPointFeature
        assert isLineFeature or isPointFeature
        self.__cost = cost
        self.__cls = clsOfObjectBeingPurchased

        self.__isLineFeature: bool = isLineFeature
        self.__isPointFeature: bool = isPointFeature
    
    def purchase(self, p: Player) -> bool:
        if self.__cost is None or self.__cls is None:
            raise NotSetupException('Cannot purchase before setupPurchase has been called')
        
        for resource, qty in self.__cost.items():
            if not p.hasResource(resource, qty):
                raise ActionError(f"Missing resource: {resource.name}")
        
        for resource, qty in self.__cost.items():
            p.takeResource(resource, qty)

        if self.__isLineFeature:
            p.inventory.addLineFeature(self.__cls)
        if self.__isPointFeature:
            p.inventory.addPointFeature(self.__cls)
    
    @property
    def purchaseCost(self) -> Dict[Resource, int]:
        return self.__cost

    


class Actions:

    @staticmethod
    def purchaseRoad(p: Player) -> bool:
        if not p.hasResource(Resource.Brick, 1):
            raise ActionError("Missing resource: brick")
        if not p.hasResource(Resource.Lumber, 1):
            raise ActionError("Missing resource: lumber")
        
        p.takeResource(Resource.Brick, 1)
        p.takeResource(Resource.Lumber, 1)

        p.inventory.addLineFeature(Road) # TODO: make method in player for this

        # TODO: make recipes that auto do this

        return True