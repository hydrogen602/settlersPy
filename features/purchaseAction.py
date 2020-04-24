
from typing import Dict, Union

from mechanics.event import eventSystemSetup, Event, ActionEvent
from tools import typeCheck


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