#! /usr/bin/env python

'''
Pygame implementation of game Tiger by Hunter Damron
'''

import pygame

import copy
import math

#Winner enum *
TIE = 0
LAMB = 1
TIGER = 2

def new_row(nodesY, prevX, layer, masterX=0.5):
    '''
    Constructs new row for drawing board
    :param nodesY: y positions list of each node
    :param prevX: x positions list of nodes on previous layer
    :param layer: layer index (int) to construct (must be less than len(nodesY)
    :param masterX: x position of top master node (usually 0.5 because centered)
    :return: returns list of x values for new layer
    '''
    row = []

    centerX = masterX #add displacement to center x
    prev_sumY = nodesY[layer-1] - nodesY[0] # - nodesY[0] * (layer-1)) #sum of y until previous row to divide in proportionality
    sumY = nodesY[layer] - nodesY[0]

    for upperX in prevX:
        #do this for each point in the previous row
        prev_dispX = upperX - masterX #x displacement of above node for proportionality \
        point = centerX + prev_dispX * sumY / prev_sumY
        row.append(point)
    return row

def board_nodes(nodesY, initial_nodesX, restrictions):
    '''
    Creates list with full board dimensions
    :param nodesY: y positions of all node layers (including first 2)
    :param nodesX: list containing lists for x positions of first 2 layers
    :param restrictions: list of even numbers describing how many nodes will be left out from layer above it (i.e. two restrictions of 2 will equal a 4 restriction in second layer)
    :return: returns 2d list of each layer's x positions list (not uniform shape)
    '''
    assert len(initial_nodesX) == 2, "initial_nodesX can only contain 2 layers"
    assert len(nodesY) == len(initial_nodesX) + len(restrictions), "Invalid board generator dimensions"
    assert all([restriction % 2 == 0 for restriction in restrictions]), "All restrictions must be even"
    assert sum(restrictions) < len(initial_nodesX[1]), "Too many restrictions"

    nodesX = initial_nodesX
    restrictions_index = 0
    for i in range(len(initial_nodesX), len(nodesY)):
        restriction_half = int(restrictions[restrictions_index] / 2)
        restrictions_index += 1
        slice = (restriction_half, len(nodesX[-1]) - restriction_half)
        nodesX.append(new_row(nodesY, nodesX[-1][slice[0]:slice[1]], len(nodesX)))

    return nodesX

def draw_board_circles(surface, nodesX, nodesY, radius):
    '''
    Draws circles to board based on nodes list (using converted values)
    :param surface: Pygame surface to draw circles on
    :param nodesX: 2D integer list with node x values separated by layer
    :param nodesY: list of layer integer y positions
    :param radius: circle radius
    '''
    for y_index in range(len(nodesY)):
        y = nodesY[y_index]
        for x in nodesX[y_index]:
            pygame.draw.circle(surface, (255, 0, 0), (x, y), radius)

    coloredX = (nodesX[0][0], nodesX[1][2], nodesX[1][3])
    coloredY = (nodesY[0], nodesY[1], nodesY[1])
    for x,y in zip(coloredX, coloredY):
        pygame.draw.circle(surface, (0,128,255), (x, y), radius)

def draw_board_lines(surface, nodesX, nodesY, width, color=(255,255,0)):
    '''
    Draws lines between nodes (modifies surface instead of returning)
    :param surface: Pygame surface to draw on
    :param nodesX: 2d integer list of x values separated by layer
    :param nodesY 1d integer list of y values
    :param width: integer width of lines
    :param color: 3-tuple with integer colors in [0,255]
    '''
    for y_index in range(1,len(nodesY)-1):
        #draw horizontal lines
        y = nodesY[y_index]
        startX = nodesX[y_index][0]
        stopX = nodesX[y_index][-1]
        pygame.draw.line(surface, color, (startX, y), (stopX, y), width)

        #draw lines downways from each node
        cur_row = nodesX[y_index] #x values of current layer
        next_row = nodesX[y_index+1] #x values of layer below
        offset = int((len(cur_row) - len(next_row)) / 2) #shift between layers

        startY = nodesY[y_index] #y position of current node
        stopY = nodesY[y_index+1] #y position of below node

        for x_index in range(len(next_row)):
            #loop across all nodes which have corresponding nodes below
            startX = cur_row[x_index + offset] #x position of current node
            stopX = next_row[x_index] #x position of below node

            pygame.draw.line(surface, color, (startX, startY), (stopX, stopY), width)

    #draw lines to master node
    offset = int((len(nodesX[1]) - len(nodesX[-1])) / 2)
    for x in nodesX[1][offset:-offset]:
        #loop over center points of second row to draw points to master node
        pygame.draw.line(surface, color, (nodesX[0][0], nodesY[0]), (x, nodesY[1]), width)

