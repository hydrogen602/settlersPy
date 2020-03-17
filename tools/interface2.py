
from .interfaceCheck import signatureChecker

class InterfaceSuperType:
    '''
    A super class for interfaces. It is not required for the
    interface system to work, but prevents the accidental instantiantion
    of interfaces and is useful in indicating that a class is an interface.
    To use, extend this class
    '''
    def __new__(cls, *args, **kwargs):
        '''
        Raises an exception when an instantiantion of a interface is attempted
        '''
        raise TypeError("Interface can't be instantiated")

def interface(interfaceCls: type):
    '''
    Interface decorator for checking that the class has the attribute that
    the interface requires. InterfaceCls should be the interface, and cls
    the concrete class that implements the interface. Technically any class
    can be an interface for this method.
    How to use:
    @interface(someInterface)
    class ConcreteClass:
        pass
    '''
    def checker(cls: type):
        '''
        This function does the actual verification of required attributes
        '''
        methods = dir(interfaceCls) # [i for i in dir(interfaceCls) if not i.startswith('__')]
        success = True
        crashReport = ["Incorrect methods:"]
        for m in methods:
            if m in [
                '__class__', '__delattr__', 
                '__dir__', '__doc__', 
                '__eq__', '__format__',
                '__getattribute__', '__hash__',
                '__ne__', '__new__', 
                '__reduce__', '__reduce_ex__', 
                '__repr__', '__setattr__', 
                '__sizeof__', '__str__', 
                '__subclasshook__'
                ]:
                continue
            try:
                signatureChecker(cls, interfaceCls, m)
            except AttributeError as e:
                success = False
                crashReport.append(e.args[0])
            except TypeError as e:
                success = False
                crashReport.append(e.args[0])

        if not success:
            raise AttributeError('\n'.join(crashReport))
        return cls
    return checker

class InterfaceClass(InterfaceSuperType):
    '''
    Example interface
    Interfaces functions shouldn't have
    a body but that is not enforced
    '''
    def foo(self): pass
    def bar(self): pass
    def baz(self): pass

@interface(InterfaceClass)
class ConcreteClass:
    '''
    Example implementation of an interface
    '''
    def foo(self): pass
    def bar(self): pass
    def baz(self): pass