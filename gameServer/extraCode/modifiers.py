from __future__ import annotations
from typing import TYPE_CHECKING

from .util import ActionError, NotSetupException, isNotNone, JsonSerializable

if TYPE_CHECKING:
    from typing import Optional, Dict
    from .location import Resource
    from ..playerCode.player import Player


class Placeable:
    '''
    For now it's just a tag
    '''
    pass


class Ownable(JsonSerializable):
    '''
    A class for anything that can be owned.
    It is a subclass of JsonSerializable.
    '''

    def __init__(self, owner: Player = None, **kwargs) -> None:
        isNotNone('__init__', owner=owner)
        super().__init__(**kwargs) # type: ignore

        self._owner: Player = owner # type: ignore

    @property
    def owner(self) -> Player:
        return self._owner

    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'owner': self._owner,
            **super().toJsonSerializable()
        }


class Purchaseable:

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
            p.inventory.addLineFeature(self.__cls) # type: ignore
            return True
        if self.__isPointFeature:
            p.inventory.addPointFeature(self.__cls) # type: ignore
            return True
        
        raise RuntimeError("This shouldn't happen")
    
    @property
    def purchaseCost(self) -> Dict[Resource, int]:
        if self.__cost is None:
            raise NotSetupException('Cannot get purchaseCost before setupPurchase has been called')
        
        return self.__cost