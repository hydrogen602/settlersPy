
organization?

Habitation -> abstract
 - pos: HexPoint
 - diceValue: int
 - neighboringTiles: List[Tile], len == 3
 - dieRolled(int) -> check if diceValue matches, then give resource
 - getPos()
    |
Settlement
    |
  City

Player

Robber
 - tile loc: HexPoint

Tile
 - pos: HexPoint
 - resource: (ResourceType)
 - isBlockedByRobber: (bool)

ResourceType extends enum

Point -> abstract
 - getHexPoint
 // if no conversion is needed, return copy of self


## Design Ideas

JSON validation should happen in server.py
GameManager shouldn't be handling socket problems

