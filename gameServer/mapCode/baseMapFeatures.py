
from ..playerCode.player import Player
from .util import JsonSerializable, isNotNone
from typing import Dict

class Placeable:
    pass

    # def __init_subclass__(cls):
    #     setattr(Placeable, cls.__name__, cls)

class Ownable(JsonSerializable):
    '''
    A class for anything that can be owned.
    It is a subclass of JsonSerializable.
    '''

    def __init__(self, owner: Player = None, **kwargs) -> None:
        isNotNone('__init__', owner=owner)
        super().__init__(**kwargs)

        self._owner: Player = owner

    @property
    def owner(self) -> Player:
        return self._owner

    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'owner': self._owner,
            **super().toJsonSerializable()
        }
