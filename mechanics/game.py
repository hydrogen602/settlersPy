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
        '''
        Initializing this class starts the game!.
        '''
        self.__playerManager: PlayerManager = PlayerManager.instance
        self.__playerManager.startGame()

        self.__map: GameMap = map_

        self.__turnNum: int = 0
        self.__roundNum: int = 0

        self.__playerTurnOrderIt: Iterator[Player] = None
    
    def __getNextPlayer(self) -> Player:
        if self.__playerTurnOrderIt is None:
            self.__roundNum += 1
            self.__playerTurnOrderIt = self.__playerManager.getPlayerTurnOrderIterator()
        
        try:
            return next(self.__playerTurnOrderIt)
        except StopIteration:
            self.__playerTurnOrderIt = self.__playerManager.getPlayerTurnOrderIterator()
            self.__roundNum += 1
            return next(self.__playerTurnOrderIt)

    def nextTurn(self) -> Turn:
        self.__turnNum += 1
        return Turn(self.__turnNum, self.__roundNum, self.__map, self.__getNextPlayer())

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

    def __init__(self, turnNum: int, roundNum: int, gameMap: GameMap, currentPlayer: Player):
        self.__turnNum: int = turnNum
        self.__roundNum: int = roundNum
        self.__gameMap: GameMap = gameMap
        self.__player: Player = currentPlayer
        self.__current2DieRoll: int = roll2Die()

    @property
    def turnNum(self) -> int:
        return self.__turnNum
    
    @property
    def roundNum(self) -> int:
        return self.__roundNum

    @property
    def gameMap(self) -> GameMap:
        return self.__gameMap

    @property
    def currentPlayer(self) -> Player:
        return self.__player
    
    @property
    def twoDieRoll(self) -> int:
        return self.__current2DieRoll

