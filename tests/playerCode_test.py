import pytest

import os
import sys

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

from gameServer.playerCode.player import Player

class TestPlayer:

    def testBasic(self):
        p = Player('alpha', None)

        assert p.name == 'alpha'
        assert p.connection is None
        assert not p.isConnected()

        p.checkFinishTurn()

        p.canMoveRobber()