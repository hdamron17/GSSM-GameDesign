#! /usr/bin/env python

'''
Pygame implementation of game Tiger by Hunter Damron
'''

import pygame

from collections import OrderedDict
import copy
import math


def new_row(nodesY, prevX, layer, masterX=0.5, debug=False):
    '''
    Constructs new row for drawing board
    :param nodesY: y positions list of each node
    :param prevX: x positions list of nodes on previous layer
    :param layer: layer index (int) to construct (must be less than len(nodesY)
    :param masterX: x position of top master node (usually 0.5 because centered)
    :return: returns list of x values for new layer
    '''
    row = []

    if debug: print("  layer: %d" % layer)

    centerX = masterX #add displacement to center x
    prev_sumY = nodesY[layer-1] - nodesY[0] # - nodesY[0] * (layer-1)) #sum of y until previous row to divide in proportionality
    sumY = nodesY[layer] - nodesY[0]

    for upperX in prevX:
        #do this for each point in the previous row
        prev_dispX = upperX - masterX #x displacement of above node for proportionality \
        point = centerX + prev_dispX * sumY / prev_sumY
        if debug: print("  %.2f = %.2f + %.2f * %.2f / %.2f" % (point, centerX, prev_dispX, sumY, prev_sumY))
        row.append(point)
    if debug: print() #add a newline just to make it readable
    return row

def board_nodes(nodesY, initial_nodesX, restrictions, debug=False):
    '''
    Creates list with full board dimensions
    :param nodesY: y positions of all node layers (including first 2)
    :param nodesX: list containing lists for x positions of first 2 layers
    :param restrictions: list of even numbers describing how many nodes will be left out from layer above it (i.e. two restrictions of 2 will equal a 4 restriction in second layer)
    :param debug: if True, it will print debuggin info
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
        nodesX.append(new_row(nodesY, nodesX[-1][slice[0]:slice[1]], len(nodesX), debug=debug))

    return nodesX

def draw_board_circles(surface, nodesX, nodesY, radius, debug=False):
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

def draw_board_lines(surface, nodesX, nodesY, width, color=(255,255,0), debug=False):
    '''
    Draws lines between nodes (modifies surface instead of returning)
    :param surface: Pygame surface to draw on
    :param nodesX: 2d integer list of x values separated by layer
    :param nodesY 1d integer list of y values
    :param width: integer width of lines
    :param color: 3-tuple with integer colors in [0,255]
    :param debug: if True, prints debug information if any
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

            if debug: print("(%d,%d) -> (%d,%d)" % (startX, startY, stopX, stopY))
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

def draw_board(surface, nodesX, nodesY, lambs=(), tigers=(), lamb_color=(0,0,0), tiger_color=(255,255,255), line_width=1, radius=10, debug=False):
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
    :param debug: if True, prints debugging information if any
    '''
    if debug: print((nodesX, nodesY, line_width, radius))
    draw_board_lines(surface, nodesX, nodesY, width=line_width, debug=debug)
    draw_board_circles(surface, nodesX, nodesY, radius=radius, debug=debug)
    draw_board_animals(surface, nodesX, nodesY, lambs, lamb_color, int(0.8*radius))
    draw_board_animals(surface, nodesX, nodesY, tigers, tiger_color, int(0.8*radius))

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
    #print("%s -> %s" % (from_yx, to_yx)) #TODO remove

    if (lamb_turn and from_yx not in lambs) or (not lamb_turn and from_yx not in tigers):
        #The from_yx location does not contain the player's piece
        return False, None #Not a valid move and no pieces were taken

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
    #print(offset) #TODO
    #print("%s --> %s" % (from_x, modified_to_x)) #TODO remove
    if from_x != modified_to_x and from_y != to_y:
        #The points are not aligned in x or y direction
        return False, None #See above for explanation

    #TODO make sure to handle negative offset when moving up the board
    #TODO make sure moves are linear (with offset)
    #TODO special case of moving to/from master node
    #TODO special case of moving between bottom nodes (not allowed but works now)

    #TODO lots of steps here

    return True, None #TODO remove - this needs to be more complicated to account for jumps and offsets, etc.

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

def endgame(board_shape, lambs, tigers, unplaced_lambs):
    '''
    Determines the winner of the game if any
    :param board_shape: 1d list of row lengths
    :param lambs: lambs locations (y,x) integer index tuples
    :param tigers: tiger locations (y,x) integer index tuples
    :param unplaced_lambs: integer number of unplaced lambs
    :return: Returns "null", "tiger", or "lamb" to denote winner
    '''
    #If any tiger cannot move it is dead #TODO move these conditions to another which just removes pieces instead of ending game
    for tiger in tigers:
        if not valid_move(lamb_turn, board_shape, from_yx, to_yx, lambs, tigers):
            return "lamb"


if __name__ == "__main__":
    ## Pygame related variables
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    done = False
    clock = pygame.time.Clock()

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

    awaiting_second = False #boolean determines if a click designates the second click in sequence
    first_node = None #(y,x) index location of node moving from

    ## Display related variables
    radius = 0.03 #radius before conversion
    line_width = 0.005 #line width before conversion

    nodesX, nodesY, (radius, line_width) = convert_nodes(nodesX, nodesY, screen.get_size(), [radius, line_width])
    if line_width <= 0: line_width = 1 #make sure there are actually lines

    lamb_color = (100,0,30) #color of lamb markers
    tiger_color = (30,0,100) #color of tiger markers

    flash_background = False #TODO remove - for debugging inputs only

    ## Loop until user exits
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
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
                    flash_background = not flash_background #TODO remove

        #TODO remove background flash
        screen.fill((255,255,255) if lamb_turn else (0,0,0)) #reset screen to redraw

        #draw board with animals and everything on it
        draw_board(screen, nodesX, nodesY, lambs=lambs, tigers=tigers, lamb_color=lamb_color,
            tiger_color=tiger_color, radius=radius, line_width=line_width)

        pygame.display.flip()
