
from abc import abstractmethod
from typing import Dict

from mechanics.actionManager import ActionManager, ActionSuperCls
from mechanics.player import Player

from biome import Resource

class PurchaseSomething(ActionSuperCls):

    @abstractmethod
    def getPurchaseCost(self) -> Dict[Resource, int]:
        pass
    
    def isValid(self, player: Player) -> bool:
        cost = self.getPurchaseCost()
        for resource in cost:
            numRequired = cost[resource]
            if not player.inventory.hasResource(resource, numRequired):
                return False
        return True

    def __init__(self, name):
        super().__init__('purchase', name)

@ActionManager.register
class PurchaseRoad(PurchaseSomething):

    def __init__(self):
        # Use lowercase and underscores with names
        super().__init__('purchase_road')
    
    def getPurchaseCost(self) -> Dict[Resource, int]:
        return {
            Resource.Brick: 1,
            Resource.Lumber: 1
        }

    def doAction(self, player: Player):
        pass # purchase
