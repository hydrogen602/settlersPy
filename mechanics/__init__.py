'''
Mechanics should be the core systems of the game, generalized.
Game rules or features should not be found in here, just an API
that supports the addition of game rules
'''

from .player import Player
from .playerManager import PlayerManager

from .event import Event, ActionEvent
