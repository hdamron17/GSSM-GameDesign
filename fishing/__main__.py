""" 
Fishing game inspired by Dilbert
"""

import curses #curses text display
import _curses #curses hidden stuff (like exceptions)
import random #spontaneity
import time #because time is just a python module
import sys #you can't trust the system (except in Python)


BOARD_SIZE = 5 #Board size as a square of this value
RANDOM_MEAN = 3 #Mean of random distribution (seconds)
RANDOM_STD_DEV = 1 #Standard deviation of random distribution (seconds)

BOARD_STRING_WIDTH = BOARD_SIZE * 3 + 1

class ScreenTooSmallException(Exception):
    """ 
    Error which arises if your screen is too small and curses doesn't care
    """

    def __init__(self):
        """
        Empty constructor because you don't need anything
        """
        pass

    def __str__(self):
        """
        toString equivalent in Python to explain 'what had happened was...'
        :return: Returns a nice description of the event
        """
        return "Error: Your screen was too small"

def render_board(screen, x, y):
    """ 
    Renders the board with token at specific position
    :param x: x location (left as 0)
    :param y: y location (top as 0)
    :return: Returns a curses pad which belongs to screen
    """
    assert x < BOARD_SIZE and y < BOARD_SIZE, "Out of bounds"
    pad_width = 3 * BOARD_SIZE + 2 #String width of pad
    pad_height = 2 * BOARD_SIZE + 2 #String height of pad
    edge_line = "+~~" * BOARD_SIZE + "+\n" #Tops and bottoms of the boxes
    center_line = "|  " * BOARD_SIZE + "|\n" #Going across the center of the boxes
    cursor_line = "|  " * x + "|<>" + "|  " * (BOARD_SIZE-x-1) + "|\n" #Center line with cursor in it
    total_board = (edge_line + center_line) * y + (edge_line + cursor_line) + \
        (edge_line + center_line) * (BOARD_SIZE-y-1) + edge_line #Total board string
    pad = curses.newpad(pad_height, pad_width)
    pad.addstr(0,0,total_board)
    return pad

def welcome(window):
    """ 
    Prints a nice welcome to the screen

    :param window: Curses window object to print to
    """
    #Creates a list of strings with border to be displayed on each line
    msgs = render_welcome([ "Welcome to Hunter Damron's ASCII Fishing inspired by Dilbert",
                " ",
                "The goal of the game is, quite simply, to catch fish.",
                "Use the arrow keys to move your cursor and 'q' to quit",
                "Be patient - the fish show up randomly in any of the spaces.",
                "If it shows up in your current space, you'll get a surprise.",
                "Thanks to the internet (specific site listed in README) for nice ASCII art fish.",
                "Good luck!",
                " ",
                "Press any key to begin" ])
    row = 0
    msg_width = len(msgs[0]) #Judging length by the cover (first element)
    msg_x = (BOARD_STRING_WIDTH - msg_width) // 2 if BOARD_STRING_WIDTH > msg_width else 0  #x coordinate of welcome string (centered)
    if msg_x + msg_width > window.getmaxyx()[1]:
        raise ScreenTooSmallException() #Screen too small
    window.clear()
    for line in msgs:
        window.addstr(3 + row, msg_x, line) #Displays each row starting from row 3
        row += 1 #Increment row
    window.refresh()

