from typing import Dict, List

from ..extraCode.location import Resource
from ..extraCode.util import ActionError
from .player import Player


class Trade:

    def __init__(self, cost: Dict[Resource, int], goodsOffered: Dict[Resource, int]):
        self._cost: Dict[Resource, int] = cost
        self._goodsOffered: Dict[Resource, int] = goodsOffered
    
    def purchase(self, player: Player):
        '''
        throws `ActionError`.
        player is the one accepting the trade
        '''
        player.requireResources(self._cost) # raises ActionError

        player.takeResources(self._cost)
        player.giveResources(self._goodsOffered)


class InterPlayerTrade(Trade):

    def __init__(self, cost: Dict[Resource, int], goodsOffered: Dict[Resource, int], offeror: Player, offerees: List[Player] = []):
        '''
        Offeror is the one proposing the offer,
        Offerees is the recipients of the offer.
        If Offerees is empty, then anyone can accept the offer.

        InterPlayerTrade are for only a single trade and so become
        invalid after a successful trade.

        Throws ActionError if the Offeror does not have what he offers
        '''
        offeror.requireResources(goodsOffered) # throws ActionError

        self.__offeror: Player = offeror
        self.__offerees: List[Player] = offerees

        self.__closedDeal = False # whether the deal has been closed
        self.__invalid = False # whether the deal has been invalidated
        super().__init__(cost, goodsOffered)
    
    def __isValidOfferee(self, player: Player) -> bool:
        '''
        Returns whether or not this player can accept the given trade deal.
        '''
        return len(self.__offerees) == 0 or player in self.__offerees
        # len(self.__offerees) == 0 means anyone can accept
        # player in self.__offerees checks if the player is in the list of accepted players
            
    def purchase(self, player: Player):
        # errors here would go to player
        if not self.__isValidOfferee(player):
            raise ActionError(f"Player is not allowed to take this trade offer")
        if self.__invalid:
            raise ActionError(f"This trade offer is invalid due to {self.__offeror.name}")
        if self.__closedDeal:
            raise ActionError(f"This offer has already been accepted")

        if not self.__offeror.hasResources(self._goodsOffered):
            # offeror no longer has what he offered
            self.__invalid = True
            raise ActionError(f"{self.__offeror.name} doesn't have what he/she offered")

        player.requireResources(self._cost)

        # both have what they wish to trade

        player.takeResources(self._cost)
        self.__offeror.takeResources(self._goodsOffered)

        player.giveResource(self._goodsOffered)
        self.__offeror.giveResources(self._cost)

        self.__closedDeal = True



