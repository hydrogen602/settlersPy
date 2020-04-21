import pytest

import os
import sys

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

# print(__file__)
# print(newPath)

# print(sys.path)

import mechanics.event as event

def testFaultySubCls():

    with pytest.raises(AttributeError):
        class FaultyNoName(event.Event):
            pass
    
    with pytest.raises(TypeError):
        class FaultyWrongNameType(event.Event):
            typeName = 42
    
    with pytest.raises(AttributeError):
        class FaultyNoFromJson(event.Event):
            typeName = "faulty"
    
    with pytest.raises(event.EventParseError):
        class FaultyTakenName(event.Event):
            typeName = "action"
            def fromJson(self, data):
                pass

def testReturn():

    with pytest.raises(KeyError):
        event.Event.fromJson({})
    
    with pytest.raises(KeyError):
        event.Event.fromJson({'type': 'noExist1234567890'})

    