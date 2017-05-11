'''
Central engine of the game - converts user inputs into game changes
'''

import warnings
from pygame import QUIT, KEYDOWN, K_UP, K_LEFT, K_RIGHT

from gui import GameBoard
from gameboard import board_from_text_file
from general import Tile, GremmType, Direction, clock


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
        
        self.max_y = len(self.board)
        self.max_x = max([len(row) for row in self.board])
        print(self.max_x, self.max_y) #TODO remove
        
        self.gremlins = self.first_gremlin()
        self.display = GameBoard(self.board, self.gremlins)
        
        done = False
        while not done:
            for event in self.display.loop():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.move()
                    if event.key == K_LEFT:
                        self.rotate(1)
                    if event.key == K_RIGHT:
                        self.rotate(-1)
    
    def first_gremlin(self):
        '''
        Finds the first gremlin in a map based on the door patterns
        :return: returns a list of one gremlin ((x,y),direction,type)
        '''
        last_row = len(self.board) - 1
        for i in range(len(self.board[last_row])):
            if self.board[-1][i] == Tile.DOOR:
                return [((i, last_row), Direction.UP, GremmType.GOOD)]
        print("Error: no door on bottom row")
        return []
    
    def move(self):
        '''
        Moves gremlins straight
        '''
        new_gremlins = []
        for gremlin in self.gremlins:
            new_gremlins.extend(self.forward(gremlin))
        self.gremlins = new_gremlins
        self.display.update_gremlins(self.gremlins)
    
    def forward(self, gremlin):
        '''
        Moves the gremlin forward in the map, while also applying any subsequent actions
        :param gremlin: gremlin tuple to move forward
        :return: returns the gremlin moved to a new place
        '''
        direction = gremlin[1]
        
        dx, dy = (0, 0)
        if direction is Direction.UP: dx, dy = (0, -1)
        elif direction is Direction.RIGHT: dx, dy = (1, 0)
        elif direction is Direction.DOWN: dx, dy = (0, 1)
        elif direction is Direction.LEFT: dx, dy = (-1, 0)
        loc = x,y = gremlin[0]
        
        new_loc = new_x, new_y = (x+dx, y+dy)
        
        if (0 > new_x >= self.max_x) or (0 > new_y >= self.max_y):
            return [(loc, clock(direction, 2), gremlin[2])]
            
        next_tile = self.board[new_y][new_x]
        if next_tile is Tile.OCCUPIED:
            return [(loc, clock(direction, 2), gremlin[2])]
#         elif next_tile is Tile.BK_SLASH:
#             pass #TODO
        else: 
            return [(new_loc, direction, gremlin[2])]
    
    def rotate(self, direction):
        '''
        Rotates the gremlins 90 degrees
        :param direction: if positive or zero, rotates counter clockwise; clockwise else
        '''
        new_gremlins = []
        for gremlin in self.gremlins:
            new_dir = clock(gremlin[1], (1 if direction >= 0 else -1))
            new_gremlins.append((gremlin[0], new_dir, gremlin[2]))
        self.gremlins = new_gremlins
        self.display.update_gremlins(self.gremlins)
        
    def collision(self):
        pass #TODO
    
def begin():
    Engine()

if __name__ == "__main__":
    begin()