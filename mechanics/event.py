'''
The event system is to turn received json messages into
an understandable and known structure and verifying
that all necessary tags are there.
'''

from typing import Dict, Union
from functools import wraps

from tools import typeCheck

def eventSystemSetup(varName: str, buildFromJsonMethod: bool):
    '''
    Decorator for the `Event` class or one
    of its subclasses.
    Gives the wrapped class a `__init_subclass__` method
    and a variable called `__subClsList`

    If `buildFromJsonMethod` is True, then the decorator will
    also build a default implementation of fromJson
    with argument `varName` as the key to look
    for in the json.
    This overwrites the class's `fromJson` function.
    '''
    def decorator_func(cls: type):

        @classmethod
        def __init_subclass__(subCls):
            '''
            Verifies a subCls has the right attributes
            and adds the subCls to the list of subClasses
            for later reference
            '''
            if not hasattr(subCls, varName):
                raise AttributeError(f"Missing attribute '{varName}'")

            x: str = getattr(subCls, varName)
            typeCheck(x, str)

            if not hasattr(subCls, 'fromJson'):
                raise AttributeError("Missing method 'fromJson'")

            # clsList = subCls.mro()[1:] # first is itself so ignore that

            # for cls in clsList:
            #     if cls.__name__ == clsName:
            #         break

            if cls.fromJson is getattr(subCls, 'fromJson'):
                raise AttributeError(f"{cls.__name__} subclass must overwrite 'fromJson', but has not")

            subClsList = getattr(cls, f'_{cls.__name__}__subClsList')

            if x in subClsList:
                raise EventParseError(f"{cls.__name__} {varName}='{x}' already exists")

            print(f"Registering {varName} '{x}' in class '{cls.__name__}'")
            subClsList[x] = subCls
        

        def fromJson(cls, data: Dict[str, Union[str, dict]]):
            '''
            A fromJson default function

            Takes a `dict` that represents a received Json message
            and finds the appropriate subclass to further verify
            and parse the message
            Throws a `KeyError` if there is no 'type' key or
            if the specified type does not have a subclass for it 
            '''

            typeCheck(data, dict)
            if varName not in data:
                raise KeyError(f"Missing key '{varName}': {data}")

            varValue = data[varName]
            if varValue not in cls.__subClsList:
                raise KeyError(f"No subclass found for event {varName} '{varValue}'")

            subCls = cls.__subClsList[varValue]

            return subCls.fromJson(data)

        if buildFromJsonMethod:
            print(f"Build `fromJson` for class '{cls.__name__}'")
            cls.fromJson = fromJson.__get__(cls, type(cls))

        cls.__init_subclass__ = __init_subclass__
        setattr(cls, f'_{cls.__name__}__subClsList', {})
        '''
        A `dict` of all subclasses of the Event class.
        This is useful for parsing json
        as the type name determines what is should expect.

        Every received json must have a key called type whose
        value matches one of the subclasses of `Event`

        The var is of type Dict[str, type]
        '''
        return cls

    return decorator_func


class EventParseError(Exception):
    pass

@eventSystemSetup('typeName', buildFromJsonMethod=True)
class Event:
    '''
    Subclasses needs a class variable
    called `typeName` that is of type `str`
    and a method called `fromJson`
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
        

@eventSystemSetup('groupName', buildFromJsonMethod=False)
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

    def __init__(self, group: str):
        self.__group: str = group
        super().__init__(ActionEvent.typeName)
    
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


@eventSystemSetup('name', buildFromJsonMethod=False)
class PurchaseAction(ActionEvent):

    groupName = 'purchase'

    __subClsList: Dict[str, type] = {}

    def __init__(self, name: str):
        self.__name: str = name
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

        