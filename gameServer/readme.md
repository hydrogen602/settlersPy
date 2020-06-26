
# Organization

Notes:
 - \[D\] Directory
 - \[M\] Module (File)
 - \[C\] Class
 - \[MC\] MetaClass
 - \[F\] Function
---
## Modules & Outline
---
### Map

 - \[D\] mapCode: GameMap, map features, etc.
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
   - \[M\] baseMapFeatures:
     - \[C\] Placeable: superclass of all that can be placed on the map by a player

### Player

 - \[D\] playerCode
   - \[M\] playerManager
     - \[C\] PlayerManager
   - \[M\] player
     - \[C\] Player
   - \[M\] inventory
     - \[C\] Inventory
     - \[C\] ExpandedInventory
   - \[M\] turn
     - \[C\] Turn

### Extra Code

 - \[D\] extraCode
   - \[M\] util
     - \[F\] isNotNone
     - \[MC\] IterableCls
     - \[C\] JsonSerializable
     - \[C\] ActionError
     - \[C\] NotSetupException
   - \[M\] location
     - \[C\] Biome
     - \[C\] Resource
     - \[C\] HexPoint
   - \[M\] modifiers
     - \[C\] Placeable
     - \[C\] Ownable
     - \[C\] Purchaseable
  

---
##  On Multiple Inheritance and Arguments in `__init__`

When there is a change of multiple inheritance, `__init__`
should always use only keyword arguments and then pass
the remaining kwargs to `super().__init__`. This
seems like the best way to deal with multiple parents
that all need some argument.

---
## JsonSerializable system

As the necessary data of an object may come from
superclasses as well as the subclass,
every class that has the `toJsonSerializable`
method should inherit from `mapCode.util.JsonSerializable`.
This superclass will ensure that all subclasses have
implemented their own `toJsonSerializable` method
as well as allowing for this pattern:
```
def toJsonSerializable(self) -> Dict[str, object]:
  return {
    'position': self._pos,
    'owner': self._owner,
    **super().toJsonSerializable()
  }
```
Here the class makes a dict with its variables,
but also calls `super().toJsonSerializable()`
so that any of its parents can also add their own
variables to the dictionary.
The `JsonSerializable` class has a `toJsonSerializable`
method that returns an empty dictionary, so that
`super().toJsonSerializable()` can be called without
worrying that none of the parents have the method,
which would cause an exception. 

---
## Websocket Error Codes

4000–4999 are for applications by websocket design

I'll use 4000-4099 for errors that should sent the user back to login

- [4000] name missing
- [4001] game already started
- [4002] invalid token