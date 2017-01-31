import curses
import _curses

BOARD_SIZE = 7 #Board Size is a constant. Make sure it's odd.
STARTING_ENERGY = 50 #Energy to start with

BOARD_STRING_WIDTH = 8 * BOARD_SIZE + 13 #String length of the rendered board
LEFT_INDICATOR_XY = (2, 6) #(x,y) position of left indicator
RIGHT_INDICATOR_XY = (8 * BOARD_SIZE + 8, 6) #(x,y) position of right indicator

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

def render_single_line(location, default, token, predecessor="      ", postdecessor="       "):
	"""
	Renders a single line to be different where token is
	:param location: Integer location of token (where 0 is center)
	:param default: Default string for where token is not
	:param token: String for where token is
	:param predecessor: String to append to the front
	:param postdecessor: String to append to the end
	:return: Returns the single rendered line as a string
	"""
	index = location + BOARD_SIZE // 2 #Convert location (0 is center) to index (0 is first element)
	return predecessor + (default * index) + (token) + (default * (BOARD_SIZE-index-1)) + postdecessor
		#Puts everything together using Python's nice string * integer functionality

def render_board(location, left, right):
	"""
	Renders the tokens part of the board to the screen
	:param location: Integer location on board (0 <= location < BOARD_SIZE)
	:param left: Left player energy
	:param right: Right player energy
	:return: Returns the board as a string
	"""
	assert -BOARD_SIZE//2 < location <= BOARD_SIZE//2, "Out of board range" #Makes sure location is valid

	#Upper and lower part of screen
	outer_string = render_single_line(location, "        ", "   |    ")
	#Top and bottom of box	box_edge_string = "+-----+ " * BOARD_SIZE
	box_edge_string = "      " + "+-----+ " * BOARD_SIZE
	#Top of token
	token_top_string = render_single_line(location, "|     | ", "| /-\ | ", " Left ", "Right ")
	#Center of token
	token_center_string = render_single_line(location, "|     | ", "| |X| | ", "  %02d  " % left, " %02d  " % right)
	#Bottom of token
	token_bottom_string = render_single_line(location, "|     | ", "| \-/ | ")

	#Joins each line with a newline to make one nice big thing
	return "\n".join((outer_string, outer_string, box_edge_string,
		token_top_string, token_center_string, token_bottom_string,
		box_edge_string, outer_string, outer_string))

def user_ints(window, left_current, right_current):
	"""
	Waits for both users to press 'w'/'s' or 'o'/'l' then 'd' and 'k' for up/down 
		and enter on left or right respectively, respectively

	-Constrains the number to 0 <= energy < current
	:param window: Curses window object to interact with
	:param left_current: Left side current energy
	:param right_current: Right side current energy
	:param LEFT_INDICATOR_XY: (x,y) tuple with left indicator position
	:param RIGHT_INDICATOR_XY: (x,y) tuple with right indicator postition
	:return: Returns the numbers entered by each side as a tuple
	"""
	left_done = right_done = False #Left and right done booleans
	left = right = 0 #Left and right energies

	if left_current <= 0:
		#Left side is done if they have no energy
		left_done = True
		window.addch(LEFT_INDICATOR_XY[1], LEFT_INDICATOR_XY[0], ord('*')) #Puts indicator of left done
	if right_current <= 0:
		#Right side is done if they have no energy
		right_done = True
		window.addch(RIGHT_INDICATOR_XY[1], RIGHT_INDICATOR_XY[0], ord('*')) #Puts indicator of right done
	window.refresh()

	while not left_done or not right_done:
		#Continues asking for input as long as either side is not done
		character = window.getkey() #Gets key from user
		if not left_done:
			#If left side is not done, it tries to interpret as a left side command
			if character == 'w':
				left += 1 #Increment left if w is pressed
			elif character == 's':
				left -= 1 #Decrement left if s is pressed
			elif character == 'd':
				left_done = True #Submit left if d is pressed
		if not right_done:
			#If right side is not done, it tries to interpret as right side command
			if character == 'o':
				right += 1 #increment right if o is pressed
			elif character == 'l':
				right -= 1 #decrement right if l is pressed
			elif character == 'k':
				right_done = True #submit right if k is pressed

		if left_done:
			window.addch(LEFT_INDICATOR_XY[1], LEFT_INDICATOR_XY[0], ord('*')) #Puts indicator of left done
		if right_done:
			window.addch(RIGHT_INDICATOR_XY[1], RIGHT_INDICATOR_XY[0], ord('*')) #Puts indicator of right done
		window.refresh()

	if left < 0: left = 0 #Cast left user input to the possible range [0, left_current]
	elif left > left_current: left = left_current

	if right < 0: right = 0 #Cast right user input to the possible range [0, right_current]
	elif right > right_current: right = right_current

	return left, right #return left and right as a tuple

