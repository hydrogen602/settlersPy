
# from abc import abstractmethod
# from typing import Dict

# from mechanics.actionManager import ActionManager, ActionSuperCls
# from mechanics.player import Player

# from message import Message

# from biome import Resource

# class PurchaseSomething(ActionSuperCls):

#     def __init__(self, name):
#         super().__init__('purchase', name)

#     @abstractmethod
#     def getPurchaseCost(self) -> Dict[Resource, int]:
#         pass
    
#     def doAction(self, messageObject: Message):
#         cost = self.getPurchaseCost()

#         inventory = messageObject.player.inventory
#         for resource in cost:
#             numRequired = cost[resource]
#             if not inventory.hasResource(resource, numRequired):
#                 print('Invalid resources')

#                 return
        
#         print('Buying road')
                
#         cost = self.getPurchaseCost()
#         for resource in cost:
#             numRequired = cost[resource]
#             inventory.removeResource(resource, numRequired)

# @ActionManager.register
# class PurchaseRoad(PurchaseSomething):

#     def __init__(self):
#         # Use lowercase and underscores with names
#         super().__init__('purchase_road')
    
#     def getPurchaseCost(self) -> Dict[Resource, int]:
#         return {
#             Resource.Brick: 1,
#             Resource.Lumber: 1
#         }
