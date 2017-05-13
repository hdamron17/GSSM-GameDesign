'''
Central engine of the game - converts user inputs into game changes
'''

from pygame import QUIT, KEYDOWN, K_UP, K_LEFT, K_RIGHT, KMOD_CTRL, K_c
from pygame.key import get_mods

from gui import GameBoard, WHITE, BLACK
from gameboard import BoardLayout
from general import Tile, GremmType, Direction, clock


MAX_RECURSION = 20

class Engine():
    def __init__(self, layout_file):
        '''
        Begins the game with specific parameters
        '''
        self.total_moves = 0
        self.level_moves = 0
        self.playing = True
        
        self.layout = BoardLayout(layout_file)
        self.init_board()
        self.loop()
    
    def win(self):
        self.playing = False
        self.display.update_message("You Win - Das Ende", WHITE, BLACK)
    
    def init_board(self, direction=Direction.UP, current_name=None):
        won = False
        new_direction = direction
        if current_name is not None:
            next_map = self.layout.next_map(current_name, direction)
            if next_map is None:
                won = True
            else:
                self.board_name, self.board, new_direction = next_map
        else:
            self.board_name, self.board = self.layout.get_start()
        
        self.max_y = len(self.board)
        self.max_x = max([len(row) for row in self.board])
        
        self.gremlins = self.first_gremlin(new_direction)
        self.display = GameBoard(self.board, self.gremlins)
        
        if won:
            self.win()
    
    def loop(self):
        done = False
        while not done:
            for event in self.display.loop():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN and self.playing:
                    if event.key == K_UP:
                        self.move()
                    if event.key == K_LEFT:
                        self.rotate(1)
                    if event.key == K_RIGHT:
                        self.rotate(-1)
                    if event.key == K_c and (get_mods() & KMOD_CTRL):
                        done = True
                self.collision_detect()
    
    def first_gremlin(self, direction=Direction.UP):
        '''
        Finds the first gremlin in a map based on the door patterns
        :param direction: direction to go into map (not side to start on)
        :return: returns a list of one gremlin ((x,y),direction,type)
        '''
        if direction in (Direction.UP, Direction.DOWN):
            row = (len(self.board) - 1) if direction is Direction.UP else 0
            for i in range(len(self.board[row])):
                if self.board[row][i] is Tile.DOOR:
                    return [((i, row), direction, GremmType.GOOD)]
        
        if direction in (Direction.LEFT, Direction.RIGHT):
            col = (max([len(row) for row in self.board])) - 1 if direction is Direction.LEFT else 0
            for i in range(len(self.board)):
                if self.board[i][col] is Tile.DOOR:
                    return [((col, i), direction, GremmType.GOOD)]
        
        print("Error: no first door detected")
        return []
    
    def move(self):
        '''
        Moves gremlins straight
        '''
        new_gremlins = []
        for gremlin in self.gremlins:
            moved = self.forward(gremlin, 0)
            if len(moved) > 0:
                new_gremlins.extend(moved)
            else:
                #A door was hit so it's inside another loop
                return False
        
#         for gremlin in new_gremlins:
#             x,y = gremlin[0]
#             if self.board[y][x] is Tile.OCCUPIED:
#                 new_gremlins.remove(gremlin)
#         
        self.gremlins = new_gremlins
        self.display.update_gremlins(self.gremlins)
        
        self.total_moves += 1
        self.level_moves += 1
        
        return True
    
    def forward(self, gremlin, count=0):
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
        loc = x, y = gremlin[0]
        
        new_loc = new_x, new_y = (x+dx, y+dy)
        
        self.total_moves += 1
        self.level_moves += 1
        
        if not (0 <= new_x < self.max_x) or not (0 <= new_y < self.max_y):
            #out of bounds -> turn around
            return self.forward((new_loc, clock(direction, 2), gremlin[2]), count+1)
        
        try:
            next_tile = self.board[new_y][new_x]
            if next_tile is Tile.OCCUPIED:
                #occupied so turn around
                return self.forward((new_loc, clock(direction, 2), gremlin[2]), count+1)
        
            #four cases of hitting mirrors
            elif next_tile in (Tile.FW_SLASH, Tile.BK_SLASH):
                if count < MAX_RECURSION:
                    if next_tile is Tile.FW_SLASH and direction in (Direction.UP, Direction.RIGHT):
                        up = self.forward((new_loc, Direction.UP, gremlin[2]), count+1)
                        right = self.forward((new_loc, Direction.RIGHT, gremlin[2]), count+1)
                        return up + right
                    
                    elif next_tile is Tile.FW_SLASH and direction in (Direction.DOWN, Direction.LEFT):
                        down = self.forward((new_loc, Direction.DOWN, gremlin[2]), count+1)
                        left = self.forward((new_loc, Direction.LEFT, gremlin[2]), count+1)
                        return down + left
                    
                    elif next_tile is Tile.BK_SLASH and direction in (Direction.DOWN, Direction.RIGHT):
                        down = self.forward((new_loc, Direction.DOWN, gremlin[2]), count+1)
                        right = self.forward((new_loc, Direction.RIGHT, gremlin[2]), count+1)
                        return down + right
                    
                    elif next_tile is Tile.BK_SLASH and direction in (Direction.UP, Direction.LEFT):
                        up = self.forward((new_loc, Direction.UP, gremlin[2]), count+1)
                        left = self.forward((new_loc, Direction.LEFT, gremlin[2]), count+1)
                        return up + left
                else:
                    #TODO TODO TODO lose error
                    return []
            elif next_tile is Tile.DOOR:
                #a door yay!
                self.init_board(direction, self.board_name)
                return []
            else:
                return [(new_loc, direction, gremlin[2])]
        except RecursionError:
            return []
    
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
        
    def collision_detect(self):
        locations = [gremlin[0] for gremlin in self.gremlins]
        collision = False
        for gremlin in self.gremlins:
            loc = gremlin[0]
            if locations.count(loc) > 1:
                collision = True
                self.board[loc[1]][loc[0]] = Tile.OCCUPIED
                self.gremlins = list(filter(lambda grem: grem[0] != loc, self.gremlins))
        
        if collision:
            self.display.update_background(self.board)
            self.display.update_gremlins(self.gremlins)

def begin(layout_file="tests/overboard_test.layout"):
    Engine(layout_file)

if __name__ == "__main__":
    begin()