'''
Generates and converts gameboard types
'''

from os.path import join as pathjoin
import string

from general import Tile, Direction, PROJECT_ROOT
from collections import OrderedDict


text_mapping = {
    ' ' + string.ascii_lowercase : Tile.EMPTY,
    '#' + string.ascii_uppercase : Tile.OCCUPIED,
    '/' : Tile.FW_SLASH,
    '\\' : Tile.BK_SLASH,
    '*' : Tile.GENERIC_ITEM,
    ':' : Tile.DOOR,
}

direction_mapping = {
    'N' : Direction.UP,
    'E' : Direction.RIGHT,
    'S' : Direction.DOWN,
    'W' : Direction.LEFT,
}

class BoardLayout():
    def __init__(self, filename):
        self.maps = {}
        self.layout = OrderedDict()
        self.start = None
        
        with open(pathjoin(PROJECT_ROOT, "assets", filename), "r") as fp:
            for line in fp:
                stripped = line.lstrip()
                if len(stripped) > 0:
                    key, value = [item.strip() for item in stripped.split(" ", 1)]
                    if line == stripped:
                        #no whitespace on side
                        assert key != "END", "END is not a valid map key"
                        self.maps[key] = board_from_text_file(value)
                        self.layout[key] = {}
                        
                        if self.start is None:
                            self.start = self.maps[key]
                            
                    elif len(self.layout) > 0:
                        #append direction to layout
                        direction = direction_mapping[key]
                        last_key = list(self.layout.keys())[-1]
                        self.layout[last_key][direction] = value if value != "END" else None
        
        for mapping in self.layout.values():
            for value in mapping.values():
                assert value is None or value in self.maps.keys(), "Invalid mapping %s" % (value)
                
    def __str__(self):
        return "maps: " + str(self.maps.keys()) + "\nlayout: " + str(dict(self.layout))
    
    def next_map(self, map_name, direction):
        return self.layout[map_name].get(direction) or self.start
    
    def get_start(self):
        return self.start
    
    #TODO all of the stuff for board layout

def text_board_from_file(filename):
    '''
    Creates text board based on text file
    :param filename: relative filename in assets directory for image to use
    :return: returns a 2D gameboard with text characters
    '''
    absolute_name = pathjoin(PROJECT_ROOT, "assets", filename)
    board = []
    with open(absolute_name) as fp:
        for line in fp:
            board.append([char for char in line if char != "\n"])
    return board

def char_to_enum(char):
    '''
    Converts a single character to enum value
    '''
    for key in text_mapping.keys():
        if char in key:
            return text_mapping[key]
    return None

def text_board_to_enum(text_board):
    '''
    Converts text board (2D array of chars) to board using general
    :param text_board: 2D array of chars as shown in assets/tests/gameboard_test.map
    :return: returns 2D array using numbers as shown in BOARD_ENUM
    '''
    board = []
    for row in text_board:
        board.append([char_to_enum(char) for char in row])
    return board

def board_from_text_file(filename):
    return text_board_to_enum(text_board_from_file(filename))

def test():
    [print(row) for row in text_board_to_enum(text_board_from_file("tests/gameboard_test.map"))]
    layout = BoardLayout("tests/overboard_test.layout")
    print(layout)

if __name__ == "__main__":
    test()