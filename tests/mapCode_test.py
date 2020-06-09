import pytest

import os
import sys

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

from gameServer.mapCode.util import HexPoint, Biome

class TestHexPoint:
    def testBasics(self):
        h = HexPoint(1, 5)
        assert h.row == 1
        assert h.col == 5
        assert h.getAsTuple() == (1, 5)
    
    def testMethods(self):
        h1 = HexPoint(2, 3)
        h2 = HexPoint(2, 5)
        h3 = HexPoint(2, 5)
        h4 = HexPoint(4, 10)

        assert h1 != h2
        assert not h1 == h2

        assert h2 == h3
        assert not h2 != h3

        assert h2 + h3 == h4
        assert (h3 - h1).getAsTuple() == (0, 2)

        d = h1.toJsonSerializable()
        assert 'row' in d
        assert 'col' in d
        assert d['row'] == 2
        assert d['col'] == 3

class TestBiome:
    def testOne(self):
        for b in Biome:
            assert isinstance(b, str)

    