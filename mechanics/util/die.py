import random

def rollDice() -> int:
    return random.randint(1,6)

def roll2Die() -> int:
    return random.randint(1,6) + random.randint(1,6)
