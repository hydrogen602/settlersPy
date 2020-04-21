#!/usr/bin/env python3

from sys import version_info

if version_info.major >= 3 and version_info.minor >= 8:
    pass # all good
else:
    raise Exception('This code needs Python 3.8 or higher due to use of annotations')

from server import Server
from tools import typeCheck, customJsonEncoder
from gameMap import GameMap

import mechanics

import json

class GameManager:

    def __init__(self):
        self.m: GameMap = GameMap()
        self.pm: mechanics.PlayerManager = mechanics.PlayerManager()

        self.serv = Server(ip='localhost', port=5000, callbackFunc=self.event, init_msgs=(self.m.getAsJson(),), playerManage=self.pm)
    
    def event(self, player: mechanics.Player, data: dict):
        '''
        event should be called by the `ServerFactory` when
        a new message has come from a client

        action messages should have the format:
        {"type": "action", "group": groupName, "name": actionName, "data": extraData }
        where the "data" tag is optional
        '''
        typeCheck(data, dict)
        print(player, data)

        if 'action' in data:
            if data['action'] == 'purchase':
                if 'name' not in data:
                    print('Malformed JSON: missing name tag in player action')
                    print('->',player, data)
                    return json.dumps({"Test": True})
                
                print(f'Player {player} would like to buy a {data["name"]}')
                # isValid?
                pass

        return json.dumps({"Test": True})
    
    def newPlayer(self, p: mechanics.Player):
        self.pm.addPlayer(p)

    def run(self):
        print('Running Server...')
        self.serv.run()

if __name__ == '__main__':
    g = GameManager()
    g.run()