def render_welcome(string_list, buffer = 8):
    """ 
    Renders the welcome message with a fance border
    :param string_list: List of strings by line in message (should include "press key to start")
    :param buffer: Number of spaces to include on sides
    :return: Returns a list of strings with border attached
    """
    max_line = max(map(len,string_list)) #Finds max of string_list using length of each string
    msg_list = [] #empty list to be appended later
    msg_list.append("+" + "=" * (max_line + buffer) + "+") #Top border
    msg_list.append("|" + " " * (max_line + buffer) + "|") #Space between top border and words
    for line in string_list:
        spaces = max_line + buffer - len(line) #number of spaces needed to fill
        msg_list.append("|" + " " * (spaces // 2) + line + " " * (spaces // 2 + spaces % 2) + "|") #Append each line in list with buffering spaces
    msg_list.append("|" + " " * (max_line + buffer) + "|") #Space between words and bottom border
    msg_list.append("+" + "=" * (max_line + buffer) + "+") #Bottom border
    return msg_list

def fish_pad(screen, fish_name):
    """ 
    Makes a curses pad to hold a fish art
    :param screen: curses screen object to make pad on top of
    :param fish_name: name of fish to use (must be a valid key in fishes dictionary)
    :return: Returns a curses pad object with fish string printed on it and message to wait for key press
    """
    if fish_name in fishes:
        #make sure we don't have dictionary accessing error
        fish_str = fishes[fish_name] #gets the fish string by its name
        wait4key = "Press any key to continue fishing" #tells user to hold their horses

        height = fish_str.count("\n") + 3 #height by counting newlines then adding one for last line and 2 for wait4key string
        width = max(map(len, fish_str.split("\n"))) + 1 #width is lenght of fishy string (max length line)
        if width < len(wait4key):
            #makes width larger if it takes more space to ask 4 key than to make fishy
            width = len(wait4key) #reassign to length of wait4key string
        pad = curses.newpad(height, width) #make a new pad to house the fish (more like an aquarium)
        pad.addstr(0,0,fish_str) #add fish string to pad
        pad.addstr(height-2, 0, wait4key) #add string at the end to say to wait
        return pad
    else:
        raise Exception("Not a valid fishy")

# ASCII images from http://www.ascii-code.com/ascii-art/animals/fish.php

fishes = {
    # "Cory" by Max Strandberg
    "cory":
    r""" 
      /\
    _/./
 ,-'    `-:..-'/
: o )      _  (
"`-....,--; `-.\
    `'
    """,

    # "Whale" by Riitta Rasimus
    "whale":
    r""" 
       .
      ":"
    ___:____     |"\/"|
  ,'        `.    \  /
  |  O        \___/  |
~^~^~^~^~^~^~^~^~^~^~^~^~
    """,

    # "Sea Horse" by Morfina
    "sea_horse":
    r""" 
      \/)/)
    _'  oo(_.-.
  /'.     .---'
/'-./    (
)     ; __\
\_.'\ : __|
     )  _/
    (  (,.
     '-.-'
    """,

    #Art by Shanaka Dias
    "shark":
    r""" 
 _________         .    .
(..       \_    ,  |\  /|
 \       O  \  /|  \ \/ /
  \______    \/ |   \  /
     vvvv\    \ |   /  |
     \^^^^  ==   \_/   |
      `\_   ===    \.  |
      / /\_   \ /      |
      |/   \_  \|      /
             \________/
    """
}

def main(screen):
    """ 
    Main function of game
    :param screen: Curses screen object provided by curses wrapper
    """
    assert BOARD_SIZE >= 1, "Board too small"
    curses.noecho() #so you don't see what you type (WYTAWYG - What You Type Ain't What You Get)

    welcome(screen) #print welcome stuff
    screen.getch() #wait for key press

    screen.nodelay(1) #Does not wait on getch()

    loc_x = loc_y = 0 #Start location at 0 because it is always valid
    screen.clear() #clear the screen to start playing
    board = render_board(screen, loc_x, loc_y) #render the board the first time
    board.refresh(0,0,0,0, *screen.getmaxyx())
    next_time = time.time() + abs(random.gauss(RANDOM_MEAN, RANDOM_STD_DEV)) #calculate gaussian random time for next fish

    running = True #will be set to false if the user presses 'q'
    while running:
        #keep running until a quitter presses 'q'
        request_render = False #only request to re-render the screen if something changes

        if time.time() >= next_time:
            #if the time is past the randomly generated next fish time
            fish_x = random.randint(0,BOARD_SIZE-1) #fish random x location
            fish_y = random.randint(0,BOARD_SIZE-1) #fish random y location

            if loc_x == fish_x and loc_y == fish_y:
                #if the fish has same x and y coordinates as cursor
                screen.clear() #clear the screen
                screen.refresh() #TODO does this help at all?
                random_fish_pad = fish_pad(screen, random.choice(list(fishes.keys()))) #make a pad with ascii fish
                random_fish_pad.refresh(0,0,0,0,*screen.getmaxyx()) #refresh screen with fish on it
                random_fish_pad.getkey() #waits for key press
                request_render = True #request to re-render the board after fishy

            next_time = time.time() + abs(random.gauss(RANDOM_MEAN, RANDOM_STD_DEV)) #recalculate fish timing
        else:
            key = screen.getch() #get a key

            if key == curses.KEY_UP and loc_y > 0:
                #key up and can go up
                loc_y -= 1
                request_render = True
            elif key == curses.KEY_DOWN and loc_y < BOARD_SIZE-1:
                #key down and can go down
                loc_y += 1
                request_render = True
            elif key == curses.KEY_LEFT and loc_x > 0:
                #key left and can go left
                loc_x -= 1
                request_render = True
            elif key == curses.KEY_RIGHT and loc_x < BOARD_SIZE-1:
                #key right and can go right
                loc_x += 1
                request_render = True
            elif key == ord("q"):
                #'q' command for quitters
                running = False #quit the game

        if request_render:
            screen.clear()
            board = render_board(screen, loc_x, loc_y)

        board.refresh(0,0,0,0, *screen.getmaxyx()) #refresh the game board pad

        time.sleep(0.05) #small delay between frames so the screen doesn't go crazy

def wrapped_main():
    """ 
    Calls the main in a wrapper to make curses stuff simpler
    """
    try:
        curses.wrapper(main) #wraps the main to make curses work nicely
        print("So long and thanks for all the fish")
    except KeyboardInterrupt:
        #if the user gets bored and forgets the 'q' command
        print("Leaving so soon? Goodbye.")
    except _curses.error:
        #because sometimes curses makes errors too (sometimes screen too small)
        print("Error: Curses made an oops")
    except ScreenTooSmallException as err:
        #Because sometimes your screen is too small
        print(err)
    except Exception as err:
        print(err)

def parse_args(args_dict):
    """ 
    Parses the arguments and puts the values in variables
    """
    arg = "" #arg to look for (empty string when not looking
    if len(sys.argv) > 1:
        #if we have arguments to parse
        for single_arg in sys.argv[1:]:
            #for each argument after the first (name of script)
            if arg == "":
                #if arg=="" then we need an argument name
                if single_arg in args_dict.keys():
                    #make sure it's in the keys and a valid parameter
                    arg = single_arg #set arg to the parameter so next iteration looks for its value
                else:
                    #You want something not implemented
                    raise Exception("Invalid command line argument")
            else:
                #arg is not empty so we're looking for a value
                try:
                    value = int(single_arg) #in this game all are integers
                    globals()[args_dict[arg]] = value #replace former constant (global namespace was the only option I could think of)
                except:
                    raise Exception("Invalid value for %s" % arg)

if __name__ == "__main__":
    parse_args({"size": "BOARD_SIZE", "std_dev": "RANDOM_STD_DEV", "mean": "RANDOM_MEAN"}) #allow changing of global variables
    wrapped_main()
