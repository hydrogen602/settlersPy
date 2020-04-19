
from typing import Set

class Player:

    __usedTokens: Set[str] = set()

    def __init__(self, name: str, token: str):
        '''
        `Player` is meant to represent one player uniquely.
        `name` is the name visible to other players and
        should be a real name. `token` is a semi-random
        string of characters to uniquely represent one
        player.
        The `token` must be unique otherwise a `ValueError` will be raised.
        '''
        if token in Player.__usedTokens:
            raise ValueError(f"The token '{token}' is not unique")

        Player.__usedTokens.add(token)

        self.__name: str = name
        self.__token: str = token
    
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
