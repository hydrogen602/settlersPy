from enum import Enum

class Resource(Enum):
    pass

class PrimaryResource(Resource):
    Wheat = 0
    Sheepie = 1
    Lumber = 2
    Ore = 3
    Brick = 4

class Biome:
    primaryRes: PrimaryResource = None

    biomeList: list = []
    '''
    A list of all biomes that are subclassed of this class
    '''

    def __init__(self, *args, **kwargs):
        '''
        Biomes are more like a tag and so shouldn't be
        instantiated.
        '''
        raise TypeError("Biome shouldn't be instantiated")

    def __init_subclass__(cls):
        assert hasattr(cls, 'primaryRes')
        assert isinstance(getattr(cls, 'primaryRes'), PrimaryResource)

        Biome.biomeList.append(cls) # add new biome to list of biomes
    


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
