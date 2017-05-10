'''
Created on May 10, 2017

@author: hdamron1594
'''

from enum import Enum, unique
from os.path import join as pathjoin, abspath, dirname, normpath
import sys


PROJECT_ROOT = normpath(pathjoin(dirname(abspath(sys.argv[0])), ".."))

@unique
class Tile(Enum):
    EMPTY = 1
    OCCUPIED = 2
    FW_SLASH = 3
    BK_SLASH = 4
    GENERIC_ITEM = 5
    DOOR = 6

@unique
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
@unique
class GremmType(Enum):
    GOOD = 1
    BAD = 2