def convert_nodes(old_nodesX, old_nodesY, surface_size, old_scalars=()):
    '''
    Converts nodes to pixelated version for drawing or mouse events
    :param old_nodesX: 2d list of floats to be converted
    :param old_nodesY: 1d list of floats to be converted
    :param surface_size: 2-tuple with x,y size of surface to plot on
    :param old_scalars: list of values to be converted (according to surface x size)
    :return: returns 2-tuple with (nodesX, nodesY) after conversion
    '''
    converted_nodesX = old_nodesX
    converted_nodesY = old_nodesY
    converted_scalars = old_scalars

    for y in range(len(old_nodesX)):
        for x in range(len(old_nodesX[y])):
            converted_nodesX[y][x] = int(old_nodesX[y][x] * surface_size[0])
    for y in range(len(old_nodesY)):
        converted_nodesY[y] = int(old_nodesY[y] * surface_size[1])
    for i in range(len(old_scalars)):
        converted_scalars[i] = int(old_scalars[i] * surface_size[0])
    return converted_nodesX, converted_nodesY, converted_scalars

def draw_board_animals(surface, nodesX, nodesY, locations, marker_color, radius):
    '''
    Draws makers on board at locations of animals (modifies surface instead of returning)
    :param surface: pygame surface to draw on
    :param nodesX: 2d integer x position list separated by layer
    :param nodesY: 1d integer y position list
    :param locations: list of (y,x) integer tuples with location index of each animal
    :param marker_color: integer 3-tuple with rgb color of markers
    :param radius: radius of marker
    '''
    for y_index, x_index in locations:
        x = nodesX[y_index][x_index]
        y = nodesY[y_index]
        pygame.draw.circle(surface, marker_color, (x, y), radius)

def draw_board_pointers(surface, nodesX, nodesY, pointers, size, line_width=1, pointer_color=(0,0,0)):
    '''
    Draws crosses on nodes for pointing (modifies surface rather than returning)
    :param surface: pygame surface to draw on
    :param nodesX: 2d list of x node positions separated by layer
    :param nodesY: 1d list of y positions for each layer
    :param pointers: list of (y,x) index tuples of nodes to draw on
    :param size: integer size of pointer cross
    :param line_width: width of line to use when drawing
    :param pointer_color: integer 3-tuple of color in rgb
    '''
    for y_index, x_index in pointers:
        x = nodesX[y_index][x_index]
        y = nodesY[y_index]
        r = int(size/2) #radius* of cross
        pygame.draw.line(surface, pointer_color, (x, y-r), (x, y+r), line_width)
        pygame.draw.line(surface, pointer_color, (x-r, y), (x+r, y), line_width)

def draw_board(surface, nodesX, nodesY, lambs=(), tigers=(), lamb_color=(0,0,0), tiger_color=(255,255,255),
        line_width=1, radius=10, pointers=[], pointer_color=(0,0,0), msg="", msg_color=(0,0,0), msg_size=20):
    '''
    Draws gameboard on surface with lambs and tigers in their places; returns nothing
    :param nodesX: 2d list of integer node x positions separated by layer (after conversion to surface size)
    :param nodesY: 1d list of integer node y positions (after conversion to surface size units)
    :param lambs: (y,x) integer tuples with lamb locations starting from top left
    :param tigers: (y,x) integer tuples with tiger locations starting from top left
    :param lamb_color: integer 3-tuple with rgb color for lamb markers
    :param tiger_color: integer 3-tuple with rgb color for tiger markers
    :param radius: radius of each circle (as decimal of surface x size)
    :param line_width: width of lines between nodes (as decimal of surface x size)
    :param pointers: list of (y,x) index tuples of nodes to draw crosses on for pointing
    :param msg: String message to print on the board
    '''
    draw_board_lines(surface, nodesX, nodesY, width=line_width)
    draw_board_circles(surface, nodesX, nodesY, radius=radius)
    draw_board_animals(surface, nodesX, nodesY, lambs, lamb_color, int(0.8*radius))
    draw_board_animals(surface, nodesX, nodesY, tigers, tiger_color, int(0.8*radius))
    draw_board_pointers(surface, nodesX, nodesY, pointers, int(1.2*radius), pointer_color=pointer_color)
    draw_text(surface, msg, int(0.7*surface.get_width()), int(0.2*surface.get_width()), color=msg_color, size=msg_size)

