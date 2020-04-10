

from enum import Enum

class PrimaryResource(Enum):
    Wheat = 0
    Sheepie = 1
    Lumber = 2
    Ore = 3
    Brick = 4

class Biome:
    def __init__(self, *args, **kwargs):
        raise TypeError("These shouldn't be instantiated")

    def __init_subclass__(subCls):
        assert hasattr(subCls, 'primaryRes')
        assert isinstance(getattr(subCls, 'primaryRes'), PrimaryResource)

class WheatField(Biome):
    primaryRes: PrimaryResource = PrimaryResource.Wheat

class Grassland(Biome):
    primaryRes: PrimaryResource = PrimaryResource.Sheepie

class Forest(Biome):
    primaryRes: PrimaryResource = PrimaryResource.Lumber

class Mountains(Biome):
    primaryRes: PrimaryResource = PrimaryResource.Ore

class Quarry(Biome):
    primaryRes: PrimaryResource = PrimaryResource.Brick
