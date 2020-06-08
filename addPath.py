
import os
p = os.path.dirname(__file__)
p = os.path.realpath(os.path.join(os.path.abspath(p), '..'))
from sys import path
if p not in path:
    path.append(p)
