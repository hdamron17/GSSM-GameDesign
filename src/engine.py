'''
Central engine of the game - converts user inputs into game changes
'''

import warnings
import pygame

import gui
from gameboard import board_from_text_file
from general import Tile


class Engine():
    def __init__(self, board_file="tests/gameboard_test.map", board_type="text"):
        '''
        Begins the game with specific parameters
        '''
        if board_type == "text":
            self.board = board_from_text_file(board_file)
        else:
            warnings.warn("Unsupported board_type")
            return
        
        self.display = gui.GameBoard(self.board)
        
        done = False
        while not done:
            for event in self.display.loop():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move()
                    if event.key == pygame.K_LEFT:
                        self.rotate(1)
                    if event.key == pygame.K_RIGHT:
                        self.rotate(-1)
    
    def first_gremlin(self):
        '''
        Finds the first gremlin in a map based on the door patterns
        :return: returns a list of one gremlin ((x,y),direction,type)
        '''
        last_row = len(self.board) - 1
        for i in range(len(self.board[last_row])):
            if self.board[-1][i] == Tile.DOOR:
                return [((last_row, i), Direction.UP, (1))]
    
    def move(self):
        '''
        Moves gremlins straight
        '''
        print("Forward") #TODO remove
        pass #TODO
    
    def rotate(self, direction):
        '''
        Rotates the gremlins 90 degrees
        :param direction: if positive or zero, rotates counter clockwise; clockwise else
        '''
        print("Turning %s" % ("left" if direction >= 0 else "right")) #TODO remove
        pass #TODO
    
    def collision(self):
        pass #TODO
    
def begin():
    Engine()

if __name__ == "__main__":
    begin()