
def typeCheck(value: object, type_: type):
    if not isinstance(value, type_):
        raise TypeError(f'Expected type {type} but got {type(value)}')

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
