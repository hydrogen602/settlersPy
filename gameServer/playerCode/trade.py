from typing import Dict, List

from ..extraCode.location import Resource
from ..extraCode.util import ActionError
from .player import Player


class Trade:

    def __init__(self, cost: Dict[Resource, int], goodsOffered: Dict[Resource, int]):
        self.__cost: Dict[Resource, int] = cost
        self.__goodsOffered: Dict[Resource, int] = goodsOffered
    
    def purchase(self, player: Player):
        '''
        throws `ActionError`.
        player is the one accepting the trade
        '''
        player.requireResources(self.__cost) # raises ActionError

        player.takeResources(self.__cost)
        player.giveResources(self.__goodsOffered)


class InterPlayerTrade(Trade):

    def __init__(self, cost: Dict[Resource, int], goodsOffered: Dict[Resource, int], offeror: Player, offerees: List[Player] = []):
        '''
        Offeror is the one proposing the offer,
        Offerees is the recipients of the offer.
        If Offerees is empty, then anyone can accept the offer.

        InterPlayerTrade are for only a single trade and so become
        invalid after a successful trade.
        '''
        self.__offeror: Player = offeror
        self.__offerees: List[Player] = offerees

        self.__closedDeal = False
        super().__init__(cost, goodsOffered)
    
    def __isValidOfferee(self, player: Player) -> bool:
        '''
        Returns whether or not this player can accept the given trade deal.
        '''
        return len(self.__offerees) == 0 or player in self.__offerees
        # len(self.__offerees) == 0 means anyone can accept
        # player in self.__offerees checks if the player is in the list of accepted players
            
    def purchase(self, player: Player):
        if not self.__isValidOfferee(player):
            raise ActionError(f"Player is not allowed to take this trade offer")


        super().purchase(player)


