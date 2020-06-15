
import os
from typing import Tuple, Dict, Optional
import curses

from gameServer.game import Game
from gameServer.extraCode.location import HexPoint
from gameServer.extraCode.util import ActionError
from gameServer.playerCode.playerManager import PlayerManager
from gameServer.playerCode.player import Player
from gameServer.mapCode.gameMap import GameMap

'''
     * --- *
    /       \\
   *         *
    \\       /
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
        # print(t, file=log)

        row, col = toRect(t.position)

        writeString(row, col, '* --- *')
        setPoint(row+1, col-1, '/')
        setPoint(row+1, col+7, '\\')

        shortName = t.biome.name[:5]

        writeString(row+2, col-2, '*{:^9}*'.format(shortName))

        writeString(row+3, col-1, '\\{:^7}/'.format(t.diceValue))
        writeString(row+4, col, '* --- *')
    
    for s in gameMap.pointFeatures:
        colorCode = colorLookup[s.owner.color]

        row, col = toRect(s.position)

        setPoint(row, col, 'S', curses.color_pair(colorCode))
    
    for r in gameMap.lineFeatures:
        colorCode = colorLookup[r.owner.color]

        row1, col1 = toRect(r.point1)
        row2, col2 = toRect(r.point2)

        if row1 - row2 == 0:
            midCol = (col1 + col2) // 2
            # --- segment
            writeString(row1, midCol-1, '===', curses.color_pair(colorCode))
        else:
            midCol = (col1 + col2) // 2
            # theres two between col1 and col2 so they're
            # either both odd or both even, and so their sum is even
            midRow = (row1 + row2) // 2
            # same for row
            setPoint(midRow, midCol, 'X', curses.color_pair(colorCode))

    print(gameMap.toJsonSerializable(), file=log)
        


    scr.refresh()


colorLookup: Dict[str, int] = {
    'red': 1,
    'yellow': 2,
    'green': 3
}


def main(stdscr):
    curses.nonl()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)



    gm = GameMap()
    gm.generateHexagonalArea(2)

    g = Game(gm)
    p: PlayerManager = g.playerManager

    players = [
        Player('alpha', None, 'red'),
        Player('beta', None, 'yellow'),
        Player('gamma', None, 'green')
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

    roadTmpPointHolder: Optional[HexPoint] = None

    while(True):
        drawMap(g.gameMap, stdscr)
        stdscr.addstr(0, 0, f"SettlersPy")
        stdscr.addstr(1, 0, f"Current Player: {g.currentTurn.currentPlayer.name}")
        stdscr.addstr(2, 0, f"Round: {g.currentTurn.roundNum}")
        stdscr.addstr(num_rows - 2, 0, ' ' * (num_columns - 2))
        stdscr.addstr(num_rows - 2, 0, str(g.currentTurn.currentPlayer.inventory))

        if roadTmpPointHolder is not None:
            row, col = toRect(roadTmpPointHolder)
            colorNum = colorLookup[g.currentTurn.currentPlayer.color]
            stdscr.addch(row, col, 'R', curses.color_pair(colorNum))

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
        elif key == ord('c'):
            s = ""
            stdscr.addstr(num_rows - 1, 0, f": ", curses.A_BLINK)
            key = stdscr.getch()
            while(key != curses.KEY_ENTER and key != 10 and key != 13):
                if key == curses.KEY_BACKSPACE or key == ord('\b') or key == 127:
                    s = s[:-1]
                    stdscr.addstr(num_rows - 1, 2, f"{s} ")
                    key = stdscr.getch()
                    continue

                s += chr(key)

                stdscr.addstr(num_rows - 1, 2, f"{s}")
                key = stdscr.getch()
            
            stdscr.addstr(num_rows - 1, 0, ' ' * (num_columns - 3))
            s = s.strip().lower()

            if s == 'next':
                try:
                    g.nextTurn()
                except ActionError as e:
                    stdscr.addstr(0, 0, f"SettlersPy: Problem: {e}")
                else:
                    print(f"switched turn {g.currentTurn.currentPlayer.name}", file=log)
                stdscr.clear()
            elif s == 'place s':
                if len(g.currentTurn.currentPlayer.inventory.ownedPointFeatures) == 0:
                    stdscr.addstr(0, 0, f"SettlersPy: Problem: You own no settlements or cities")
                    continue
                try:
                    g.currentTurn.currentPlayer.inventory.placePointFeature(0, atPos, g.currentTurn)
                except ActionError as e:
                    stdscr.addstr(0, 0, f"SettlersPy: Problem: {e}")
            elif s == 'place r':
                if len(g.currentTurn.currentPlayer.inventory.ownedLineFeatures) == 0:
                    stdscr.addstr(0, 0, f"SettlersPy: Problem: You own no roads")
                    continue

                if roadTmpPointHolder is not None:
                    try:
                        g.currentTurn.currentPlayer.inventory.placeLineFeature(0, roadTmpPointHolder, atPos, g.currentTurn)
                        roadTmpPointHolder = None
                    except ActionError as e:
                        stdscr.addstr(0, 0, f"SettlersPy: Problem: {e}")
                else:
                    roadTmpPointHolder = atPos
                
                




if __name__ == '__main__':
    try:
        curses.wrapper(main)
    finally:
        log.close()