from __future__ import annotations

from mechanics.player import Player
from mechanics.event import Event
from tools import typeCheck

class Message:

    def __init__(self, fromPlayer: Player, msg: dict, serverFactoryInstance: 'ServerFactory'):
        #typeCheck(fromPlayer, Player)
        #typeCheck(msg, dict)

        self.__player: Player = fromPlayer 
        self.__msg_raw: dict = msg
        self.__serverFactoryInstance: 'ServerFactory' = serverFactoryInstance

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
    def msg(self) -> dict:
        return self.__msgProcessed
    
    @property
    def msg_raw(self) -> dict:
        return self.__msg_raw
    
    @property
    def serverFactoryInstance(self):
        return self.__serverFactoryInstance
    
    def doAction(self):
        return self.__msgProcessed.doAction(self)