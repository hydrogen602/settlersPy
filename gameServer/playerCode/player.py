from __future__ import annotations

from typing import Set, TYPE_CHECKING, Dict
from secrets import token_urlsafe

from .inventory import ExpandedInventory
from ..extraCode.util import ActionError

if TYPE_CHECKING:
    from ..extraCode.location import Resource
    from ..extraCode.location import HexPoint
    from .turn import Turn

class Player:

    __usedTokens: Set[str] = set()

    def __init__(self, name: str, connection, color: str) -> None:
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
        self.__color: str = color

        self.__canMoveRobber: bool = False

        self.__inventory: ExpandedInventory = ExpandedInventory()
    
    def checkFinishTurn(self):
        '''
        Throws an `ActionError` if a player isn't
        allowed to end their turn yet
        '''
        if len(self.__inventory.ownedLineFeatures) > 0:
            raise ActionError("There are unplaced roads")
        if len(self.__inventory.ownedPointFeatures) > 0:
            raise ActionError("There are unplaced settlements or cities")
        if self.__canMoveRobber:
            raise ActionError("Robber needs to be moved")
    
    def canMoveRobber(self):
        '''
        Called whenever the player needs to move the robber.
        Ex: if a 7 is rolled or a knight is played
        '''
        self.__canMoveRobber = True
    
    def moveRobber(self, point: HexPoint, turn: Turn):
        '''
        Call when a player wants to move the robber
        '''
        if not self.__canMoveRobber:
            raise ActionError("Not allowed to move robber")
        
        try:
            turn.gameMap.moveRobber(point)
        except KeyError:
            raise ActionError("No tile at given position")
        else:
            # no error
            self.__canMoveRobber = False
    
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
    
    def takeResource(self, resource: Resource, count: int):
        self.__inventory.removeResource(resource, count)
    
    def hasResource(self, resource: Resource, minimum: int) -> bool:
        return self.__inventory.hasResource(resource, minimum)
    
    @property
    def color(self) -> str:
        return self.__color
    
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
    
    def toJsonSerializable(self) -> Dict[str, object]:
        return {
            'name': self.__name,
            'token': self.__token,
            'color': self.__color
        }
