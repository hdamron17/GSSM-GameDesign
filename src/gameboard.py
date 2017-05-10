'''
Generates and converts gameboard types
'''

from os.path import join as pathjoin
import string

from general import Tile, PROJECT_ROOT


text_mapping = {
    ' ' + string.ascii_lowercase : Tile.EMPTY,
    '#' + string.ascii_uppercase : Tile.OCCUPIED,
    '/' : Tile.FW_SLASH,
    '\\' : Tile.BK_SLASH,
    '*' : Tile.GENERIC_ITEM,
    ':' : Tile.DOOR,
}

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

if __name__ == "__main__":
    test()