def dist(pos1, pos2):
    '''
    Euclidean distance between two points
    :param pos1: first (x,y) tuple
    :param pos2: second (x,y) tuple
    :return: returns float distance between points
    '''
    return math.sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )

def button_clicked(nodesX, nodesY, cursor_position, radius):
    '''
    Finds circle pointed to if any
    :param nodesX: 2d integer list of x positions separated by layer
    :param nodesY: 1d integer list of y positions of layers
    :param cursor_position: 2-tuple with cursor position
    :param radius: integer radius of each circle
    :return: returns (y,x) integer index tuple of node or None
    '''
    for y_index in range(len(nodesY)):
        y = nodesY[y_index]
        rowX = nodesX[y_index]
        for x_index in range(len(rowX)):
            x = rowX[x_index]
            if dist((x,y), cursor_position) <= radius:
                return y_index, x_index

def valid_move(lamb_turn, board_shape, from_yx, to_yx, lambs, tigers):
    '''
    Determines if move is valid
    :param lamb_turn: boolean True->lamb's turn, False->tiger's turn
    :param board_shape: 1d list of row lengths (y length is length of board_shape)
    :param from_yx: integer (y,x) index tuple from which animal moves
    :param to_yx: integer (y,x) index tuple to which animal moves
    :param lambs: list of integer (y,x) index tuples of lambs
    :param tiger: list of integer (y,x) index tuples of tigers
    :return returns tuple with (boolean of move validity (True->valid), (y,x) index tuple of removed animal or None)
    '''
    if (lamb_turn and from_yx not in lambs) or (not lamb_turn and from_yx not in tigers):
        #The from_yx location does not contain the player's piece
        return False, None #Not a valid move and no pieces were taken

    if to_yx in lambs or to_yx in tigers:
        #cannot be on top of another animal
        return False, None #Not a valid move and no pieces harmed in the production of this invalid move

    from_y = from_yx[0]
    to_y = to_yx[0]
    if 0 > from_y >= len(board_shape) or 0 > to_y >= len(board_shape):
        #Out of bounds in y direction
        return False, None #Again, not valid and no pieces taken

    from_x = from_yx[1]
    to_x = to_yx[1]
    from_x_len = board_shape[from_y]
    to_x_len = board_shape[to_y]
    if 0 > from_x >= from_x_len or 0 > to_x >= to_x_len:
        #Out of bounds in x direction
        return False, None #Once again, not valid and no pieces taken

    offset = int((board_shape[from_y] - board_shape[to_y]) / 2) #difference between locations
    #Note: x_offset may be negative when moving up the board
    modified_to_x = to_x + offset #index used for comparing linearity

    if (from_y == 0 and 1 <= to_x < board_shape[to_y]-1) or (to_y == 0 and 1 <= from_x < board_shape[from_y]-1):
        # moving from top node, offset should be whatever necessary to get to the next node
        # or moding to top node, offset should be the index of top node
        modified_to_x = to_x
    elif from_y == to_y and from_y == len(board_shape) - 1:
        #Attempting to move between nodes on the bottom rung
        return False, None #See above's above for explanation
    elif from_y != to_y and from_x != modified_to_x:
        #The points are not aligned in x or y direction
        return False, None #See above for explanation

    #Determine jumps or move distants restraints
    if from_y == to_y:
        #moving in y direction
        dist = abs(from_x - modified_to_x)
        if lamb_turn:
            #lambs can only move one so validity is determined by distance
            return dist <= 1, None
        else:
            #Tigers can either move one or jump a lamb_turn
            if dist > 2:
                #too far
                return False, None
            elif dist == 2:
                #possibly jumping a lamb
                dead_lamb = from_y, int((to_x + from_x) / 2)
                if dead_lamb in lambs:
                    return True, (dead_lamb)
                else:
                    return False, None
            else:
                return True, None
    else:
        #else moving in x direction
        dist = abs(from_y - to_y)
        if lamb_turn:
            #lambs can only move one so validity is determined by distance
            return dist <= 1, None
        else:
            #Tigers can either move one or jump a lamb_turn
            if dist > 2:
                #too far
                return False, None
            elif dist == 2:
                #possibly jumping a lamb
                lamb_y = int((to_y + from_y) / 2)
                lamb_offset = int((board_shape[from_y] - board_shape[lamb_y]) / 2) #offset to lamb location
                lamb_x = from_x - lamb_offset
                if from_x == 0:
                    #jumping from top node
                    lamb_offset = int((board_shape[to_y] - board_shape[lamb_y]) / 2) #offset to lamb location using to_y
                    lamb_x = to_x - lamb_offset

                lamb = lamb_y, lamb_x
                if lamb in lambs:
                    return True, lamb
                else:
                    return False, None
            else:
                return True, None

