class Tile:

    def __init__(self, biome, diceValue: int):
        self.biome = biome
        #checks that the dice value is an instance of an Int 
        assert isinstance(diceValue, int)
        #checks that the diceValue is between 2-12
        assert diceValue >= 2 and diceValue <= 12
        self.diceValue = diceValue 
        self.settlementList = []
        
    def diceRolled (self, valueRolled):
        if valueRolled == self.diceValue:
            for s in self.settlementList: 
                s.giveResource(self.biome)
        

