'''
Graphics part of the game - converts symbolic game representation to graphics then displays that.
Also handles user input and passes filtered input to the engine
'''

import pygame

#from gremm_tunnel import PROJECT_ROOT
import gremm_tunnel
import gameboard


BOX_SIZE = 20

class GameBoard():
    '''
    Single game board with resident game pieces
    '''
    
    def __init__(self, board):
        '''
        Creates GameBoard object from a board (created by 
        '''
        pygame.init()
        self.y_size = len(board)
        self.x_size = max([len(row) for row in board])
        self.screen = pygame.display.set_mode((BOX_SIZE*self.x_size, BOX_SIZE*self.y_size))

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.screen.fill((0,255,0))
        pygame.display.flip()
        return True
    
def test():
    board = GameBoard(gameboard.board_from_text_file("tests/gameboard_test.map"))
    while board.loop(): pass

if __name__ == "__main__":
    test()