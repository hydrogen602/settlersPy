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

from typing import Callable, Tuple

class ServerProtocol(WebSocketServerProtocol):
    '''
    Sending a message of 'Hi' returns two messages, 'Hello' and a json
    that is {'token': token}

    Sending a message of 'history' returns all previously send messages
    '''

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
        self.token = self.factory.register(self, clientTypeRequest)

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

    def __init__(self, url, f, callbackFunc: Callable[[str, dict], str], init_msgs: Tuple[str] = ()):
        '''
        Initializes the class
        Args:
            url (str): has to be in the format of "ws://127.0.0.1:8008"
        '''
        self.players = {}

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
    
    def getToken(self, client) -> str:
        for token in self.players:
            if self.players[token] is client:
                return token
        return ''
    
    def sendHistory(self, client):
        for msg in self.history:
            client.sendMessage(msg.encode())

    def register(self, client, clientTypeRequest) -> str:
        if len(clientTypeRequest.strip()) > 0:
            token = clientTypeRequest.strip()
            if token in self.players:
                print("Reconnecting player:", token)
                self.players[token] = client

        else:
            token = secrets.token_urlsafe(20)
            print("Connecting player:", token)
            self.players[token] = client
        
        return token

    def unregister(self, client):
        for token in self.players:
            if self.players[token] is client:
                print("Disconnected player:", token)
                self.players[token] = None
    
    def broadcastToAll(self, msg: str): # sourceConnection: ServerProtocol
        self.file.write(msg + '\n')
        self.file.flush()
        self.history.append(msg)
        
        for token in self.players:
            if self.players[token]: # is None if disconnected
                self.players[token].sendMessage(msg.encode())
        

class Server:

    def __init__(self, ip: str = '127.0.0.1', port: int = 5000, callbackFunc: Callable[[str, dict], str] = None, init_msgs: Tuple[str] = ()):
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

        # display debug information to stdout for now
        log.startLogging(sys.stdout)  # TODO: replace with log file (maybe)

        self.file = open('gameMsgLog.log', 'w')

        # Setup server factory
        self.server = ServerFactory(u'ws://{}:{}'.format(ip, port), self.file, callbackFunc, init_msgs=init_msgs)
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
        try:
            # start listening for and handling connections
            # task.deferLater(reactor, 1, lambda: [self.server.broadcastToAll(msg) for msg in init_msgs])
            reactor.run()
        finally:
            self.file.close()
            # if logs are sent to a file instead of stdout
            # the file should be closed here with f.close()
