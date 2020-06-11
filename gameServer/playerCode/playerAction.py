
from .player import Player
from ..mapCode import Resource, Road, Settlement, City

class ActionError(Exception):
    pass

class Actions:

    @staticmethod
    def purchaseRoad(p: Player) -> bool:
        if not p.hasResource(Resource.Brick, 1):
            raise ActionError("Missing resource: brick")
        if not p.hasResource(Resource.Lumber, 1):
            raise ActionError("Missing resource: lumber")
        
        p.takeResource(Resource.Brick, 1)
        p.takeResource(Resource.Lumber, 1)

        p._Player__inventory.addLineFeature(Road) # TODO: make method in player for this

        # TODO: make recipes that auto do this

        return True