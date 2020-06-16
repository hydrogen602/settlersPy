import pytest

import os
import sys

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

from gameServer.playerCode.player import Player
import gameServer.playerCode.inventory as inventory
import gameServer.extraCode.util as util
import gameServer.extraCode.location as location

@pytest.fixture
def player():
    return Player('testName', None, 'blue')

@pytest.fixture
def player2():
    return Player('testName2', None, 'red')

class TestPlayer:

    def testBasic(self, player: Player):
        assert player.name == 'testName'
        assert player.connection is None
        assert player.color == 'blue'
        assert not player.isConnected()
        assert isinstance(player.token, str)
        
        player.checkFinishTurn()
    
    def testRobber(self, player: Player):
        assert not player.canMoveRobber
        player.playerMustMoveRobber()
        assert player.canMoveRobber

        with pytest.raises(util.ActionError):
            player.checkFinishTurn()

    def testInv(self, player: Player):
        assert isinstance(player.inventory, inventory.ExpandedInventory)
        assert player.inventory.totalResourceCount() == 0
        
        for e in location.Resource:
            assert player.hasResource(e, 0)
            assert not player.hasResource(e, 1)
        
        with pytest.raises(ValueError):
            player.takeResource(location.Resource.Brick, 2)
        
        player.giveResource(location.Resource.Lumber, 3)
        assert player.hasResource(location.Resource.Lumber, 0)
        assert player.hasResource(location.Resource.Lumber, 1)
        assert player.hasResource(location.Resource.Lumber, 2)
        assert player.hasResource(location.Resource.Lumber, 3)
        assert not player.hasResource(location.Resource.Lumber, 4)

        with pytest.raises(ValueError):
            player.takeResource(location.Resource.Lumber, 5)
        
        assert player.hasResource(location.Resource.Lumber, 3)

        player.takeResource(location.Resource.Lumber, 2)

        assert player.hasResource(location.Resource.Lumber, 0)
        assert player.hasResource(location.Resource.Lumber, 1)
        assert not player.hasResource(location.Resource.Lumber, 2)

        with pytest.raises(ValueError):
            player.takeResource(location.Resource.Lumber, 2)
    
    def testEq(self, player: Player, player2: Player):
        tmp = player
        assert player == tmp
        assert not player != tmp
        assert not player == player2
        assert player != player2




        