def welcome(window):
	"""
	Prints a nice welcome to the screen

	:param window: Curses window object to print to
	"""
	#Creates a list of strings with border to be displayed on each line
	msgs = render_welcome([	"Welcome to Hunter Damron's ASCII Footsteps",
				" ",
				"Two players will compete to move the token",
				"from the middle to their respective sides.",
				"Each player starts with 50 energy points. ",
				"On each turn they can spend as many as they want.",
				"The player who spends more money wins the round",
				"and the token moves one step to their side.",
				"Be careful to not spend all of your points",
				"too early because if you run out, you're done.",
				"Good luck!",
				" ",
				"Press any key to begin" ])
	row = 0
	msg_width = len(msgs[0]) #Judging length by the cover (first element)
	msg_x = (BOARD_STRING_WIDTH - msg_width) // 2 if BOARD_STRING_WIDTH > msg_width else 0  #x coordinate of welcome string (centered)
	if msg_x + msg_width > window.getmaxyx()[1]:
		raise ScreenTooSmallException() #Screen too small
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

def show_commands(window):
	"""
	Shows command options at bottom of window
	:param window: Curses window object to manipulate
	"""
	height, width = window.getmaxyx() #Height, width of current window
	msg = ["w", "Left increase", "s", "Left decrease", "d", "Left submit",
		"o", "Right increase", "l", "Right decrease", "k", "Right submit"]
	cmd_len = 20 #Maximum length of command so that they can be arranged
	rows = (width // cmd_len) // (len(msg) // 2) + 1 #How many rows are needed
		#The above calculates number per row then integer divides by number of commands
	cur_row = height - rows -1 #Placement of row based on height
	cur_col = 0 #Current column of string placement
	highlighted = True #alternates to hightlight every other string (the commands)
	for string in msg:
		if highlighted:
			window.addstr(cur_row, cur_col, string, curses.A_REVERSE) #Print reversed color
			cur_col += 2 #add 2 for the letter and a space
		else:
			window.addstr(cur_row, cur_col, string) #Print regular
			cur_col += cmd_len - 2 #add the rest of the command length excluding the 2
			if cur_col + cmd_len > width:
				#Basically a '\n'
				cur_row += 1 #go to next row
				cur_col = 0 #reset to column 0
		highlighted = not highlighted #toggle highlighted
	window.refresh()

def main(screen):
	"""
	Main function which uses a curses screen to manipulate and do the game

	-The game is described in more detail in the README

	:param screen: Curses screen object to do the game on
	"""
	assert BOARD_SIZE % 2 == 1, "Board has unfair even number" #Make sure board is even or it won't work

	curses.noecho() #prevents writing chars to screen
	screen.clear() # Clears screen for the first time

	location = 0 #Initialize location to 0
	left_energy = right_energy = STARTING_ENERGY #Allocates starting energy

	welcome(screen) #Print pretty welcome screen
	screen.getkey() #Wait for a key press to start
	screen.clear()

	if BOARD_STRING_WIDTH > screen.getmaxyx()[1]:
		raise ScreenTooSmallException() #Screen too small
	screen.addstr(1, 0, render_board(location, left_energy, right_energy)) #Puts the rendered board on screen
	show_commands(screen) #Show help bar at bottom

	#While location is not in endpoints (or beyond in that impossible case)
	while -BOARD_SIZE//2 + 1 < location <= BOARD_SIZE//2 - 1 and (left_energy > 0 or right_energy > 0):
		left_minus, right_minus = user_ints(screen, left_energy, right_energy) #Get user inputs
		left_energy -= left_minus #Subtract left user bet from left energy
		right_energy -= right_minus #Subtract right user bet from right energy
		if left_minus > right_minus:
			location -= 1 #Moves coin to left if left bet more than right
		elif left_minus < right_minus:
			location += 1 #Moves coin to right if right bet more than left

		screen.clear() #Clear screen to recalculate display
		if BOARD_STRING_WIDTH > screen.getmaxyx()[1]:
			raise ScreenTooSmallException() #Screen too small
		show_commands(screen) #show help bar underneath
		screen.addstr(1, 0, render_board(location, left_energy, right_energy)) #Display the rendered gameboard
		screen.refresh() #update screen
	if location < 0:
		congrats_string = "Left side wins!" #Left side wins if location is less than 0
	elif location > 0:
		congrats_string = "Right side wins!" #Right side wins if location is greater than 0
	else:
		congrats_screen = "It's a draw." #No one wins if it ends exactly in the middle
	congrats_string += " Enter any key to exit." #Make sure the user knows how to get out of here

	screen.addstr(11, (BOARD_STRING_WIDTH - len(congrats_string))//2, congrats_string) #Print the final string in the center
	screen.refresh() #Publishes congrats string
	screen.getkey() #Wait for key press to exit

def wrapped_main():
	"""
	Wrapped main of module - creates a wrappered curses instance and does the main function with it
	"""
	try:
		curses.wrapper(main) #Python makes it into a nice wrapper to deal with curses
	except KeyboardInterrupt:
		#Because we want to die peacefully
		print("Leaving so soon? Goodbye.")
	except _curses.error:
		#Because curses can't handle things like terminal resize
		print("Error: Curses made an oops")
	except ScreenTooSmallException as err:
		#Because sometimes your screen is too small
		print(err)

if __name__ == "__main__":
    wrapped_main() #Do the wrapped_main when run as a main script
