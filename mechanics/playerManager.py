
from .player import Player

from typing import Dict, Union, List, Iterator
from random import shuffle

from tools import typeCheck

class PlayerManager:

    __hasInit: bool = False

    instance = None

    def __init__(self):
        '''
        Manages instances of the `Player` class.
        Keeps a dict of all players and allows for
        lookup of the `Player` instance given the token
        and other player management related things.
        '''
        if PlayerManager.__hasInit:
            raise Exception('There should only be one instance of the PlayerManager')
        PlayerManager.__hasInit = True
        PlayerManager.instance = self

        self.__players: Dict[str, Player] = {}

        self.__gameStarted: bool = False
        self.__playerTurnOrder: List[str] = []

        self.__playerTurnOrderIterator: Iterator[str] = None
    
    def startGame(self):
        '''
        Call once the game has started. This locks the player list
        and creates a random turn order from the current list of players
        '''
        if self.__gameStarted:
            raise Exception('Game has already started')

        self.__gameStarted = True
        self.__playerTurnOrder = list(self.__players.keys())
        shuffle(self.__playerTurnOrder)
    
    # def getPlayerTurnOrderIterator(self) -> Iterator[Player]:
    #     if not self.__gameStarted:
    #         raise Exception('Game hasn\'t started yet')
        
    #     for key in self.__playerTurnOrder:
    #         yield self.__players[key]
    
    def nextPlayer(self) -> Player:
        '''
        Returns whose player's turn the next turn is
        '''
        if not self.__gameStarted:
            raise Exception('Game hasn\'t started yet')

        if self.__playerTurnOrderIterator is None:
            self.__playerTurnOrderIterator = iter(self.__playerTurnOrder)
        
        try:
            return next(self.__playerTurnOrderIterator)
        except StopIteration:
            self.__playerTurnOrderIterator = iter(self.__playerTurnOrder)
            return next(self.__playerTurnOrderIterator)
    
    # def __next__(self) -> Player:
    #     '''
    #     PlayerManager has a next function, which makes it an iterator, but this
    #     iterator goes in circles and follows turn order
    #     '''
    #     if not self.__gameStarted:
    #         raise Exception('Game hasn\'t started yet')

    #     return self.nextPlayer()
    
    def addPlayer(self, p: Player):
        '''
        Add a new player to the playerManager.
        Cannot be done once the game has started
        '''
        typeCheck(p, Player)

        if self.__gameStarted:
            raise Exception('Cannot add player after game has started')

        self.__players[p.token] = p
        # players should always have unique tokens
    
    def getPlayer(self, token: str) -> Union[Player, None]:
        '''
        Looks for the player with the given token.
        Returns the Player instance if found and
        `None` if nothing is found.
        Thus this method doesn't raise a `KeyError`
        '''
        return self.__players.get(token)
    
    def __getitem__(self, token: str) -> Player:
        '''
        Looks for the player with the given token.
        Raises a `KeyError` if no player with the given token is found.
        This allows for use of indexing with [].
        '''
        if token not in self.__players:
            raise KeyError(f'No player with token {token} found')
        return self.__players[token]
    
    def __contains__(self, token: str) -> bool:
        '''
        Returns whether or not a player with the given token exists.
        This allows using the `in` keyword.
        '''
        return token in self.__players
    
    def __iter__(self):
        '''
        Returns an iterator over the player list.
        Call this if the order of players does not matter.
        If order matters, like in determining the next person to play,
        use getPlayerTurnOrderIterator
        '''
        return iter(self.__players.values())
    

PlayerManager() # instantiate the one player manager instance
