
from ..playerCode.player import Player
from typing import Dict

class Placeable:
    pass

    # def __init_subclass__(cls):
    #     setattr(Placeable, cls.__name__, cls)

# class Ownable:

#     def __init__(self, owner: Player):
#         self._owner: Player = owner

#     @property
#     def owner(self) -> Player:
#         return self._owner

#     def toJsonSerializable(self) -> Dict[str, object]:
#         return {
#             'owner': self._owner
#         }
