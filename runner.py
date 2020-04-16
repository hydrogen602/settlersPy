#!/usr/bin/env python3

from sys import version_info

if version_info.major >= 3 and version_info.minor >= 8:
    pass # all good
else:
    raise Exception('This code needs Python 3.8 or higher due to use of annotations')

from server import Server
from tools import typeCheck, customJsonEncoder
from gameMap import GameMap

import json

class GameManager:

    def __init__(self):
        self.m = GameMap()
        self.serv = Server(ip='localhost', port=5000, callbackFunc=self.event, init_msgs=(self.m.getAsJson(),))
    
    def event(self, playerID: str, data: dict):
        '''
        event should be called by the `ServerFactory` when
        a new message has come from a client
        '''
        typeCheck(data, dict)
        print(playerID, data)
        return json.dumps({"Test": True})

    def run(self):
        print('Running Server...')
        self.serv.run()

if __name__ == '__main__':
    g = GameManager()
    g.run()

