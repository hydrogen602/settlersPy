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

    _cost: Optional[Dict[Resource, int]] = None
    _isLineFeature: bool = False
    _isPointFeature: bool = False

    def __init_subclass__(cls):
        super().__init_subclass__()

        if not cls._cost:
            raise TypeError(f'Subclass ${cls.__name__} of Purchaseable is missing \'_cost\' attribute')
        
        assert isinstance(cls._cost, dict)
        for key, value in cls._cost.items():
            assert isinstance(key, Resource)
            assert isinstance(value, int)

        if not (hasattr(cls, '_isLineFeature') or hasattr(cls, '_isPointFeature')):
            raise TypeError(f'Subclass ${cls.__name__} of Purchaseable needs to have either \'_isLineFeature\' or \'_isPointFeature\' attribute')

        isLineFeature = False
        isPointFeature = False

        if hasattr(cls, '_isLineFeature'):
            isLineFeature = getattr(cls, '_isLineFeature')
            assert isinstance(isLineFeature, bool)
        
        if hasattr(cls, '_isPointFeature'):
            isPointFeature = getattr(cls, '_isPointFeature')
            assert isinstance(isPointFeature, bool)
        
        if (isLineFeature and isPointFeature) or not (isLineFeature or isPointFeature):
            raise TypeError('One one of \'_isPointFeature\' and \'_isLineFeature\' should be set')

        cls._isLineFeature = isLineFeature
        cls._isPointFeature = isPointFeature
    
    @classmethod
    def purchase(cls, p: Player) -> bool:
        if (cls is Purchaseable):
            raise TypeError('Do not call \'purchase()\' on Purchaseable, only on subclasses')

        # if cls._cost is None or cls.__cls is None:
        #     raise NotSetupException('Cannot purchase before setupPurchase has been called')
        
        for resource, qty in cls._cost.items():
            if not p.hasResource(resource, qty):
                raise ActionError(f"Missing resource: {resource.name}")
        
        for resource, qty in cls._cost.items():
            p.takeResource(resource, qty)

        if cls._isLineFeature:
            p.inventory.addLineFeature(cls())
            return True

        if cls._isPointFeature:
            p.inventory.addPointFeature(cls())
            return True
        
        raise RuntimeError("This shouldn't happen")
    
    @classmethod
    def purchaseCost(cls) -> Dict[Resource, int]:
        if cls._cost is None:
            raise NotSetupException('Cannot get purchaseCost before setupPurchase has been called')
        
        return cls._cost
