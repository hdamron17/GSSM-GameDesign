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
        self.total_moves = 0
        self.level_moves = 0
        
        self.init_board(board_file, board_type)
        try:
            self.loop()
        except Exception as e:
            print("You died with exception %s" % e)
    
    def new_level(self, board_file="tests/gameboard_test2.map", board_type="text"):
        del self.display #remove display window to start again
        self.init_board(board_file, board_type)
        self.loop()
    
    def init_board(self, board_file="tests/gameboard_test.map", board_type="text"):
        if board_type == "text":
            self.board = board_from_text_file(board_file)
        else:
            warnings.warn("Unsupported board_type")
            return
        
        self.max_y = len(self.board)
        self.max_x = max([len(row) for row in self.board])
        
        self.gremlins = self.first_gremlin()
        self.display = GameBoard(self.board, self.gremlins)
    
    def loop(self):
        done = False
        cont = True
        while not done and cont:
            for event in self.display.loop():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        cont = self.move()
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
            moved = self.forward(gremlin)
            if len(moved) > 0:
                new_gremlins.extend(moved)
            else:
                #A door was hit so it's inside another loop
                return False
        self.gremlins = new_gremlins
        self.display.update_gremlins(self.gremlins)
        
        self.total_moves += 1
        self.level_moves += 1
        
        return True
    
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
        x, y = gremlin[0]
        
        new_loc = new_x, new_y = (x+dx, y+dy)
        
        self.total_moves += 1
        self.level_moves += 1
        
        if not (0 <= new_x < self.max_x) or not (0 <= new_y < self.max_y):
            #out of bounds -> turn around
            return self.forward((new_loc, clock(direction, 2), gremlin[2]))
            
        next_tile = self.board[new_y][new_x]
        if next_tile is Tile.OCCUPIED:
            #occupied so turn around
            return self.forward((new_loc, clock(direction, 2), gremlin[2]))
        
        #four cases of hitting mirrors
        elif next_tile is Tile.FW_SLASH and direction in (Direction.UP, Direction.RIGHT):
            up = self.forward((new_loc, Direction.UP, gremlin[2]))
            right = self.forward((new_loc, Direction.RIGHT, gremlin[2]))
            return up + right
        
        elif next_tile is Tile.FW_SLASH and direction in (Direction.DOWN, Direction.LEFT):
            down = self.forward((new_loc, Direction.DOWN, gremlin[2]))
            left = self.forward((new_loc, Direction.LEFT, gremlin[2]))
            return down + left
        
        elif next_tile is Tile.BK_SLASH and direction in (Direction.DOWN, Direction.RIGHT):
            down = self.forward((new_loc, Direction.DOWN, gremlin[2]))
            right = self.forward((new_loc, Direction.RIGHT, gremlin[2]))
            return down + right
        
        elif next_tile is Tile.BK_SLASH and direction in (Direction.UP, Direction.LEFT):
            up = self.forward((new_loc, Direction.UP, gremlin[2]))
            left = self.forward((new_loc, Direction.LEFT, gremlin[2]))
            return up + left
        
        elif next_tile is Tile.DOOR:
            #a door yay!
            self.new_level()
            return []
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