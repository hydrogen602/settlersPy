
# Organization

Notes:
 - \[F\] Folder
 - \[M\] Module (File)
 - \[C\] Class
---
## Modules & Outline
---
### Map

 - \[F\] mapCode: GameMap, map features, etc.
   - \[M\] util
     - \[C\] HexPoint
     - \[C\] Biome
   - \[M\] gameMap
     - \[C\] GameMap: Holds reference to all things on the map
   - \[M\] pointMapFeatures
     - \[C\] Settlement: A town on the map
     - \[C\] City(Settlement): A city, subclass of settlement
   - \[M\] tiles
     - \[C\] Tile: The board tiles
   - \[M\] lineMapFeatures
     - \[C\] Road

### Player

 - \[F\] playerCode
   - \[M\] playerManager
     - \[C\] PlayerManager
   - \[M\] player
     - \[C\] Player
   - \[M\] inventory
     - \[C\] Inventory
 