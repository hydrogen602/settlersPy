
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
        crashReport = ["Missing methods:"]
        for m in methods:
            if not hasattr(cls, m):
                success = False
                crashReport.append(f"Class '{cls.__name__}' is missing attribute '{m}'")
        
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
    pass
    foo = 0
    bar = 0
    baz = 0