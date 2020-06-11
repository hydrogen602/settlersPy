from typing import Dict


def isNotNone(methodName: str, **kwargs):
    '''
    Verifies that each keyword argument given is not null.
    '''
    for key in kwargs:
        assert isinstance(key, str)
        if kwargs[key] is None:
            raise TypeError(f"{methodName}() missing required argument: '{key}'")


class IterableCls(type):
    def __init__(cls, name, bases, dct) -> None:
        if not hasattr(cls, 'getIterable'):
            raise TypeError(f'IterableCls {name} must have method getIterable')

    def __iter__(cls):
        return iter(cls.getIterable())
    
    def __getitem__(cls, key):
        return cls.getIterable()[key]


class JsonSerializable:
    '''
    A superclass for classes that have a
    `toJsonSerializable` method but may
    also be part of multiple inheritance.
    Requires subclasses to override the 
    `toJsonSerializable` method.
    In the list of classes that a cls is inheriting
    from, put JsonSerializable last for best results.
    (aka it might crash otherwise but i'm not sure)
    '''

    def __init_subclass__(cls):
        func = getattr(cls, 'toJsonSerializable')
        if func is JsonSerializable.toJsonSerializable:
            # didn't implement their own method
            raise TypeError(f"{cls.__name__} did not implement its own 'toJsonSerializable' method")
    
    def toJsonSerializable(self) -> Dict[str, object]:
        return {}


class ActionError(Exception):
    # TODO: move to a util package
    '''
    For when some action isn't allowed by
    game rules, like buying something
    the player can't afford or placing
    something where it is not allowed to
    be placed
    '''
    pass


class NotSetupException(Exception):
    # TODO: move to a util package
    '''
    For when something cannot be used yet
    because some setup action hasn't happened yet
    '''
    pass
