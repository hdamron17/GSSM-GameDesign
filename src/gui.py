'''
Graphics part of the game - converts symbolic game representation to graphics then displays that.
Also handles user input and passes filtered input to the engine
'''

import pygame

import gameboard


BOX_SIZE = 40
HALF_BOX = int(BOX_SIZE / 2)
QUARTER_BOX = int(BOX_SIZE / 4)

LINE_WIDTH = 2

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
TRANSPARENCY=(0, 0, 0, 0)

BACKGROUND = BLACK
BACKGROUND_LINES = WHITE
DOOR = WHITE
GENERIC_ITEM = WHITE


class GameBoard():
    '''
    Single game board with resident game pieces
    '''
    
    def __init__(self, board):
        '''
        Creates GameBoard object from a board (created in gameboard modeule)
        '''
        pygame.init()
        self.y_size = len(board)
        self.x_size = max([len(row) for row in board])
        self.max_y = BOX_SIZE*self.y_size
        self.max_x = BOX_SIZE*self.x_size
        self.screen = pygame.display.set_mode((self.max_x, self.max_y))
        
        self.background = self.make_background(board)
        #self.gremlins = None #TODO TODO TODO
        
        self.layers = [
            self.background,
        #    self.gremlins
        ]
        
        self.blit_all(self.background)
        pygame.display.flip()

    def loop(self):
        '''
        Loops, returning commands from user
        :return: returns tuple of simplified user commands
        '''
        events = pygame.event.get()
        #self.blit("background")
        pygame.display.flip() #TODO determine if this can be changed to only updates sometimes
        return events
    
    def blit_all(self, surface):
        '''
        Blits the specified layer and everything above it
        '''
        index = self.layers.index(surface) #throws ValueError if non-existent
        for layer in self.layers[index:]:
            self.screen.blit(layer, (0,0))
        
    def update_background(self, board):
        self.background = self.make_background(board)
        self.blit_all(self.background)
    
    def make_background(self, board):
        '''
        Draws background and lines
        '''
        background = pygame.Surface((self.max_x, self.max_y))
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
                
                if tile == gameboard.Tile.BK_SLASH:
                    pygame.draw.line(background, BACKGROUND_LINES, (x, y), (x+BOX_SIZE, y+BOX_SIZE), LINE_WIDTH)
                    
                elif tile == gameboard.Tile.FW_SLASH:
                    pygame.draw.line(background, BACKGROUND_LINES, (x+BOX_SIZE, y), (x, y+BOX_SIZE), LINE_WIDTH)
                    
                elif tile == gameboard.Tile.OCCUPIED:
                    pygame.draw.rect(background, BACKGROUND_LINES, pygame.Rect(x, y, BOX_SIZE, BOX_SIZE), 0)
                    
                elif tile == gameboard.Tile.DOOR:
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
                        
                elif tile == gameboard.Tile.GENERIC_ITEM:
                    pygame.draw.circle(background, GENERIC_ITEM, (x+HALF_BOX, y+HALF_BOX), QUARTER_BOX, 0)
        
        return background
    
    def make_gremlins(self):
        pass #TODO TODO TODO
    
def test():
    board = GameBoard(gameboard.board_from_text_file("tests/gameboard_test.map"))
    done = False
    while not done:
        for event in board.loop():
            if event.type == pygame.QUIT:
                done = True

if __name__ == "__main__":
    test()