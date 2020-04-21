
from typing import Dict, Union
from tools import typeCheck

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
    
    def __init_subclass__(cls):
        if not hasattr(cls, 'typeName'):
            raise AttributeError("Missing attribute 'typeName'")

        typeName: str = getattr(cls, 'typeName')
        typeCheck(typeName, str)

        if not hasattr(cls, 'fromJson'):
            raise AttributeError("Missing method 'fromJson'")
        if Event.fromJson is getattr(cls, 'fromJson'):
            raise AttributeError(f"Event subclass must overwrite 'fromJson', but has not")

        if typeName in Event.__subClsList:
            raise EventParseError(f"Event type '{typeName}' already exists")

        Event.__subClsList[typeName] = cls
    
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
    '''

    typeName = 'action'

    def __init__(self, group: str, name: str, data: Dict[str, str]):
        self.__group: str = group
        self.__name: str = name
        super().__init__('action')
    
    @property
    def group(self) -> str:
        return self.__group
    
    @property
    def name(self) -> str:
        return self.__name
    
    @staticmethod
    def fromJson(data):
        raise NotImplementedError