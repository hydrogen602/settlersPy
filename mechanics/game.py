from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from mechanics.util.die import roll2Die

if TYPE_CHECKING:
    from mechanics.playerManager import PlayerManager
    from mechanics.player import Player
    from mechanics.gameMap.gameMap import GameMap


class Game:
    '''
    Represents a game and its associated data
    '''

    def __init__(self, map_: GameMap):
        self.__playerManager: PlayerManager = PlayerManager.instance
        self.__map: GameMap = map_

        self.turnNum = 0

    def nextTurn(self) -> Turn:
        self.turnNum += 1
        return Turn(self.turnNum, self.__map, self.__playerManager.nextPlayer())

    @property
    def players(self) -> PlayerManager:
        return self.__playerManager

    @property
    def map(self) -> GameMap:
        return self.__map


class Turn:
    '''
    Superclass representing a turn
    and the information related to it.
    Stores things like which player's turn it is 
    '''

    def __init__(self, turnNum: int, gameMap: GameMap, currentPlayer: Player):
        self.__turnNum: int = turnNum
        self.__gameMap: GameMap = gameMap
        self.__player: Player = currentPlayer
        self.__current2DieRoll: int = roll2Die()

    @property
    def turnNum(self) -> int:
        return self.__turnNum

    @property
    def gameMap(self) -> GameMap:
        return self.__gameMap

    @property
    def currentPlayer(self) -> Player:
        return self.__player
    
    @property
    def twoDieRoll(self) -> int:
        return self.__current2DieRoll

