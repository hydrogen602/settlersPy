from __future__ import annotations
from typing import TYPE_CHECKING

from .util import ActionError, NotSetupException, isNotNone, JsonSerializable, ArgumentMissingError
from .location import Resource

if TYPE_CHECKING:
    from typing import Optional, Dict
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
            raise TypeError(f'Subclass \'{cls.__name__}\' of Purchaseable is missing \'_cost\' attribute')

        assert isinstance(cls._cost, dict)
        for key, value in cls._cost.items():
            assert isinstance(key, Resource)
            assert isinstance(value, int)

        assert isinstance(cls._isLineFeature, bool)
        assert isinstance(cls._isPointFeature, bool)

        if (cls._isLineFeature and cls._isPointFeature) or not (cls._isLineFeature or cls._isPointFeature):
            raise TypeError('One one of \'_isPointFeature\' and \'_isLineFeature\' should be set')
    
    @classmethod
    def purchase(cls, p: Player):
        '''
        Automatically adds to player's inventory

        raises `ActionError`
        '''

        if (cls is Purchaseable):
            raise TypeError('Do not call \'purchase()\' on Purchaseable, only on subclasses')

        if cls._cost is None:
            raise RuntimeError('This should have been caught in \'__init_subclass__\'')

        p.requireResources(cls._cost) # raises ActionError
        p.takeResources(cls._cost)

        if cls._isLineFeature:
            if not issubclass(cls, Ownable):
                raise TypeError(f'Line Features should be owned by someone, class "{cls.__qualname__}" is not Ownable though"')
            p.inventory.addLineFeature(cls(owner=p))
            return

        if cls._isPointFeature:
            if not issubclass(cls, Ownable):
                raise TypeError(f'Point Features should be owned by someone, class "{cls.__qualname__}" is not Ownable though"')
            p.inventory.addPointFeature(cls(owner=p))
            return
        
        raise RuntimeError("This shouldn't happen")
    
    @classmethod
    def purchaseCost(cls) -> Dict[Resource, int]:
        if cls._cost is None:
            raise RuntimeError('This should have been caught in \'__init_subclass__\'')
        
        return cls._cost
