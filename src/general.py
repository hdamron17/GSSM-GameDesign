'''
General enums and things which may be needed across modules
'''

from enum import IntEnum, Enum, unique
from os.path import join as pathjoin, abspath, dirname, normpath
import sys


PROJECT_ROOT = normpath(pathjoin(dirname(abspath(sys.argv[0])), ".."))

@unique
class Tile(Enum):
    '''
    Type of tile in a map
    '''
    EMPTY = 1
    OCCUPIED = 2
    FW_SLASH = 3
    BK_SLASH = 4
    GENERIC_ITEM = 5
    DOOR = 6

@unique
class Direction(IntEnum):
    '''
    Direction of a gremlin to go
    '''
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
def clock(direction, rotations=1):
    '''
    Rotates it clockwise
    :param direction: direction item to be rotated
    :param rotations: number of rotations to go (negative -> counterclockwise)
    :return: returns the direction 90 degrees clockwise
    '''
    return Direction((direction - rotations) % 4)
    
@unique
class GremmType(Enum):
    '''
    Type of gremlin (in case it is needed in future versions)
    '''
    GOOD = 1
    BAD = 2