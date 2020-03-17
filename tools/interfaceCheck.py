'''
Additional interface and function checking systems
'''

from typing import Union, Tuple, Dict, List
from inspect import signature


# def assertIsImplementation(obj: object, class_or_tuple: Union[type, Tuple[type]]) -> bool:
#     if isinstance(class_or_tuple):
#         needToCheck: Tuple[type] = class_or_tuple
#     else:
#         needToCheck: Tuple[type] = (class_or_tuple, )

#     for ty in needToCheck:
#         methods = dir(ty)
#         success = True
#         crashReport = ["Missing methods:"]
#         for m in methods:
#             if not hasattr(obj, m):
#                 success = False
#                 crashReport.append(f"Object '{obj.__name__}' is missing attribute '{m}'")
        
#         if not success:
#             raise AttributeError('\n'.join(crashReport))

def signatureChecker(cls: type, interface: type, attrName: str) -> None:
    '''
    Checks if an attribute of the interface is present in the class `cls`.
    Returns `None` if no issue is found, else `TypeError` or `AttributeError`
    '''
    if not hasattr(cls, attrName):
        raise AttributeError(f"Class '{cls.__name__}' is missing attribute '{attrName}'")
    a_ref = getattr(cls, attrName)
    orig_ref = getattr(interface, attrName)
    if callable(orig_ref):
        if not callable(a_ref):
            raise TypeError(f"Interface '{interface.__name__}' requires callable attribute '{attrName}' but the implementation of '{attrName}' in class '{cls.__name__}' is not callable")

        if not hasattr(orig_ref, '__code__'):
            return  # can't analyze
        
        orig_sig = signature(orig_ref)
        impl_sig = signature(a_ref)

        if orig_sig != impl_sig:
            raise TypeError(f"Signatures don't match: Expected {orig_ref.__name__}{str(orig_sig)} but got {a_ref.__name__}{str(impl_sig)}")

        #if hasattr(orig_ref, '__annotations__') and orig_ref.__annotations__ != a_ref.__annotations__:
        #    raise TypeError(f"Signatures mismatch of attribute '{a}': {reprinter(orig_ref)} <=> {reprinter(a_ref)}")
    else:
        if callable(a_ref):
            raise TypeError(f"Interface '{interface.__name__}' requires a non-callable attribute '{attrName}' but the implementation of '{attrName}' in class '{cls.__name__}' is callable")

# class A:
#     def foo(self, x: int) -> int: pass

# class B:
#     def foo(self, x: str) -> int: pass

# signatureChecker(B, A, 'foo')