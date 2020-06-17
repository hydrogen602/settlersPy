'''
Server code for setting up a WebSocket server, handling connections, and verifying
connection details.

This code borrows from an earlier project with the CISS ROV Robotics Team,
but still my code


Required 3rd-party libraries:
`autobahn`
`twisted`
'''
import sys
import json
import secrets
from typing import Callable, Tuple, Union, List, Optional

from twisted.python import log # type: ignore
from twisted.internet import reactor # type: ignore

from .. import playerCode
from .. import extraCode
from .. import mapCode
from .. import game
from .factoryAndProtocol import ServerFactory, ServerProtocol


class Server:

    def __init__(self, ip: str = '127.0.0.1', port: int = 5000):
        '''
        A class for managing the code for running the server.
        To setup the server, run `s = Server()`,
        and then run `s.run()` to start it.

        Requires keyword argument `callbackFunc` which should
        be of type `Callable[[str, dict], str]`. This is
        for handling incoming messages and should return
        a status update to all clients. The return type
        should be type `str` and be json. The
        arguments are a unique id for each player as a `str`
        and the message from that player as a `dict`
        '''

        tmpGameMap = mapCode.GameMap()
        tmpGameMap.generateHexagonalArea(2)

        self.g: game.Game = game.Game(tmpGameMap)

        self.ip = ip
        self.port = port

        self.file = open('gameMsgLog.log', 'w')

        # Setup server factory
        self.server = ServerFactory(
            u'ws://{}:{}'.format(ip, port), 
            self.file, 
            g=self.g,
            serverCallback=self.callback
            )
        self.server.protocol = ServerProtocol

        # setup listening server
        reactor.listenTCP(port, self.server) # pylint: disable=no-member
    
    def callback(self, obj: dict):
        if 'debug' in obj:
            debugCmd = obj['debug']
            if debugCmd == 'startGame':
                print('Game started')
                self.g.startGame()
                self.server.broadcastToAll(self.g.getAsJson())

    def run(self):
        '''
        Run the server. This method will not return
        until the server is ended by an Exception like ^C.

        init_msgs are for messages that should be send to the player
        immediately, like the game map for example.
        '''
        # display debug information to stdout for now
        log.startLogging(sys.stdout)  # TODO: replace with log file (maybe)

        try:
            # start listening for and handling connections
            # task.deferLater(reactor, 1, lambda: [self.server.broadcastToAll(msg) for msg in init_msgs])
            reactor.run() # pylint: disable=no-member
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
        finally:
            self.file.close()
            # if logs are sent to a file instead of stdout
            # the file should be closed here with f.close()


def main():
    s = Server()
    s.run()
