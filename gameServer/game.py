
from typing import Iterator, Optional
import json

from .extraCode.util import AlreadySetupException, NotSetupException, roll2Die, JsonSerializable, customJsonEncoder
from .playerCode.playerManager import PlayerManager
from .playerCode.player import Player
from .playerCode.turn import Turn
from .mapCode.gameMap import GameMap
from .mapCode.lineMapFeatures import Road
from .mapCode.pointMapFeatures import Settlement

class Game(JsonSerializable):

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

    def __newTurn(self, currentPlayer: Player):
        '''
        For handling things that should happen when it becomes a player's
        turn, like making a `Turn` instance or giving them a settlement and
        road in the first two turns
        '''
        dieVal: Optional[int] = None
        if self.__roundNum >= 2:
            # give resources!
            dieVal = roll2Die()
            if dieVal == 7:
                currentPlayer.canMoveRobber()
                # TODO: if inv count > 7, then half has to be removed
            else:
                for t in self.__gameMap.tiles:
                    t.diceRolled(dieVal)

        self.__currentTurn = Turn(self.__gameMap, self.__roundNum, currentPlayer, dieVal)

        if self.__roundNum < 2:
            currentPlayer.inventory.addPointFeature(Settlement(owner=currentPlayer))
            currentPlayer.inventory.addLineFeature(Road(owner=currentPlayer))

    def startGame(self):
        if self.__gameStarted:
            raise AlreadySetupException("Game already started")

        self.__gameStarted = True
        self.__playerManager.startGame()
        self.__playerTurnOrderIterator = self.__playerManager.getPlayerTurnOrderIterator()

        self.__newTurn(next(self.__playerTurnOrderIterator))
        
    
    def addPlayer(self, p: Player):
        if self.__gameStarted:
            raise AlreadySetupException("Game already started")
        self.__playerManager.addPlayer(p)
    
    def nextTurn(self):
        if not self.__gameStarted:
            raise NotSetupException("Game hasn't started yet")

        self.__currentTurn.currentPlayer.checkFinishTurn()

        try:
            nextPlayer = next(self.__playerTurnOrderIterator)
        except StopIteration:
            self.__roundNum += 1
            self.__playerTurnOrderIterator = self.__playerManager.getPlayerTurnOrderIterator()

            nextPlayer = next(self.__playerTurnOrderIterator)
        
        self.__newTurn(nextPlayer)
    
    def toJsonSerializable(self):
        return {
            'players': list(self.__playerManager),
            'gameMap': self.__gameMap,
            'gameStarted': self.__gameStarted,
            **super().toJsonSerializable()
        }

    def getAsJson(self):
        return json.dumps(self, cls=customJsonEncoder)
