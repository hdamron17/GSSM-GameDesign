'''
Generates and converts gameboard types
'''

from os.path import join as pathjoin
import string

from general import Tile, Direction, PROJECT_ROOT
from collections import OrderedDict


#Which text character maps to which Tile enum in map file
text_mapping = {
    ' ' + string.ascii_lowercase : Tile.EMPTY,
    '#' + string.ascii_uppercase : Tile.OCCUPIED,
    '/' : Tile.FW_SLASH,
    '\\' : Tile.BK_SLASH,
    '*' : Tile.GENERIC_ITEM,
    ':' : Tile.DOOR,
}

#which letter maps to which direction in layout file
direction_mapping = {
    'N' : Direction.UP,
    'E' : Direction.RIGHT,
    'S' : Direction.DOWN,
    'W' : Direction.LEFT,
}

class BoardLayout():
    '''
    Reads from .layout file and controls flow between rooms
    '''
    
    def __init__(self, filename):
        '''
        Reads .layout file from assets folder and constructs BoardLayout object
        '''
        self.maps = {}
        self.colors = {}
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
                        filename, color_str = value.split(" ", 1)
                        self.maps[key] = board_from_text_file(filename)
                        self.colors[key] = [int(c) for c in color_str.split(",", 2)]
                        self.layout[key] = {}
                        
                        if self.start is None:
                            self.start = (key, self.maps[key])
                            
                    elif len(self.layout) > 0:
                        #append direction to layout
                        direction = direction_mapping[key]
                        last_key = list(self.layout.keys())[-1]
                        self.layout[last_key][direction] = value if value != "END" else "END"
        
        for mapping in self.layout.values():
            for value in mapping.values():
                assert value == "END" or value in self.maps.keys(), "Invalid mapping %s" % (value)
                
    def __str__(self):
        '''
        toString()
        '''
        return "maps: " + str(self.maps.keys()) + "\nlayout: " + str(dict(self.layout))
    
    def next_map(self, map_name, direction):
        '''
        Gets the next map from the dictionary
        :param map_name: name of current map
        :param direction: direction to go from current map
        :return: returns another map or None if the current map is the end
            in the format (map name, map 2D array, direction)
            if there is no mapping returns starting map
        '''
        next_map_name = self.layout[map_name].get(direction)
        if next_map_name is None:
            return self.start + (Direction.UP,)
        elif next_map_name == "END":
            return None
        else:
            return next_map_name, self.maps[next_map_name], direction
    
    def get_start(self):
        '''
        Gets starting map in form (map name, map 2D array)
        '''
        return self.start
    
    def color(self, map_name):
        '''
        Gets the color of a map
        :param map_name: name of map to get
        :return: returns integer 3-tuple for color
        '''
        return self.colors.get(map_name)
    
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
    '''
    Combinatory function gets board from text file as the name suggests
    :param filename: name of file to read
    :return: returns 2D array of Tile enums representing board
    '''
    return text_board_to_enum(text_board_from_file(filename))

def test():
    '''
    Test function does a simple map and prints stuff about it
    '''
    [print(row) for row in text_board_to_enum(text_board_from_file("gbd1/start.map"))]
    layout = BoardLayout("gbd1/gbd1.layout")
    print(layout)
    print(layout.get_start())
    print(layout.next_map('learner', Direction.RIGHT))

if __name__ == "__main__":
    test()