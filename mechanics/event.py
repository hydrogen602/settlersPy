'''
The event system is to turn received json messages into
an understandable and known structure and verifying
that all necessary tags are there.
'''

from typing import Dict, Union
from functools import wraps

from tools import typeCheck


def init_subclass_event(clsName: str, varName: str):

    def decorator_func(func):
        @wraps(func)
        def wrapper_func(subCls):
            if not hasattr(subCls, varName):
                raise AttributeError(f"Missing attribute '{varName}'")

            x: str = getattr(subCls, varName)
            typeCheck(x, str)

            if not hasattr(subCls, 'fromJson'):
                raise AttributeError("Missing method 'fromJson'")

            clsList = subCls.mro()[1:] # first is itself so ignore that

            for cls in clsList:
                if cls.__name__ == clsName:
                    break

            if cls.fromJson is getattr(subCls, 'fromJson'):
                raise AttributeError(f"{cls.__name__} subclass must overwrite 'fromJson', but has not")

            subClsList = getattr(cls, f'_{cls.__name__}__subClsList')

            if x in subClsList:
                raise EventParseError(f"{cls.__name__} {varName}='{x}' already exists")

            print(f"Registering {varName} '{x}' in class '{cls.__name__}'")
            subClsList[x] = subCls

        return wrapper_func

    return decorator_func


class EventParseError(Exception):
    pass

class Event:
    '''
    Subclasses needs a class variable
    called `typeName` that is of type `str`
    and a method called `fromJson`
    '''

    __subClsList: Dict[str, type] = {}
    '''
    A `dict` of all subclasses of the Event class.
    This is useful for parsing json
    as the type name determines what is should expect.

    Every received json must have a key called type whose
    value matches one of the subclasses of `Event`
    '''

    def __init__(self, type_: str):
        '''
        Don't call this method directly.
        It should only be called by a subclass
        '''
        self.__type: str = type_
    
    @property
    def eventType(self) -> str:
        return self.__type
    
    @init_subclass_event('Event', 'typeName')
    def __init_subclass__(cls):
        pass
    
    @staticmethod
    def fromJson(data: Dict[str, Union[str, dict]]):
        '''
        Takes a `dict` that represents a received Json message
        and finds the appropriate subclass to further verify
        and parse the message
        Throws a `KeyError` if there is no 'type' key or
        if the specified type does not have a subclass for it 
        '''
        typeCheck(data, dict)
        if 'type' not in data:
            raise KeyError(f"Missing key 'type': {data}")

        typeName = data['type']
        if typeName not in Event.__subClsList:
            raise KeyError(f"No subclass found for event type '{typeName}'")

        subCls = Event.__subClsList[typeName]

        return subCls.fromJson(data)
        

class ActionEvent(Event):
    '''
    Represents an action event. This convers anything done
    by the player with the board like a purchase of a road
    or the placement of a town.
    Subclasses of this class must have an attribute
    called `groupName` that must be of type `str`
    and a `fromJson` method
    '''

    typeName = 'action'

    __subClsList: Dict[str, type] = {}

    def __init__(self, group: str):
        self.__group: str = group
        super().__init__(ActionEvent.typeName)
    
    def __init_subclass__(cls):
        if not hasattr(cls, 'groupName'):
            raise AttributeError("Missing attribute 'groupName'")

        groupName: str = getattr(cls, 'groupName')
        typeCheck(groupName, str)

        if not hasattr(cls, 'fromJson'):
            raise AttributeError("Missing method 'fromJson'")
        if ActionEvent.fromJson is getattr(cls, 'fromJson'):
            raise AttributeError(f"ActionEvent subclass must overwrite 'fromJson', but has not")

        if groupName in ActionEvent.__subClsList:
            raise EventParseError(f"ActionEvent group '{groupName}' already exists")

        ActionEvent.__subClsList[groupName] = cls
        #super().__init_subclass__()
    
    @property
    def group(self) -> str:
        return self.__group
    
    @staticmethod
    def fromJson(data: Dict[str, Union[str, dict]]):
        typeCheck(data, dict)

        if 'group' not in data:
            raise KeyError("Missing key 'group'")

        groupName = data['group']
        if groupName not in ActionEvent.__subClsList:
            raise KeyError(f"No subclass found for event group '{groupName}'")

        subCls = ActionEvent.__subClsList[groupName]

        return subCls.fromJson(data)


class PurchaseAction(ActionEvent):

    groupName = 'purchase'

    __subClsList: Dict[str, type] = {}

    def __init__(self, name: str, data: dict):
        self.__name: str = name
        self.__data: dict = data
        super().__init__(PurchaseAction.groupName)
    
    @property
    def name(self) -> str:
        return self.__name
    
    @staticmethod
    def fromJson(data: Dict[str, Union[str, dict]]):
        typeCheck(data, dict)

        if 'name' not in data:
            raise KeyError("Missing key 'name'")

        name = data['name']
        if name not in PurchaseAction.__subClsList:
            raise KeyError(f"No subclass found for event name '{name}'")

        subCls = ActionEvent.__subClsList[name]

        return subCls.fromJson(data)

        