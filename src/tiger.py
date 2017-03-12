#! /usr/bin/env python

''' 
Pygame implementation of game Tiger by Hunter Damron
'''

import pygame
from collections import OrderedDict


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
    Draws circles to board based on nodes list
    :param surface: Pygame surface to draw circles on
    :param nodesX: 2D list with node x values separated by layer
    :param nodesY: list of layer y positions
    :param radius: circle radius (as decimal of surface x size)
    '''
    surfaceX, surfaceY = surface.get_size()

    r = int(radius * surfaceX)

    for y_index in range(len(nodesY)):
        y = nodesY[y_index]
        for x in nodesX[y_index]:
            realX = int(x * surfaceX)
            realY = int(y * surfaceY)
            if debug: print("%.2f, %.2f -> %d, %d" % (x, y, realX, realY))
            pygame.draw.circle(surface, (255, 0, 0), (realX, realY), r)

    coloredX = (nodesX[0][0], nodesX[1][2], nodesX[1][3])
    coloredY = (nodesY[0], nodesY[1], nodesY[1])
    for x,y in zip(coloredX, coloredY):
        realX = int(x * surfaceX)
        realY = int(y * surfaceY)
        pygame.draw.circle(surface, (0,128,255), (realX, realY), r)

def draw_board_lines(surface, nodesX, nodesY, width, debug=False):
    surfaceX, surfaceY = surface.get_size()

    for y_index in range(1,len(nodesY)-1):
        #loop through y layers to draw horizontal lines
        y = nodesY[y_index]
        realY = int(y * surfaceY)
        startX = nodesX[y_index][0]
        stopX = nodesX[y_index][-1]
        real_startX = int(startX * surfaceX)
        real_stopX = int(nodesX[y_index][-1] * surfaceX)
        real_width = int(width * surfaceX)
        if real_width <= 0: real_width = 1
        if debug: print("(%.2f, %.2f) -> (%.2f, %.2f)" % (real_startX, realY, real_stopX, realY))
        pygame.draw.line(surface, (255,255,0), (real_startX, realY), (real_stopX, realY), real_width)

    #TODO draw 'vertical' lines down y layers (and figure out how to abstract it)

    if debug: print() #a new line for readability

def draw_board(surface, nodesX, nodesY, lambs=(), tigers=(), line_width=0.001, radius=0.03, debug=False):
    ''' 
    Draws gameboard on surface with lambs and tigers in their places; returns nothing
    :param lambs: (x,y) integer tuples with lamb locations starting from top left
    :param tigers: (x,y) integer tuples with tiger locations starting from top left
    :param radius: radius of each circle (as decimal of surface x size)
    :param line_width: width of lines between nodes (as decimal of surface x size)
    :param debug: if True, prints debugging information
    '''
    draw_board_lines(surface, nodesX, nodesY, line_width, debug)
    draw_board_circles(surface, nodesX, nodesY, radius, debug)


if __name__ == "__main__":
    ## Pygame related variables
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    done = False
    clock = pygame.time.Clock()

    ## Mechanic related variables
    nodesY = [0.2, 0.5, 0.7, 0.9]
    nodesX = [[0.5,], [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]] #initial nodesX
    restrictions = (0, 2)

    nodesX = board_nodes(nodesY, nodesX, restrictions)

    ## Display related variables
    radius = 0.03

    ## Loop until user exits
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0,0,0))
        draw_board(screen, nodesX, nodesY, radius=radius)

        pygame.display.flip()


while not done and False: ##TODO remove this (here for reference only)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 3
    if pressed[pygame.K_DOWN]: y += 3
    if pressed[pygame.K_LEFT]: x -= 3
    if pressed[pygame.K_RIGHT]: x += 3

    if is_blue: color = (0, 128, 255)
    else: color = (255, 100, 0)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    pygame.display.flip()
    clock.tick(60)
