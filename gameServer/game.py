
from typing import Iterator, Optional

from .extraCode.util import AlreadySetupException, NotSetupException
from .playerCode.playerManager import PlayerManager
from .playerCode.player import Player
from .playerCode.turn import Turn
from .mapCode.gameMap import GameMap

class Game:

    def __init__(self, gameMap: GameMap):
        self.__gameStarted: bool = False
        self.__playerManager: PlayerManager = PlayerManager()

        self.__gameMap: GameMap = gameMap

        self.__playerTurnOrderIterator: Optional[Iterator[Player]] = None
        self.__currentTurn: Optional[Turn] = None

        self.__roundNum = 0

    @property
    def playerManager(self) -> PlayerManager:
        return self.__playerManager

    @property
    def currentTurn(self) -> Turn:
        if self.__currentTurn is None:
            raise NotSetupException("Game hasn't started yet")

        return self.__currentTurn
    
    @property
    def gameMap(self) -> GameMap:
        return self.__gameMap

    def __newTurn(self):
        pass

    def startGame(self):
        if self.__gameStarted:
            raise AlreadySetupException("Game already started")

        self.__gameStarted = True
        self.__playerManager.startGame()
        self.__playerTurnOrderIterator = self.__playerManager.getPlayerTurnOrderIterator()

        self.__currentTurn = Turn(self.__gameMap, self.__roundNum, next(self.__playerTurnOrderIterator))
        
    
    def addPlayer(self, p: Player):
        if self.__gameStarted:
            raise AlreadySetupException("Game already started")
        self.__playerManager.addPlayer(p)
    
    def nextTurn(self):
        if not self.__gameStarted:
            raise NotSetupException("Game hasn't started yet")

        self.__currentTurn.currentPlayer.checkFinishTurn()

        try:
            self.__currentTurn = Turn(self.__gameMap, self.__roundNum, next(self.__playerTurnOrderIterator))
        except StopIteration:
            self.__roundNum += 1
            self.__playerTurnOrderIterator = self.__playerManager.getPlayerTurnOrderIterator()
            self.__currentTurn = Turn(self.__gameMap, self.__roundNum, next(self.__playerTurnOrderIterator))
