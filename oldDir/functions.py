
def typeCheck(value: object, type_: type):
    '''
    Raises a `TypeError` if value is not of the given type
    '''
    if not isinstance(value, type_):
        raise TypeError(f'Expected type {type_} but got {type(value)}')

def subclassCheck(subCls: type, superCls: type):
    if not issubclass(subCls, superCls):
        raise TypeError(f'Expected subclass of {superCls.__name__}, but {subCls.__name__} is not')

def requireNotNone(obj: object):
    if obj is None:
        raise TypeError(f'Object may not be None')

