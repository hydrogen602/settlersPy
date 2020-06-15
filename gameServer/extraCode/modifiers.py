from __future__ import annotations
from typing import TYPE_CHECKING

from .util import ActionError, NotSetupException, isNotNone, JsonSerializable, ArgumentMissingError

if TYPE_CHECKING:
    from typing import Optional, Dict
    from .location import Resource
    from ..playerCode.player import Player


class Placeable(JsonSerializable):
    '''
    This is for objects which can be held by the player
    in their inventory before being put on the map
    '''
    def __init__(self, isPlaced: bool = None, **kwargs) -> None:
        '''
        isPlaced does not need to be specified but
        is instead determined by subclassed based
        on whether they got their map position or not
        '''
        if isPlaced is None:
            raise ArgumentMissingError('__init__', 'isPlaced')
        super().__init__(**kwargs) # type: ignore

        self._isPlaced: bool = isPlaced
    
    @property
    def isPlaced(self) -> bool:
        return self._isPlaced
    
    def _place(self):
        '''
        Call when something like a Settlement
        instance is being placed on the map
        '''
        self._isPlaced = True
    
    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'isPlaced': self._isPlaced,
            **super().toJsonSerializable()
        }


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
        assert not (isLineFeature and isPointFeature)
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
            p.inventory.addLineFeature(self.__cls())
            return True
        if self.__isPointFeature:
            p.inventory.addPointFeature(self.__cls())
            return True
        
        raise RuntimeError("This shouldn't happen")
    
    @property
    def purchaseCost(self) -> Dict[Resource, int]:
        if self.__cost is None:
            raise NotSetupException('Cannot get purchaseCost before setupPurchase has been called')
        
        return self.__cost