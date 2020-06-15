from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..mapCode.gameMap import GameMap
    from .player import Player

class Turn:

    def __init__(self, gameMap: GameMap, roundNum: int, currentPlayer: Player, dieValue: Optional[int] = None):
        assert dieValue is None or isinstance(dieValue, int)
        assert isinstance(roundNum, int)

        self.__gameMap: GameMap = gameMap
        self.__roundNum: int = roundNum
        self.__currentPlayer: Player = currentPlayer
        self.__dieValue: Optional[int] = dieValue
    
    @property
    def gameMap(self) -> GameMap:
        return self.__gameMap
    
    @property
    def roundNum(self) -> int:
        '''
        Round number should start at 0,
        so 0 -> 1st, 1 -> 2nd, etc.
        '''
        return self.__roundNum
    
    @property
    def currentPlayer(self) -> Player:
        return self.__currentPlayer
    
    @property
    def dieValue(self) -> Optional[int]:
        return self.__dieValue