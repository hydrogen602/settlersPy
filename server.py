#!/usr/bin/env python3.7

'''
Author: Jonathan Rotter
Server code

Required 3rd-party libraries:
`autobahn`
`twisted`
'''
import sys
import json
import secrets

# importing the necessary objects
# autobahn does websocket stuff, but relies on twisted
from autobahn.twisted.websocket import \
    WebSocketServerProtocol, WebSocketServerFactory

# twisted does asynchronous code execution needed for websockets
from twisted.python import log
from twisted.internet import reactor

from typing import Callable, Tuple, Union, List

from tools import typeCheck
import mechanics

class ServerProtocol(WebSocketServerProtocol):
    '''
    Sending a message of 'Hi' returns two messages, 'Hello' and a json
    that is {'token': token}

    Sending a message of 'history' returns all previously send messages
    '''

    @property
    def token(self) -> Union[str, None]:
        try:
            return self.__token
        except AttributeError:
            return None

    def onConnect(self, request):

        print(request.path)
        # debug information
        print('Client connecting & registering: {0}'.format(request.peer))
        clientTypeRequest = request.path

        # process the type of request
        if clientTypeRequest.startswith('/'):
            # remove the slash if there is one
            clientTypeRequest = clientTypeRequest[1:]

        # tell the factory to remember the connection
        self.__token = self.factory.register(self, clientTypeRequest)

    def onOpen(self):
        print('WebSocket connection open')

    def onClose(self, wasClean, code, reason):
        print('WebSocket connection closed: {0}'.format(reason))

        # tell the factory that this connection is dead
        self.factory.unregister(self)

    def onMessage(self, msg, isBinary):
        msg = msg.decode()

        if msg.lower() == 'hi':
            self.sendMessage(b"Hello")

            msg = json.dumps({'token': self.factory.getToken(self)})
            self.sendMessage(msg.encode())

        elif msg == 'history':
            self.factory.sendHistory(self)

        else:
            try:
                obj = json.loads(msg)
                if type(obj) == 'str':
                    raise json.decoder.JSONDecodeError

                self.factory.callbackHandler(obj, self)   
            except json.decoder.JSONDecodeError:
                print("Error: Invalid JSON:", msg)


class ServerFactory(WebSocketServerFactory):
    '''
    Keeps track of all connections and relays data to other clients
    '''

    def __init__(self, url, f, callbackFunc: Callable[[str, dict], str], 
                 init_msgs: Tuple[str] = (), playerManage: mechanics.PlayerManager = None):
        '''
        Initializes the class
        Args:
            url (str): has to be in the format of "ws://127.0.0.1:8008"
            f (file): a writable file for logging
        
        The playerManager should be shared with the GameManager
        '''
        typeCheck(playerManage, mechanics.PlayerManager)

        self.pm: mechanics.PlayerManager = playerManage

        self.file = f

        self.callbackFunc = callbackFunc

        self.history = list(init_msgs)

        WebSocketServerFactory.__init__(self, url)
    
    def callbackHandler(self, msg: dict, client: ServerProtocol):
        '''
        call the callbackFunc to notify the game manager of a new
        message
        '''
        jsonMsg = self.callbackFunc(client.token, msg)
        self.broadcastToAll(jsonMsg)
    
    def getToken(self, client: ServerProtocol) -> str:
        t = client.token
        if t is None:
            raise Exception('client has not yet registered. This error should not occur ever')

        return t
    
    def sendHistory(self, client):
        for msg in self.history:
            client.sendMessage(msg.encode())

    def register(self, client: ServerProtocol, clientTypeRequest: str) -> Union[str, None]:
        '''
        Called by any new connecting client to address
        whether they are a new player or a reconnecting one.

        The request line should be /name/token
        or /name but the first / is removed by onConnect

        In the case that the name is missing the method will
        return `None` and trigger a 400 error. Same goes for if
        a token is given that the server does not know.        
        '''
        token = None
        name = None

        if len(clientTypeRequest.strip()) == 0:
            print('name missing')
            client.sendHttpErrorResponse(404, 'Name missing')
            #client.sendClose()
        
        tmp = clientTypeRequest.strip()
        tmp = tmp.split('/')
        l = len(tmp)
        if l == 1:
            name = tmp[0]
        elif l == 2:
            name = tmp[0]
            token = tmp[1]
        else:
            print('name missing')
            client.sendHttpErrorResponse(404, 'Name missing')
            #client.sendClose()
            return None
        
        # print('clientTypeRequest =', len(clientTypeRequest.strip().split('/')))
        
        p: mechanics.Player = None

        if token is None:
            p = mechanics.Player(name, client)
            print("New player:", p.token)
            self.pm.addPlayer(p)

        if token is not None:
            if token in self.pm:
                print("Reconnecting player:", token)
                p = self.pm.getPlayer(token)
                p.reconnect(client)
            else:
                print("Unknown token:", token)
                client.sendHttpErrorResponse(403, 'Unknown token given')
                #client.sendClose()
                return None
                # p = mechanics.Player(name, client)
                # self.pm.addPlayer(p)
        
        return p.token

    def unregister(self, client):
        token = client.token
        if token in self.pm:
            print("Disconnected player:", token)
            self.pm[token].disconnect()
        elif token is None:
            print("Player disconnected before assigned token:", token)
        else:
            print("Disconnected player, but token not found?:", token)
    
    def broadcastToAll(self, msg: str): # sourceConnection: ServerProtocol
        '''
        Sends a message of type `str` to all currently connected
        players
        '''
        self.file.write(msg + '\n')
        self.file.flush()
        self.history.append(msg)

        encoded = msg.encode()

        for p in self.pm:
            if p.isConnected():
                p.connection.sendMessage(encoded)
    
    def broadcastToSome(self, msg: str, tokenList: List[str], writeToHistory: bool = False):
        '''
        Sends a message of type `str` to all currently connected
        players whose token is found in the list.
        `writeToHistory`  determines whether or not this message should
        be included in the history.
        '''
        if writeToHistory:
            self.file.write(msg + '\n')
            self.file.flush()
            self.history.append(msg)
        
        encoded = msg.encode()
        
        for token in tokenList:
            p = self.pm.getPlayer(token)
            if p is not None and p.isConnected():
                p.connection.sendMessage(encoded)

        

class Server:

    def __init__(self, ip: str = '127.0.0.1', port: int = 5000, callbackFunc: Callable[[str, dict], str] = None, 
                 init_msgs: Tuple[str] = (), playerManage: mechanics.PlayerManager = None):
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
        self.ip = ip
        self.port = port

        if not callbackFunc:
            # def dummyFunc(self, d: dict) -> str:
            #     print('[callbackFunc]', d)
            #     return '{}'

            # callbackFunc = dummyFunc

            raise TypeError('Missing keyword argument "callbackFunc" which should be of type "Callable[[dict], str]"')

        self.file = open('gameMsgLog.log', 'w')

        # Setup server factory
        self.server = ServerFactory(u'ws://{}:{}'.format(ip, port), self.file, callbackFunc, init_msgs=init_msgs, playerManage=playerManage)
        self.server.protocol = ServerProtocol

        # setup listening server
        reactor.listenTCP(port, self.server)

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
            reactor.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.file.close()
            # if logs are sent to a file instead of stdout
            # the file should be closed here with f.close()
