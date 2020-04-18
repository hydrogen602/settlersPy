'''
Action Manager module
'''

from tools import typeCheck
from typing import Dict, Callable
from abc import ABC as AbstractBaseClass
from abc import abstractmethod

class ActionIllegalException(Exception):
    '''
    Raised when the game rules do not permit a certain action from
    happening, like purchasing something that the player cannot afford.
    '''
    pass


class ActionSuperCls(AbstractBaseClass):
    '''
    This class is for implementing new actions. Each
    action needs a `isValid` method and a `doAction`
    method so that all the actions can be called from
    one place, the `ActionManager`.


    Represents a single action. Each action needs a function 
    called `isValid` that takes a `str`, playerID, and returns a `bool`
    representing whether this player is allowed to do this action or not.
    `doAction` is the function that, once called, actually carries out the
    action. It receives one argument, the playerID as `str`
    This should check, for example, whether a player has the necessary
    resources for a purchase.
    Each action is represented with a group name and an individual name,
    and are later referred to using those names.

    '''

    def __init__(self, group: str, name: str):
        self.__group = group
        self.__name = name

    @abstractmethod
    def isValid(self, playerID: str) -> bool:
        '''
        Called by `ActionManager` to verify an action is allowed
        by the Game Rules. Subclasses need to implement this method.
        '''
        ...
    
    @abstractmethod
    def doAction(self, playerID: str) -> None:
        '''
        Called by `ActionManager` to run an action once it has been
        verified to be legal according to the game rules.
        Subclasses need to implement this method.
        '''
        ...
    
    @property
    def group(self) -> str:
        return self.__group
    
    @property
    def name(self) -> str:
        return self.__name


class ActionManager:
    '''
    This module is for managing all the actions a player can trigger
    in the game in one place. Each action, like buying a road
    or placed it is represented with an instance of the `ActionManager.Action`
    class, and then added to the manager using the `addAction` method.
    Later the actions can be called with the `call` method. All
    actions have a group and their own name, like an all buying actions group
    which would have group="purchase" for example.
    '''

    class Action(ActionSuperCls):
        '''
        A class for making an action using just two functions rather than a whole subclass
        '''

        def __init__(self, isValid: Callable[[str], bool], doAction: Callable[[str], None], group: str, name: str):
            self.__isValid: Callable[[str], bool] = isValid
            self.__doAction: Callable[[str], None] = doAction
            super().__init__(group, name)
        
        def isValid(self, playerID: str) -> bool:
            '''
            Called by `ActionManager` to verify an action is allowed
            by the Game Rules. This is just a wrapper over the passed
            in `isValid` function that gives annotations.
            '''
            return self.__isValid(playerID)
        
        def doAction(self, playerID: str) -> None:
            '''
            Called by `ActionManager` to run an action once it has been
            verified to be legal according to the game rules.
            This is just a wrapper over the passed
            in `doAction` function that gives annotations.
            '''
            return self.__doAction(playerID)


    def __init__(self):
        self.actions: Dict[str, Dict[str, ActionManager.Action]] = {}
    
    def addAction(self, ac: Action) -> None:
        '''
        Add an action of type `ActionManager.Action` to the list
        of actions.
        '''
        typeCheck(ac, ActionSuperCls)

        if ac.group not in self.actions:
            self.actions[ac.group] = {} # create group if it doesn't exist

        self.actions[ac.group][ac.name] = ac
    
    def call(self, group: str, name: str, playerID: str) -> None:
        '''
        Call an action. If a player wanted to buy a road for example,
        then this method would be called as `call('purchase', 'road', 'player1')`.
        This method throws `KeyError` if either the group does not exist or an
        action of the specified name does not exist in the group.
        The method throws an `ActionIllegalException` if the game rules
        prohibit this action, i.e. `isValid()` returned false.
        '''
        if group not in self.actions:
            raise KeyError(f"No group found called '{group}' in ActionManager")
        if name not in self.actions[group]:
            raise KeyError(f"No action found called '{name}' in group '{group}' in ActionManager")
        
        ac: ActionManager.Action = self.actions[group][name]

        if not ac.isValid(playerID=playerID):
            raise ActionIllegalException(f"Action '{name}' of group '{group}' for player '{playerID}' is not allowed")

        ac.doAction(playerID=playerID)


