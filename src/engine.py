'''
Central engine of the game - converts user inputs into game changes
'''

import warnings

import gui
import gameboard


class Engine():
    def __init__(self, board_file="tests/gameboard_test.map", board_type="text"):
        '''
        Begins the game with specific parameters
        '''
        if board_type == "text":
            self.board = gameboard.board_from_text_file(board_file)
        else:
            warnings.warn("Unsupported board_type")
            return
        
        self.display = gui.GameBoard(self.board)
        
        done = False
        while not done:
            self.display.loop()
            pass
    
    def loop(self):
        pass

def begin():
    Engine()

if __name__ == "__main__":
    begin()