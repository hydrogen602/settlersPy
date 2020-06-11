
from typing import Set

from secrets import token_urlsafe

from .inventory import ExpandedInventory

from ..mapCode.util import Resource

class Player:

    __usedTokens: Set[str] = set()

    def __init__(self, name: str, connection) -> None:
        '''
        `Player` is meant to represent one player uniquely.
        `name` is the name visible to other players and
        should be a real name. `token` is a semi-random
        string of characters to uniquely represent one
        player.
        `connection` should be of type `ServerProtocol` but its hard to enforce
        '''

        token = token_urlsafe(16)
        while token in Player.__usedTokens:
            token = token_urlsafe(16)

        Player.__usedTokens.add(token)

        self.__name: str = name
        self.__token: str = token
        self.__connection = connection

        self.__inventory: ExpandedInventory = ExpandedInventory()
    
    @property
    def connection(self):
        '''
        The instance of `ServerProtocol` that this player has
        '''
        return self.__connection
    
    def isConnected(self):
        '''
        Returns whether the connection variable is not None.
        Equivalent to foo.connection is not None
        '''
        return self.__connection is not None
    
    def reconnect(self, connection):
        '''
        Called when the player reconnects and so has a different `ServerProtocol` instance
        '''
        self.__connection = connection
    
    def disconnect(self):
        '''
        Called when the player disconnects
        '''
        self.__connection = None
    
    @property
    def name(self) -> str:
        '''
        The displayed name of the player
        '''
        return self.__name
    
    @property
    def token(self) -> str:
        '''
        The token used to uniquely identify the player
        '''
        return self.__token
    
    @property
    def inventory(self) -> ExpandedInventory:
        return self.__inventory
    
    def giveResource(self, resource: Resource, count: int = 1):
        self.__inventory.addResource(resource, count)
    
    @property
    def color(self) -> str:
        return 'blue' # TODO: make this chooseable by user
    
    def __eq__(self, other: object) -> bool:
        '''
        Equality is only determined by the token,
        which should be unique. Thus, two players
        with the same name will still return False
        when checked for equality.
        If `other` is of type other than
        `PlayerID`, the result is always False
        '''
        if isinstance(other, Player):
            return other.token == self.token
        else:
            return False
    
    def __ne__(self, other: object) -> bool:
        '''
        Returns the inverse of __eq__
        '''
        return not self.__eq__(other)
    
    def __str__(self) -> str:
        '''
        returns a str in the format of:
        "Player(name={self.name}, token={self.token})"
        '''
        return f"Player(name={self.name}, token={self.token})"
    
    def __repr__(self) -> str:
        '''
        returns `self.__str__()`
        '''
        return self.__str__()
