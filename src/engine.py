'''
Central engine of the game - converts user inputs into game changes
'''

import warnings

import gui
import gameboard

def begin(board_file="tests/gameboard_test.map", board_type="text"):
    '''
    Begins the game with specific parameters
    '''
    if board_type == "text":
        board = gameboard.text_board_from_file(board_file)
    else:
        warnings.warn("Unsupported board_type")
        return
    
    gui.GameBoard(board)

def test():
    begin()

if __name__ == "__main__":
    test()