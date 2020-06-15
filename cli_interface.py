
import os
from typing import Tuple
import curses

from gameServer.game import Game
from gameServer.extraCode.location import HexPoint
from gameServer.playerCode.playerManager import PlayerManager
from gameServer.playerCode.player import Player
from gameServer.mapCode.gameMap import GameMap

'''
     * --- *
    /       \\
   *         *
    \       /
     * --- *
'''

tmp = os.get_terminal_size()
num_columns = tmp.columns
num_rows = tmp.lines
del tmp

log = open('run.log', 'w')

offsetRow = 5
offsetCol = 20

def toRect(hex: HexPoint, debug=False) -> Tuple[int, int]:
    # translate to rectangular
    row = hex.row * 2
    col = hex.col * 8

    if abs(hex.row % 2) == abs(hex.col % 2):
        if debug: print('shift!', file=log)
        col += 2
    
    return row + offsetRow, col + offsetCol

def drawMap(gameMap: GameMap, scr):
    #screen = [[' '] * num_columns for _ in range(num_rows)]

    def setPoint(row: int, col: int, char: str, *attr):
        assert len(char) == 1
        if row < 0 or row >= num_rows:
            return # offscreen
        if col < 0 or col >= num_columns:
            return # offscreen
        
        scr.addch(row, col, char, *attr)
    
    def writeString(row: int, col: int, s: str, *attr):
        '''
        Write out a string starting at the giving coords
        '''
        for index, char in enumerate(s):
            setPoint(row, col + index, char, *attr)

    for t in gameMap.tiles:
        print(t, file=log)

        row, col = toRect(t.position)

        writeString(row, col, '* --- *')
        setPoint(row+1, col-1, '/')
        setPoint(row+1, col+7, '\\')

        shortName = t.biome.name[:5]

        writeString(row+2, col-2, '*{:^9}*'.format(shortName))

        writeString(row+3, col-1, '\\{:^7}/'.format(t.diceValue))
        writeString(row+4, col, '* --- *')

    scr.refresh()


def main(stdscr):

    gm = GameMap()
    gm.generateHexagonalArea(2)

    g = Game(gm)
    p: PlayerManager = g.playerManager

    players = [
        Player('alpha', None),
        Player('beta', None),
        Player('gamma', None)
    ]

    for pl in players:
        g.addPlayer(pl)

    assert p.getPlayerCount() == len(players)

    assert players[0] == p.getPlayer(players[0].token)

    g.startGame()

    names = [player.name for player in players]
    for player in p.getPlayerTurnOrderIterator():
        names.remove(player.name)
    
    assert len(names) == 0

    

    atPos = HexPoint(0, 0)

    while(True):
        drawMap(g.gameMap, stdscr)
        stdscr.addstr(0, 0, f"Current Player: {g.currentTurn.currentPlayer.name}")
        stdscr.addstr(1, 0, f"Round: {g.currentTurn.roundNum}")

        row, col = toRect(atPos)
        stdscr.move(row, col)

        key: int = stdscr.getch()
        if key == ord('w') or key == curses.KEY_UP:
            atPos = atPos - HexPoint(1, 0)
        elif key == ord('s') or key == curses.KEY_DOWN:
            atPos = atPos + HexPoint(1, 0)
        elif key == ord('a') or key == curses.KEY_LEFT:
            atPos = atPos - HexPoint(0, 1)
        elif key == ord('d') or key == curses.KEY_RIGHT:
            atPos = atPos + HexPoint(0, 1)
        elif key == ord('q'):
            break


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    finally:
        log.close()