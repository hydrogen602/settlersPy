
def typeCheck(value: object, type_: type):
    '''
    Raises a `TypeError` if value is not of the given type
    '''
    if not isinstance(value, type_):
        raise TypeError(f'Expected type {type_} but got {type(value)}')

def subclassCheck(subCls: type, superCls: type):
    if not issubclass(subCls, superCls):
        raise TypeError(f'Expected subclass of {superCls.__name__}, but {subCls.__name__} is not')

# def enforceType(func):
#     assert callable(func)
#     assert hasattr(func, '__annotations__')

#     if 'return' not in func.__annotations__:
#         raise AttributeError(f'Function {func.__name__} is missing a return type annotation')

#     def wrapper(*args, **kwargs):

#         pass

#     return wrapper
    

# def foo(x: int) -> None:
#     pass

# enforceType(foo)
