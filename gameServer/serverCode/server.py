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

from twisted.python import log, logfile # type: ignore
from twisted.internet import reactor # type: ignore

from .. import playerCode
from .. import extraCode
from .. import mapCode
from .. import game
from .factoryAndProtocol import ServerFactory, ServerProtocol
from .jsonParser import JsonParserType


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
    
    def __updateClientInventory(self, token: Optional[str] = None):
        if token is None:
            pIter: playerCode.Player
            for pIter in self.g.playerManager:
                self.server.broadcastToSome(extraCode.getAsJson(pIter.inventory), [pIter.token])
            return

        p = self.g.playerManager.getPlayer(token)
        if p is None:
            print(f'RuntimeError: token of client not in playerManager. This should not happen')
            return
        
        self.server.broadcastToSome(extraCode.getAsJson(p.inventory), [token])
    
    def callback(self, obj: dict, client: ServerProtocol):
        token = client.token
        if token is None:
            print(f'Error, toke is None???? client={client} obj={obj}')
            return
                
        if 'debug' in obj:
            debugCmd = obj['debug']
            if debugCmd == 'startGame':
                print('Game started')
                self.g.startGame()
                self.server.broadcastToAll(self.g.getAsJson())

                json_msg = { 'type': 'notification', 'content': 'Game Started' }
                self.server.broadcastToAll(json.dumps(json_msg))

                self.server.broadcastToAll(extraCode.getAsJson(self.g.currentTurn)) # send out turn

                #print('sent:', extraCode.getAsJson(self.g.currentTurn))
        else:
            try:
                request = JsonParserType(obj)

                if request.type_ == 'action':
                    if request.content == 'nextTurn':
                        self.g.nextTurn()
                        self.__updateClientInventory()
                
                    elif request.content == 'placeSettlement':
                        point, indexTmp = request.requireArgs(2) # pylint: disable=unbalanced-tuple-unpacking
                        hp: extraCode.HexPoint = extraCode.HexPoint.fromJson(point)
                        index: int = int(indexTmp)

                        if len(self.g.currentTurn.currentPlayer.inventory.ownedPointFeatures) == 0:
                            raise extraCode.ActionError('You own no settlements or cities')
                        
                        self.g.currentTurn.currentPlayer.inventory.placePointFeature(index, hp, self.g.currentTurn)
                        self.server.updateAll()
                    
                    #{'type': 'action', 'content': 'placeRoad', 'args': [{'__name__': 'HexPoint', 'row': 1, 'col': 1}, {'__name__': 'HexPoint', 'row': 1, 'col': 2}, None]}
                    elif request.content == 'placeRoad':
                        p1, p2, indexTmp = request.requireArgs(3)
                        hp1: extraCode.HexPoint = extraCode.HexPoint.fromJson(p1)
                        hp2: extraCode.HexPoint = extraCode.HexPoint.fromJson(p2)
                        index = int(indexTmp)

                        if len(self.g.currentTurn.currentPlayer.inventory.ownedLineFeatures) == 0:
                            raise extraCode.ActionError('You own no roads')

                        self.g.currentTurn.currentPlayer.inventory.placeLineFeature(index, hp1, hp2, self.g.currentTurn)
                        self.server.updateAll()
                
                elif request.type_ == 'update':
                    if request.content == 'inventory':
                        self.__updateClientInventory(token)

            except extraCode.ActionError as e:
                s = ' '.join(e.args)
                
                json_msg = { 'type': 'error', 'content': 'ERROR: ' + s }
                self.server.broadcastToSome(json.dumps(json_msg), [token])

    def run(self):
        '''
        Run the server. This method will not return
        until the server is ended by an Exception like ^C.

        init_msgs are for messages that should be send to the player
        immediately, like the game map for example.
        '''

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
    log.startLogging(sys.stdout, setStdout=True)

    logFile = logfile.LogFile.fromFullPath('twistedLog.log')
    log.addObserver(log.FileLogObserver(logFile).emit)

    s = Server()
    s.run()
