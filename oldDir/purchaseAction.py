
from typing import Dict, Union

from mechanics.event import eventSystemSetup, Event, ActionEvent
from tools import typeCheck

from biome import Resource

from abc import abstractmethod

#from mechanics.actionManager import ActionManager, ActionIllegalException

from message import Message

@eventSystemSetup('name', buildFromJsonMethod=True)
class PurchaseAction(ActionEvent):

    groupName = 'purchase'

    __subClsList: Dict[str, type] = {}

    def __init__(self, name: str):
        self.__name: str = name
        super().__init__(PurchaseAction.groupName)
    
    @property
    def name(self) -> str:
        return self.__name
    
    @abstractmethod
    def getPurchaseCost(self) -> Dict[Resource, int]:
        pass
    
    def doAction(self, messageObject: Message):
        cost = self.getPurchaseCost()

        inventory = messageObject.player.inventory
        for resource in cost:
            numRequired = cost[resource]
            if not inventory.hasResource(resource, numRequired):
                print('Invalid resources')

                return
        
        print('Buying something')
                
        cost = self.getPurchaseCost()
        for resource in cost:
            numRequired = cost[resource]
            inventory.removeResource(resource, numRequired)
    
    # @staticmethod
    # def fromJson(data: Dict[str, Union[str, dict]]):
    #     typeCheck(data, dict)

    #     if 'name' not in data:
    #         raise KeyError("Missing key 'name'")

    #     name = data['name']
    #     if name not in PurchaseAction.__subClsList:
    #         raise KeyError(f"No subclass found for event name '{name}'")

    #     subCls = ActionEvent.__subClsList[name]

    #     return subCls.fromJson(data)


class PurchaseRoad(PurchaseAction):
    '''
    Example js to trigger this class:
    ws.send(JSON.stringify({'typeName':'action', 'group':'purchase', 'name':'purchase_road'}))
    '''

    name = "purchase_road"

    def __init__(self, data):
        self.__data: Dict[str, object] = data
        super().__init__(PurchaseRoad.name)
    
    @property
    def data(self) -> Dict[str, object]:
        return self.__data
    
    @staticmethod
    def fromJson(data: Dict[str, Union[str, dict]]):
        typeCheck(data, dict)

        # purchase road needs no extra data

        print("Player wants to purchase a road")

        return PurchaseRoad(data)
    
    def getPurchaseCost(self) -> Dict[Resource, int]:
        return {
            Resource.Brick: 1,
            Resource.Lumber: 1
        }
    
    # def doAction(self, messageCls):
    #     print("Purchase road")
    #     ActionManager.call(self.group, self.name, messageCls)
        
        