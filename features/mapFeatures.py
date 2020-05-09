from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from point import HexPoint
    from mechanics.player import Player
    from biome import Biome

import mechanics.gameMap as gameMap

class Settlement(gameMap.ProducingOutpost):

    def __init__(self, pos: HexPoint, owner: Player):
        super().__init__(pos, owner)
    
    def harvestResource(self, biome: Biome):
        self.owner.giveResource(biome.primaryRes)


class City(gameMap.ProducingOutpost):

    def __init__(self, pos: HexPoint, owner: Player):
        super().__init__(pos, owner)
    
    def harvestResource(self, biome: Biome):
        self.owner.giveResource(biome.primaryRes, count=2)
