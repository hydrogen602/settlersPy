from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..mapCode.gameMap import GameMap
    from .player import Player

class Turn:

    def __init__(self, gameMap: GameMap, roundNum: int, currentPlayer: Player):
        self.__gameMap: GameMap = gameMap
        self.__roundNum: int = roundNum
        self.__currentPlayer: Player = currentPlayer
    
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