def valid_place(board_shape, place_yx, lambs, tigers):
    '''
    Determines if lamb plamement is valid
    :param board_shape: 1d list of row lengths
    :param place_yx: (y,x) integer index tuple of lamb placement
    :param lambs: lambs locations (y,x) integer index tuples
    :param tigers: tiger locations (y,x) integer index tuples
    :return: returns True if the placement is valid else False
    '''
    if place_yx in lambs or place_yx in tigers:
        #Placement is blocked by another animal
        return False

    y_index = place_yx[0]
    if 0 > y_index >= len(board_shape):
        #Out of bounds in y direction
        return False

    row_length = board_shape[y_index] #length of x row in board
    x_index = place_yx[1]
    if 0 > x_index >= row_length:
        #Out of bounds in x direction
        return False

    return True #Placement is within all bounds

def dead_tigers(board_shape, lambs, tigers):
    '''
    Determines how many tigers are immobile and consequently dead
    :param board_shape: 1d list of row lengths (y length is length of board_shape)
    :param lambs: list of integer (y,x) index tuples of lambs
    :param tigers: list of integer (y,x) index tuples of tigers
    :return: returns list of integer (y,x) index tuples of dead tigers
    '''
    dead_tigers = []
    for tiger in tigers:
        mobile = False #tiger starts off immobile then becomes mobile if any moves are valid
        for y in range(len(board_shape)):
            row_len = board_shape[y]
            for x in range(row_len):
                if valid_move(False, board_shape, tiger, (y,x), lambs, tigers)[0]:
                    mobile = True
        if not mobile:
            dead_tigers.append(tiger)
    return dead_tigers

def draw_text(surface, text, x, y, size=50, font='Comic Sans MS', color=(0,0,0)):
    '''
    Draws a text onto the surface (can be multiline)
    :param surface: pygame surface to draw on
    :param text: list of strings with text (separated by line)
    '''
    use_font = pygame.font.SysFont(font, size)
    for line in text.split("\n"):
        display_text = use_font.render(str(line), True, color)
        surface.blit(display_text, (x,y))
        y += size + 1

