'''
The tools module is for enforcing interfaces on classes
and verifying that functions expect the right arguments and types

Also has a custom json encoder for objects
'''

from .interface2 import InterfaceSuperType, interface
from .functions import typeCheck, subclassCheck
from .customJson import customJsonEncoder

if __name__ == '__main__':
    raise ImportError
if __name__ != 'tools':
    raise ImportError("What? __name__ = " + __name__)