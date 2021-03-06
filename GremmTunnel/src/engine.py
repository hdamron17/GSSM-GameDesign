'''
Central engine of the game - converts user inputs into game changes
'''

from pygame import QUIT, KEYDOWN, K_UP, K_LEFT, K_RIGHT, KMOD_CTRL, K_c, K_SPACE
from pygame.key import get_mods

from gui import GameBoard, WHITE, BLACK
from gameboard import BoardLayout
from general import Tile, GremmType, Direction, clock


MAX_RECURSION = 20

class Engine():
    '''
    Engine controls game logic and passes it to the gui
    '''
    
    def __init__(self, layout_file, display_message=True):
        '''
        Begins the game with specific parameters
        '''
        self.total_moves = 0
        self.level_moves = 0
        self.playing = not display_message
        
        self.layout_file = layout_file
        self.layout = BoardLayout(layout_file)
        self.init_board()
        
        if not self.playing:
            self.start_msg()
        
        self.loop()
    
    def win(self):
        '''
        Displays win message and stops accepting user input for playing other than x button
        '''
        self.playing = False
        self.display.update_message("You Win - Das Ende", WHITE, BLACK)
    
    def start_msg(self):
        '''
        Displays start message until spacebar
        '''
        self.display.update_message("Arrow keys to move, Spacebar to (re)start", BLACK, WHITE)
    
    def init_board(self, direction=Direction.UP, current_name=None):
        '''
        Initializes next board from the layout object and updates object accordingly
        :param direction: direction to go out of room
        :param current_name: name of current room (to go to next room) or None to get first room
        '''
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
        
        alt_color = self.layout.color(self.board_name)
        self.max_y = len(self.board)
        self.max_x = max([len(row) for row in self.board])
        
        self.gremlins = self.first_gremlin(new_direction)
        self.display = GameBoard(self.board, self.gremlins, alt_color=alt_color)
        
        if won:
            self.win()
    
    def loop(self):
        '''
        Basic loop tests pygame key events and reacts accordingly
        '''
        done = False
        while not done:
            for event in self.display.loop():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if self.playing:
                        if event.key == K_SPACE:
                            self.__init__(self.layout_file, False)
                            done = True
                        if event.key == K_UP:
                            self.move()
                        if event.key == K_LEFT:
                            self.rotate(1)
                        if event.key == K_RIGHT:
                            self.rotate(-1)
                        if event.key == K_c and (get_mods() & KMOD_CTRL):
                            done = True
                    elif event.key == K_SPACE:
                        self.display.clear_message()
                        self.playing = True
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
        Moves gremlins straight (and then some)
        '''
        new_gremlins = []
        for gremlin in self.gremlins:
            moved = self.forward(gremlin, 0)
            if len(moved) > 0:
                new_gremlins.extend(moved)
            else:
                #A door was hit so it's inside another loop
                return False
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
        :param count: number of times it was recursed to prevent exceeding MAX_RECURSION
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
                door_direction = self.which_door(new_loc)
                self.init_board(door_direction, self.board_name)
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
        '''
        Detects collisions and turns any collisions to OCCUPIED tiles in the board
        '''
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
    
    def which_door(self, loc):
        '''
        Determines which door is at a location
        :param loc: integer x,y tuple at edge of board
        :return: returns a direction enum for which way the gremlin would be going if it went directly out the door
        '''
        x,y = loc
        if x == 0: return Direction.LEFT
        elif x == self.max_x-1: return Direction.RIGHT
        elif y == 0: return Direction.UP
        elif y == self.max_y-1: return Direction.DOWN
        #if the place isn't a door, that's a persnal problem

def begin(layout_file="gbd1/gbd1.layout"):
    Engine(layout_file)

if __name__ == "__main__":
    begin()