from enum import Enum


class Resource(Enum):
    Wheat = 0
    Sheepie = 1
    Lumber = 2
    Ore = 3
    Brick = 4


class Biome:
    primaryRes: Resource = None
    color: str = None

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
        assert isinstance(getattr(cls, 'primaryRes'), Resource)

        assert hasattr(cls, 'color')
        assert isinstance(getattr(cls, 'color'), str)

        Biome.biomeList.append(cls)  # add new biome to list of biomes


class Farmland(Biome):
    primaryRes: Resource = Resource.Wheat
    color = 'goldenrod'


class Grassland(Biome):
    primaryRes: Resource = Resource.Sheepie
    color = 'limegreen'


class Forest(Biome):
    primaryRes: Resource = Resource.Lumber
    color = 'forestgreen'


class Mountain(Biome):
    primaryRes: Resource = Resource.Ore
    color = 'dimgray'


class Quarry(Biome):
    primaryRes: Resource = Resource.Brick
    color = 'firebrick'