def main():
    ## Pygame related variables
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Hunter Damron's Tiger Game")

    ## Mechanic related variables
    nodesY = [0.2, 0.5, 0.7, 0.9] #before conversion
    nodesX = [[0.5,], [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]] #initial nodesX
    restrictions = (0, 2) #restrictions on node building (because bottom row only has 4 nodes)

    nodesX = board_nodes(nodesY, nodesX, restrictions) #x nodes before conversion

    row_sizes = [len(row) for row in nodesX] #gets list of row sizes

    lamb_turn = True
    unplaced_lambs = 15

    lambs = [] #list of lamb locations
    tigers = [(0,0), (1,2), (1,3)] #list of tiger locations

    playing = True #True as long as no player has won
    quit = False #true when user clicks the x button
    winner = TIE
    ready = False #is the user ready to play the game

    awaiting_second = False #boolean determines if a click designates the second click in sequence
    first_node = None #(y,x) index location of node moving from

    ## Display related variables
    radius = 0.03 #radius before conversion
    line_width = 0.005 #line width before conversion

    nodesX, nodesY, (radius, line_width) = convert_nodes(nodesX, nodesY, screen.get_size(), [radius, line_width])
    if line_width <= 0: line_width = 1 #make sure there are actually lines

    lamb_color = (0,0,0) #color of lamb markers
    tiger_color = (255,255,255) #color of tiger markers

    # Display welcome message
    msg =  "Welcome to Hunter Damron's Tiger Game, \n" + \
            "a digital clone of the age-old Tiger board game.\n\n" + \
            "To play, tigers and lambs move around \n" + \
            "the board attempting to trap each other.\n\n" + \
            "Tigers start with three markers on the board and can move them.\n" + \
            "Tigers can jump over lambs and capture them.\n\n" + \
            "Lambs start out with none on the board but \n" + \
            "15 in reserve and play a lamb each turn. \n" + \
            "Once all are played, lambs can move.\n\n" + \
            "If a tiger is unable to move, it is removed from the board.\n\n" + \
            "If all tigers are removed, the lambs win. \n" + \
            "If there are not enough lambs to capture a tiger, the tigers win.\n\n" + \
            "Press any key to continue."
    screen.fill((100,100,100))
    draw_text(screen, msg, 2, 2, size=24)

    pygame.display.flip()

    while not ready and not quit:
        for etype in map(lambda event: event.type, pygame.event.get()):
            if etype == pygame.QUIT:
                quit = True
            if etype == pygame.KEYDOWN or etype == pygame.MOUSEBUTTONDOWN:
                ready = True


    ## Loop until user exits
    while playing and not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #left mouse click
                clicked_node = button_clicked(nodesX, nodesY, pygame.mouse.get_pos(), radius)
                if clicked_node != None:
                    #a node is clicked
                    if awaiting_second and first_node != None:
                        #this is the node to move to
                        move = valid_move(lamb_turn, row_sizes, first_node, clicked_node, lambs, tigers)
                        if move[0]:
                            #it was a valid move
                            if lamb_turn:
                                lambs.remove(first_node)
                                lambs.append(clicked_node)
                            else:
                                tigers.remove(first_node)
                                tigers.append(clicked_node)
                                if move[1] != None:
                                    #lamb was eaten in the process
                                    lambs.remove(move[1])
                            lamb_turn = not lamb_turn #next turn
                        #whether it was valid or not, we want to start over looking for first_node
                        first_node = None
                        awaiting_second = False

                    else:
                        #this is the first click
                        if lamb_turn and unplaced_lambs > 0:
                            #lamb can place a token
                            if valid_place(row_sizes, clicked_node, lambs, tigers):
                                #lamb can be placed there
                                lambs.append(clicked_node)
                                unplaced_lambs -= 1
                                lamb_turn = not lamb_turn #next turn
                        else:
                            #clicked node becomes first click to move on next click
                            first_node = clicked_node
                            awaiting_second = True

                    #Eliminating all dead tigers and determining end game
                    for dead_tiger in dead_tigers(row_sizes, lambs, tigers):
                        tigers.remove(dead_tiger)

                    # Lambs are not enough (two because one cannot trap a tiger)
                    if unplaced_lambs + len(lambs) < 2:
                        playing = False
                        winner = TIGER

                    # Tigers are non-existent (because zero tigers don't exist)
                    if len(tigers) <= 0:
                        playing = False
                        winner = LAMB

        #Conditional background color
        screen.fill(lamb_color if lamb_turn else tiger_color) #reset screen to redraw

        #draw board with animals and everything on it
        draw_board(screen, nodesX, nodesY, lambs=lambs, tigers=tigers, lamb_color=lamb_color,
            tiger_color=tiger_color, radius=radius, line_width=line_width,
            pointers=([first_node] if first_node != None else []),
            pointer_color=(tiger_color if lamb_turn else lamb_color),
            msg="Unplaced Lambs: %s" % unplaced_lambs,
            msg_color=tiger_color if lamb_turn else lamb_color, msg_size=20)

        pygame.display.flip()

    # Display endgame stuff
    color = (100,100,100)
    alt_color = (0,0,0)
    msg = "It's a tie"
    if winner == LAMB:
        color = lamb_color
        alt_color = tiger_color
        msg = "Lamb wins"
    elif winner == TIGER:
        color = tiger_color
        alt_color = lamb_color
        msg = "Tiger wins"

    screen.fill(color)
    draw_text(screen, msg, int(screen.get_width()/2), int(screen.get_height()/2), color=alt_color)

    if not quit:
        pygame.display.flip()

    while not quit:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                quit = True
        #Do nothing while waiting on user to quit the window

if __name__ == "__main__":
    main()
