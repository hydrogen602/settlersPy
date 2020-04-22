import pytest

import os
import sys

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

# print(__file__)
# print(newPath)

# print(sys.path)

def testImporting():
    import mechanics.event as event

def testFaultySubCls1():
    import mechanics.event as event

    with pytest.raises(AttributeError):
        class FaultyNoName(event.Event):
           pass

def testFaultySubCls2():
    import mechanics.event as event

    with pytest.raises(TypeError):
        class FaultyWrongNameType(event.Event):
            typeName = 42

def testFaultySubCls3():
    import mechanics.event as event

    with pytest.raises(AttributeError):
        class FaultyNoFromJson(event.Event):
            typeName = "faulty"

def testFaultySubCls4():
    import mechanics.event as event

    with pytest.raises(event.EventParseError):
        class FaultyTakenName(event.Event):
            typeName = "action"
            def fromJson(self, data):
                pass

def testReturn():
    import mechanics.event as event

    with pytest.raises(KeyError):
        event.Event.fromJson({})
    
    with pytest.raises(KeyError):
        event.Event.fromJson({'type': 'noExist1234567890'})

    