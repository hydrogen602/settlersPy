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
from twisted.internet import reactor  # ,task

IP = '127.0.0.1'

PORT = 5050


class ServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):

        print(request.path)
        # debug information
        print('Client connecting & registering: {0}'.format(request.peer))
        clientTypeRequest = request.path

        self.testState = 0

        # process the type of request
        if clientTypeRequest.startswith('/'):
            # remove the slash if there is one
            clientTypeRequest = clientTypeRequest[1:]

        # tell the factory to remember the connection
        self.factory.register(self, clientTypeRequest)

    def onOpen(self):
        print('WebSocket connection open')

    def onClose(self, wasClean, code, reason):
        print('WebSocket connection closed: {0}'.format(reason))

        # tell the factory that this connection is dead
        self.factory.unregister(self)
    
    def isReady(self):
        return self.testState == 2

    def onMessage(self, msg, isBinary):
        msg = msg.decode()

        if msg == 'Hi':
            self.sendMessage(b"Hello")
            self.testState = 1

            msg = json.dumps({'token': self.factory.getToken(self)})
            self.sendMessage(msg.encode())
            return
        elif msg == 'history':
            self.factory.sendHistory(self)
        
        try:
            obj = json.loads(msg)

            if "test" in obj and obj["test"] == "verify":
                b = json.dumps({"test": "echo verified"}).encode()
                self.sendMessage(b)
                self.testState = 2
            else:
                pass # echo to others
                self.factory.broadcast(msg, self)
        
        except json.decoder.JSONDecodeError:
            print("Error: Invalid JSON:", msg)


class ServerFactory(WebSocketServerFactory):
    '''
    Keeps track of all connections and relays data to other clients
    '''

    def __init__(self, url, f):
        '''
        Initializes the class
        Args:
            url (str): has to be in the format of "ws://127.0.0.1:8008"
        '''
        self.players = {}

        self.file = f

        self.history = []

        WebSocketServerFactory.__init__(self, url)
    
    def getToken(self, client) -> str:
        for token in self.players:
            if self.players[token] is client:
                return token
        return ''
    
    def sendHistory(self, client):
        for msg in self.history:
            client.sendMessage(msg.encode())

    def register(self, client, clientTypeRequest):
        if len(clientTypeRequest.strip()) > 0:
            token = clientTypeRequest.strip()
            if token in self.players:
                print("Reconnecting player:", token)
                self.players[token] = client

            # find old connection
        else:
            token = secrets.token_urlsafe(20)
            print("Connecting player:", token)
            self.players[token] = client

    def unregister(self, client):
        for token in self.players:
            if self.players[token] is client:
                print("Disconnecting player:", token)
                self.players[token] = None
    
    def broadcast(self, msg: str, sourceConnection: ServerProtocol):
        f.write(msg + '\n')
        f.flush()
        self.history.append(msg)
        
        for token in self.players:
            if self.players[token] and self.players[token]: # is None if disconnected
                self.players[token].sendMessage(msg.encode())
        

if __name__ == '__main__':
    # display debug information to stdout for now
    log.startLogging(sys.stdout)  # TODO: replace with log file (maybe)

    f = open('gameMsgLog.log', 'w')

    # Setup server factory
    server = ServerFactory(u'ws://{}:{}'.format(IP, PORT), f)
    server.protocol = ServerProtocol

    # setup listening server
    reactor.listenTCP(PORT, server)

    try:
        # start listening for and handling connections
        reactor.run()
    finally:
        f.close()
        # if logs are sent to a file instead of stdout
        # the file should be closed here with f.close()
