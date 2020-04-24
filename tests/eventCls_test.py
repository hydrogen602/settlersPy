import pytest

import os
import sys

newPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(newPath)

# print(__file__)
# print(newPath)

# print(sys.path)

@pytest.mark.incremental
class TestFaultySubClsExceptions:
    def testImporting(self):
        import mechanics.event as event

    def testFaultySubCls1(self):
        import mechanics.event as event

        with pytest.raises(AttributeError):
            class FaultyNoName(event.Event):
                pass

    def testFaultySubCls2(self):
        import mechanics.event as event

        with pytest.raises(TypeError):
            class FaultyWrongNameType(event.Event):
                typeName = 42

    def testFaultySubCls3(self):
        import mechanics.event as event

        with pytest.raises(AttributeError):
            @event.eventSystemSetup('typeName_testFaultySubCls3', buildFromJsonMethod=False)
            class FaultyNoFromJson(event.Event):
                typeName = "faulty"
            print(FaultyNoFromJson.fromJson)

    def testFaultySubCls4(self):
        import mechanics.event as event

        with pytest.raises(event.EventParseError):
            class FaultyTakenName(event.Event):
                typeName = "action"
                def fromJson(self, data):
                    pass

    def testReturn(self):
        import mechanics.event as event

        with pytest.raises(KeyError):
            event.Event.fromJson({})
        
        with pytest.raises(KeyError):
            event.Event.fromJson({'type': 'noExist1234567890'})

@pytest.mark.incremental
class TestParsingSubCls:
    def testImporting(self):
        import mechanics.event as event

    def testSubClass(self):
        import mechanics.event as event

        @event.eventSystemSetup('actionTest', buildFromJsonMethod=True)
        class BasicSubCls(event.Event):
            typeName = 'testType_testSubClass'
    
    def testSubClass2(self):
        import mechanics.event as event

        global called
        called = False

        @event.eventSystemSetup('basicSubCls', buildFromJsonMethod=True)
        class BasicSubCls(event.Event):
            typeName = 'testType_testSubClass2'
        
        @event.eventSystemSetup('actionSubCls', buildFromJsonMethod=False)
        class ActionSubCls(BasicSubCls):
            basicSubCls = 'actionName'
        
            @classmethod
            def fromJson(cls, data):
                global called
                called = True
                return ''
        
        event.Event.fromJson({'typeName': 'testType_testSubClass2', 'basicSubCls': 'actionName'})

        assert called


@pytest.mark.incremental
class TestFeatureClasses:
    def testImporting(self):
        import mechanics.event as event
        import features.purchaseAction as purchaseModule
    
    def testModule(self):
        import mechanics.event as event
        import features.purchaseAction as purchaseModule

        cls = purchaseModule.PurchaseAction
