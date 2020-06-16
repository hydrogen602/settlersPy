from typing import Union, Tuple, List
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

from .. import playerCode


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
        self.__token = self.factory.register(self, clientTypeRequest) # pylint: disable=no-member

    def onOpen(self):
        print('WebSocket connection open')

    def onClose(self, wasClean, code, reason):
        print('WebSocket connection closed: {0}'.format(reason))

        # tell the factory that this connection is dead
        self.factory.unregister(self) # pylint: disable=no-member

    def onMessage(self, msg, isBinary):
        msg = msg.decode()

        if msg.lower() == 'hi':
            self.sendMessage(b"Hello")

            msg = json.dumps({'token': self.factory.getToken(self)}) # pylint: disable=no-member
            self.sendMessage(msg.encode())

        elif msg == 'history':
            self.factory.sendHistory(self) # pylint: disable=no-member

        else:
            try:
                obj = json.loads(msg)
                if type(obj) == 'str':
                    raise json.decoder.JSONDecodeError

                print("Got json msg:", obj)

                self.factory.onMessage(obj) # pylint: disable=no-member
                #m = Message(mechanics.PlayerManager.instance.getPlayer(self.token), obj, self.factory)

                #self.factory.callbackHandler(m, self)   
            except json.decoder.JSONDecodeError:
                print("Error: Invalid JSON:", msg)


class ServerFactory(WebSocketServerFactory):
    '''
    Keeps track of all connections and relays data to other clients
    '''

    def __init__(self, url, f, init_msgs: List[str], playerManage: playerCode.PlayerManager, serverCallback):
        '''
        Initializes the class
        Args:
            url (str): has to be in the format of "ws://127.0.0.1:8008"
            f (file): a writable file for logging
        
        The playerManager should be shared with the GameManager
        '''

        self.playerManager: playerCode.PlayerManager = playerManage

        self.file = f

        self.history = list(init_msgs)

        self.serverCallback = serverCallback

        WebSocketServerFactory.__init__(self, url)
    
    def getToken(self, client: ServerProtocol) -> str:
        t = client.token
        if t is None:
            raise Exception('client has not yet registered. This error should not occur ever')

        return t
    
    def sendHistory(self, client):
        for msg in self.history:
            client.sendMessage(msg.encode())
    
    def onMessage(self, obj: dict):
        self.serverCallback(obj)

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
            return None

        
        tmp: str = clientTypeRequest.strip()
        tmpLs = tmp.split('/')
        del tmp

        l = len(tmpLs)
        if l == 1:
            name = tmpLs[0]
        elif l == 2:
            name = tmpLs[0]
            token = tmpLs[1]
        else:
            print('name missing')
            client.sendHttpErrorResponse(404, 'Name missing')
            #client.sendClose()
            return None
        
        # print('clientTypeRequest =', len(clientTypeRequest.strip().split('/')))
        
        if token is None:
            if self.playerManager.isGameStarted():
                print('game already started, can\'t join')
                client.sendHttpErrorResponse(403, 'Game already started, can\'t join')
                return None
            
            p: playerCode.Player = playerCode.Player(name, client, color='green')
            print("New player:", p)
            self.playerManager.addPlayer(p)

            return p.token

        else:
            if token in self.playerManager:
                print("Reconnecting player:", token)
                p = self.playerManager[token]
                p.reconnect(client)
            else:
                print("Unknown token:", token)
                client.sendHttpErrorResponse(403, 'Unknown token given')
                #client.sendClose()
                return None
        
            return p.token

    def unregister(self, client):
        token = client.token
        if token in self.playerManager:
            print("Disconnected player:", token)
            self.playerManager[token].disconnect()
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

        for p in self.playerManager:
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
            p = self.playerManager.getPlayer(token)
            if p is not None and p.isConnected():
                p.connection.sendMessage(encoded)