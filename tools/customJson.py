import json
from .functions import typeCheck

class customJsonEncoder(json.JSONEncoder):
    '''
    A custom encoder for this project that represents
    any class as a dict of its instance variables (obj.__dict__)
    and adds a key '__name__' whose value is the name of the class
    of that object ( type(obj).__name__ ).

    If a custom encoder is needed, a class
    can implement a toJsonSerializable() method
    that should return a dict that contains all
    necessary data
    '''

    def default(self, obj): # pylint: disable=E0202
        dictData = {}

        if hasattr(obj, 'toJsonSerializable'):
            dictData = getattr(obj, 'toJsonSerializable')()
            typeCheck(dictData, dict)
        else:
            raise TypeError(f"Type {type(obj)} is not JSON Serializable, missing method toJsonSerializable()")         
            # dictData = dict(obj.__dict__)
        
        dictData['__name__'] = type(obj).__name__
        return dictData
