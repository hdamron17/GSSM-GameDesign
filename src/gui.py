'''
Graphics part of the game - converts symbolic game representation to graphics then displays that.
Also handles user input and passes filtered input to the engine
'''

import pygame
import math

from gameboard import board_from_text_file
from general import GremmType, Direction, Tile


BOX_SIZE = 80
HALF_BOX = int(BOX_SIZE / 2)
QUARTER_BOX = int(BOX_SIZE / 4)

LINE_WIDTH = 2

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
TRANSPARENCY = (0, 0, 0, 0)

BACKGROUND = BLACK
BACKGROUND_LINES = WHITE
DOOR = WHITE
GENERIC_ITEM = WHITE

GREMLIN_TYPE = {
    GremmType.GOOD : BLUE,
    GremmType.BAD : RED,
}

SQRT3 = math.sqrt(3)


class GameBoard():
    '''
    Single game board with resident game pieces
    '''
    
    def __init__(self, board=[[]], gremlins=[]):
        '''
        Creates GameBoard object from a board (created in gameboard modeule)
        '''
        pygame.init()
        self.y_size = len(board)
        self.x_size = max([len(row) for row in board])
        self.max_y = BOX_SIZE*self.y_size
        self.max_x = BOX_SIZE*self.x_size
        self.screen = pygame.display.set_mode((self.max_x, self.max_y))
        
        self.layers = {
            "background" : self.make_background(board),
            "gremlins" : self.make_gremlins(gremlins)
        }
        
        self.redraw()
        pygame.display.flip()

    def loop(self):
        '''
        Loops, returning commands from user
        :return: returns tuple of simplified user commands
        '''
        events = pygame.event.get()
        #self.blit("background")
        #pygame.display.flip() #TODO determine if this can be changed to only updates sometimes
        return events
    
    def blit_all(self, surface_name):
        '''
        Blits the specified layer and everything above it
        '''
        keys = list(self.layers.keys())
        index = keys.index(surface_name) #throws ValueError if non-existent
        for key in keys[index:]:
            self.screen.blit(self.layers[key], (0,0))
    
    def redraw(self):
        '''
        Redraws everything
        '''
        keys = list(self.layers.keys())
        index = 0
        for key in keys[index:]:
            self.screen.blit(self.layers[key], (0,0))
            self.screen.blit(self.layers[key], (0,0))
        pygame.display.flip()
        
    def update_background(self, board):
        '''
        Updates background with a new board
        '''
        self.layers["background"] = self.make_background(board)
        self.redraw()
    
    def make_background(self, board):
        '''
        Draws background and lines
        '''
        background = pygame.Surface((self.max_x, self.max_y), pygame.SRCALPHA)
        background.fill(BACKGROUND)
        
        for col in range(1, self.x_size):
            x = col * BOX_SIZE
            pygame.draw.line(background, BACKGROUND_LINES, (x, 0), (x, self.max_y), LINE_WIDTH)
            
        for row in range(1, self.y_size):
            y = row * BOX_SIZE
            pygame.draw.line(background, BACKGROUND_LINES, (0, y), (self.max_x, y), LINE_WIDTH)
        
        for row in range(0, self.y_size):
            y = row * BOX_SIZE
            for col in range(0, self.x_size):
                x = col * BOX_SIZE
                
                tile = board[row][col]
                
                if tile == Tile.BK_SLASH:
                    pygame.draw.line(background, BACKGROUND_LINES, (x, y), (x+BOX_SIZE, y+BOX_SIZE), LINE_WIDTH)
                    
                elif tile == Tile.FW_SLASH:
                    pygame.draw.line(background, BACKGROUND_LINES, (x+BOX_SIZE, y), (x, y+BOX_SIZE), LINE_WIDTH)
                    
                elif tile == Tile.OCCUPIED:
                    pygame.draw.rect(background, BACKGROUND_LINES, pygame.Rect(x, y, BOX_SIZE, BOX_SIZE), 0)
                    
                elif tile == Tile.DOOR:
                    points_list = [(x+HALF_BOX, y+HALF_BOX)]
                    up_x = x + BOX_SIZE
                    up_y = y + BOX_SIZE
                    if row <= 0:
                        points_list.extend([(x, y), (up_x, y)])
                    elif row >= self.y_size-1:
                        points_list.extend([(x, up_y), (up_x, up_y)])
                    elif col <= 0:
                        points_list.extend([(x, y), (x, up_y)])
                    elif col >= self.x_size-1:
                        points_list.extend([(up_x, y), (up_x, up_y)])
                    else:
                        pass
                    
                    if len(points_list) > 1:
                        pygame.draw.polygon(background, DOOR, points_list, 0)
                elif tile == Tile.GENERIC_ITEM:
                    pygame.draw.circle(background, GENERIC_ITEM, (x+HALF_BOX, y+HALF_BOX), QUARTER_BOX, 0)
        
        return background
    
    def update_gremlins(self, gremlins):
        '''
        Updates gremlins with a new list
        '''
        self.layers["gremlins"] = self.make_gremlins(gremlins)
        self.redraw()
        
    def make_gremlins(self, gremlins):
        '''
        Draws gremlins (currently as arrows) on board
        :param gremlins: list of gremlins in format ((x,y), direction, type)
        Note: x and y coordinates are integers starting with 0 as top left corner
        '''
        grem_surface = pygame.Surface((self.max_x, self.max_y), pygame.SRCALPHA)
        
        for gremlin in gremlins:
            print("gremlin %s" % (gremlins,))
            raw_x, raw_y = gremlin[0]
            direction = gremlin[1]
            gremlin_type = gremlin[2]
            
            color = GREMLIN_TYPE.get(gremlin_type)
            print("color %s" % (color,))
            location = (raw_x*BOX_SIZE, raw_y*BOX_SIZE)
            
            pygame.draw.polygon(grem_surface, color, arrow(location=location, direction=direction))
        
        return grem_surface
    
def arrow(box_size=BOX_SIZE, location=(0,0), direction=None):
    '''
    Creates arrow arrow coordinates
    :param box_size: size of bounding box
    :param location: integer 2-tuple location of upper right hand corner
    :param direction: from engine.Direction - of arrow
    :return: returns list of integer (x,y) tuples with locations
    '''
    a = BOX_SIZE #for convenience only
    base = [(0.1*a, 0.35*a), (0.6*a, 0.35*a), (0.6*a, 0.1*a), (0.9*a, 0.5*a), (0.6*a, 0.9*a), (0.6*a, 0.65*a), (0.6*a, 0.65*a), (0.1*a, 0.65*a)]
    if not direction or direction == Direction.RIGHT:
        pass #already right
    elif direction == Direction.DOWN:
        base = [(a-y, x) for x,y in base]
    elif direction == Direction.LEFT:
        base = [(a-x, a-y) for x,y in base]
    elif direction == Direction.UP:
        base = [(y, a-x) for x,y in base]
    
    return [(location[0] + x, location[1] + y) for x,y in base]
    
def test():
    board = GameBoard(board_from_text_file("tests/gameboard_test.map"), [((10,5), Direction.UP, GremmType.GOOD)])
    done = False
    while not done:
        for event in board.loop():
            if event.type == pygame.QUIT:
                done = True

if __name__ == "__main__":
    test()