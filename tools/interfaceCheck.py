from typing import Union, Tuple, Dict, List
from inspect import getargs, signature

def assertIsImplementation(obj: object, class_or_tuple: Union[type, Tuple[type]]) -> bool:
    if isinstance(class_or_tuple):
        needToCheck: Tuple[type] = class_or_tuple
    else:
        needToCheck: Tuple[type] = (class_or_tuple, )

    for ty in needToCheck:
        methods = dir(ty)
        success = True
        crashReport = ["Missing methods:"]
        for m in methods:
            if not hasattr(obj, m):
                success = False
                crashReport.append(f"Object '{obj.__name__}' is missing attribute '{m}'")
        
        if not success:
            raise AttributeError('\n'.join(crashReport))

class Signature:

    def __init__(self, func):
        self.name = func.__name__

        self.__s = signature(func)

        argNames = list(self.__s.parameters)

        self.args = args
        self.varArgs = varArgs
        self.varKeywords = varKeywords
        self.returnType = returnType
    
    def __str__(self):
        return self.name + str(self.__s)

def signatureCheck(cls: type, interface: type):
    def reprinter(func) -> str:
        anno = func.__annotations__
        re = anno.get('return')
        args = ', '.join([anno[k].__name__ for k in anno if k != 'return'])
        if re:
            return f'{func.__name__}({args}) -> {re.__name__}'
        else:
            return f'{func.__name__}({args}) -> object'
    
    def signatureAssembler(func) -> List[Tuple[str, object]]:
        # make signature
        args, varArgs, varKeywords = getargs(func.__code__)

        sig = [] # list to preserve order of args

        def addWithAnnotationIfExists(name, default=object):
            if name in func.__annotations__:
                sig.append((name, func.__annotations__[name]))
            else:
                sig.append((name, default))

        for a in args:
            addWithAnnotationIfExists(a)
        
        if varArgs:
            addWithAnnotationIfExists(varArgs, default=Tuple[object])
        
        if varKeywords:
            addWithAnnotationIfExists(varKeywords, default=Dict[object, object])
        
        return sig

    attrs = dir(interface)
    for a in attrs:
        if not hasattr(cls, a):
            raise AttributeError(f"Class '{cls.__name__}' is missing attribute '{a}'")
        a_ref = getattr(cls, a)
        orig_ref = getattr(interface, a)
        if callable(orig_ref):
            if not callable(a_ref):
                raise TypeError(f"Interface '{interface.__name__}' requires callable attribute '{a}' but the implementation of '{a}' in class '{cls.__name__}' is not callable")

            if not hasattr(orig_ref, '__code__'):
                continue  # can't analyze
            
            orig_sig = signatureAssembler(orig_ref)

            impl_sig = signatureAssembler(a_ref)

            for orig_arg, impl_arg in zip(orig_sig, impl_sig):
                print(orig_arg, impl_arg)
                if orig_arg != impl_arg:
                    
                    raise TypeError(f"Signatures don't match: Expected {signatureToStr(orig_ref, orig_sig)} but got {signatureToStr(orig_ref, impl_sig)}")
        


            #if hasattr(orig_ref, '__annotations__') and orig_ref.__annotations__ != a_ref.__annotations__:
            #    raise TypeError(f"Signatures mismatch of attribute '{a}': {reprinter(orig_ref)} <=> {reprinter(a_ref)}")
        else:
            if callable(a_ref):
                raise TypeError(f"Interface '{interface.__name__}' requires a non-callable attribute '{a}' but the implementation of '{a}' in class '{cls.__name__}' is callable")

class A:
    def foo() -> int: pass

class B:
    def foo(): pass

signatureCheck(B, A)