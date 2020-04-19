
from .player import Player

from typing import Dict, Union
from tools import typeCheck

class PlayerManager:

    def __init__(self):
        '''
        Manages instances of the `Player` class.
        Keeps a dict of all players and allows for
        lookup of the `Player` instance given the token
        and other player management related things.
        '''
        self.__players: Dict[str, Player] = {}
    
    def addPlayer(self, p: Player):
        '''
        Add a new player to the playerManager
        '''
        typeCheck(p, Player)

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
        '''
        if token not in self.__players:
            raise KeyError(f'No player with token {token} found')
        return self.__players[token]
    
