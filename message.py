from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.player import Player
    from server import ServerFactory

from mechanics.event import Event
from tools import typeCheck

class Message:

    def __init__(self, fromPlayer: Player, msg: dict, serverFactoryInstance: ServerFactory):
        # serverFactoryInstance is of type ServerFactory
        #typeCheck(fromPlayer, Player)
        #typeCheck(msg, dict)

        self.__player: Player = fromPlayer 
        self.__msg_raw: dict = msg
        self.__serverFactoryInstance: ServerFactory = serverFactoryInstance

        self.__msgProcessed: Event = None

        try:
            self.__msgProcessed = Event.fromJson(msg)
        except Exception as e:
            print("Event JSON parsing failed")
            print(e)

    @property
    def player(self) -> Player:
        return self.__player
    
    @property
    def msg(self) -> Event:
        return self.__msgProcessed
    
    @property
    def msg_raw(self) -> dict:
        return self.__msg_raw
    
    @property
    def serverFactoryInstance(self) -> ServerFactory:
        return self.__serverFactoryInstance
    
    def doAction(self):
        if self.__msgProcessed is None:
            print("Invalid Json caused doAction to be null")
        else:
            return self.__msgProcessed.doAction(self)