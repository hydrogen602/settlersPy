import pytest
import os
import sys
import json

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

from gameServer import playerCode, extraCode, mapCode, game
from gameServer.extraCode.util import _debugSetSeed

@pytest.fixture(scope="module")
def setupGame():
    _debugSetSeed('42')
    gameMap = mapCode.GameMap()
    gameMap.generateHexagonalArea(2)

    # with open('run.log', 'w') as f: # for debug
    #     f.write(gameMap.getAsJson())

    g = game.Game(gameMap)
    return g

@pytest.mark.incremental
class TestGame:
    
    def testBasic(self, setupGame):
        g: game.Game = setupGame
        assert g.playerManager.getPlayerCount() == 0
        assert len(g.gameMap.tiles) == 7

        with open('tests/runMap.json') as f:
            # as the random num gen's seed gets set the map will be the same
            standard = json.load(f) 
            current = json.loads(g.gameMap.getAsJson())
            assert standard == current

        with pytest.raises(extraCode.NotSetupException):
            g.currentTurn
        
        x = g.toJsonSerializable()
        assert 'gameStarted' in x
        assert not x['gameStarted']
    
    def testAddPlayers(self, setupGame):
        g: game.Game = setupGame
        g.addPlayer(playerCode.Player('test1', None, 'blue'))
        g.addPlayer(playerCode.Player('test2', None, 'red'))

        assert g.playerManager.getPlayerCount() == 2

        g.startGame()

        with pytest.raises(extraCode.AlreadySetupException):
            g.addPlayer(playerCode.Player('test3', None, 'green'))

        assert g.playerManager.isGameStarted()
        ls = list(g.playerManager.getPlayerTurnOrderIterator())

        assert len(ls) == 2
        for tmp in ls:
            p: playerCode.Player = tmp
            assert g.playerManager.getPlayer(p.token)
        
        assert ls[0] != ls[1]

        ls2 = list(g.playerManager.getPlayerTurnOrderIterator())
        
        assert ls2 == ls
    
    def testGameStart(self, setupGame):
        g: game.Game = setupGame

        assert g.playerManager.isGameStarted()
        assert g.playerManager.getPlayerCount() == 2

        assert g.currentTurn.dieValue is None

        tmp = g.currentTurn.currentPlayer.inventory.ownedLineFeatures
        assert len(tmp) == 1
        assert isinstance(tmp[0], mapCode.Road)
        assert not tmp[0].isPlaced

        tmp2 = g.currentTurn.currentPlayer.inventory.ownedPointFeatures
        assert len(tmp2) == 1
        assert isinstance(tmp2[0], mapCode.Settlement)
        assert not tmp2[0].isPlaced

        p = g.currentTurn.currentPlayer
        with pytest.raises(extraCode.ActionError):
            g.nextTurn()
        
        assert g.currentTurn.currentPlayer == p

        with pytest.raises(extraCode.ActionError):
            g.currentTurn.currentPlayer.inventory.placeLineFeature(0, extraCode.HexPoint(0, 0), extraCode.HexPoint(0, 1), g.currentTurn)

        with pytest.raises(IndexError):
            g.currentTurn.currentPlayer.inventory.placePointFeature(1, extraCode.HexPoint(0, 0), g.currentTurn)


    def testFirstRound(self, setupGame):
        g: game.Game = setupGame

        assert g.currentTurn.roundNum == 0

        p = g.currentTurn.currentPlayer
        
        g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(0, 0), g.currentTurn)

        with pytest.raises(extraCode.ActionError):
            g.currentTurn.currentPlayer.inventory.placeLineFeature(0, extraCode.HexPoint(0, 0), extraCode.HexPoint(0, -1), g.currentTurn)

        with pytest.raises(extraCode.ActionError):
            g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(0, 0), g.currentTurn)
        
        g.currentTurn.currentPlayer.inventory.placeLineFeature(0, extraCode.HexPoint(0, 0), extraCode.HexPoint(0, 1), g.currentTurn)

        g.nextTurn()

        assert p != g.currentTurn.currentPlayer

        with pytest.raises(extraCode.ActionError):
            g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(0, 0), g.currentTurn)
        with pytest.raises(extraCode.ActionError):
            g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(1, 0), g.currentTurn)
        
        g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(2, 0), g.currentTurn)
        g.currentTurn.currentPlayer.inventory.placeLineFeature(0, extraCode.HexPoint(2, 0), extraCode.HexPoint(2, 1), g.currentTurn)

        g.nextTurn()

        assert p == g.currentTurn.currentPlayer
        assert g.currentTurn.roundNum == 1

    def testSecondRound(self, setupGame):
        g: game.Game = setupGame

        assert g.currentTurn.roundNum == 1

        p = g.currentTurn.currentPlayer
        
        g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(0, 2), g.currentTurn)
        g.currentTurn.currentPlayer.inventory.placeLineFeature(0, extraCode.HexPoint(0, 2), extraCode.HexPoint(0, 3), g.currentTurn)

        g.nextTurn()

        assert p != g.currentTurn.currentPlayer

        g.currentTurn.currentPlayer.inventory.placePointFeature(0, extraCode.HexPoint(2, 2), g.currentTurn)
        g.currentTurn.currentPlayer.inventory.placeLineFeature(0, extraCode.HexPoint(2, 2), extraCode.HexPoint(2, 3), g.currentTurn)

        g.nextTurn()

        assert p == g.currentTurn.currentPlayer
        assert g.currentTurn.roundNum == 2
    
    def testThirdAndForthRound(self, setupGame):
        # rolls are 9, 9, 5
        g: game.Game = setupGame

        assert g.currentTurn.roundNum == 2

        p = g.currentTurn.currentPlayer
        g.nextTurn()
        assert p != g.currentTurn.currentPlayer
        g.nextTurn()
        assert p == g.currentTurn.currentPlayer

        assert g.currentTurn.roundNum == 3

        p = g.currentTurn.currentPlayer

        # should have gotten something this turn
        assert g.currentTurn.currentPlayer.inventory.getCount(extraCode.Resource.Ore) == 1

        g.nextTurn()

        assert p != g.currentTurn.currentPlayer

        g.nextTurn()

        assert p == g.currentTurn.currentPlayer
        assert g.currentTurn.roundNum == 4
        

