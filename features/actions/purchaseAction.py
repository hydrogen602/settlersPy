
from mechanics.actionManager import ActionManager, ActionSuperCls


class PurchaseRoad(ActionSuperCls):

    def __init__(self):
        # Use lowercase and underscores with names
        super().__init__('purchase', 'purchase_road')

    def isValid(self, player):
        pass # has the player the right resources?

    def doAction(self, player):
        pass # purchase