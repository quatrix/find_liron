#!/usr/bin/python
import curses
import random
import time
from math import sqrt

# initialization
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
cheat = 0

def draw_frame(board,board_y,board_x):
	"""drawing frame borders and edges"""
	# drawing boards frames
	for frame_x in range(0,board_x):
		board.addch(0,frame_x,'-')
		board.addch(pad_y,frame_x,'-')

	for frame_y in range(0,board_y):
		board.addch(frame_y,0,'|')
		board.addch(frame_y,pad_x,'|')

	# making the edges prettier
	for edge in [[0,0],[board_y,0],[0,pad_x],[pad_y,pad_x]]:
		board.addch(edge[0],edge[1],'+')

def rand_table(bombs,holes,board_y,board_x):
	board_size = board_y * board_x
	bomb_chance = board_size / bombs
	hole_chance = board_size / holes

	board = []

	for y in range(0,board_y):
		board.append([])
		for x in range(0,board_x):
			board[y].append('')

	while bombs > 0 or holes > 0:
		rand_y = random.randrange(1,board_y)
		rand_x = random.randrange(1,board_x)

		if board[rand_y][rand_x] == '':
			if bombs > 0:
				board[rand_y][rand_x] = 'B'
				bombs -= 1;
			else:
				board[rand_y][rand_x] = 'O'
				holes -= 1;

	return board

def rand_liron(board,board_y,board_x):
	liron = [];

	for y in range(0,board_y):
		for x in range(0,board_x):
			if board[y][x] == 'O': 
				liron.append([y,x]);

	return liron[random.randrange(0,len(liron))]

def rand_player(board,board_y,board_x):
	player = [];

	for y in range(1,board_y):
		for x in range(1,board_x):
			if board[y][x] == '': 
				player.append([y,x]);

	return player[random.randrange(0,len(player))]

def draw_objs(pad,board,board_y,board_x):
	for y in range(0,board_y):
		for x in range(0,board_x):
			if board[y][x] == 'B': 
				pad.addstr(y,x, 'B', curses.color_pair(1) )
			elif board[y][x] == 'O': 
				pad.addstr(y,x, 'O', curses.color_pair(2) )
			elif board[y][x] == 'L': 
				pad.addstr(y,x, 'L', curses.color_pair(4) )

def board_message(message,color = 'red'): 
	colors = {'red': curses.color_pair(1), 'green': curses.color_pair(2), 'white': curses.color_pair(3)}

	pad.addstr(pad_y + 1,1, message,colors[color])
	pad.refresh(0,0, 0,0, pad_y + 1,pad_x)

	
# board size
pad_x = 60
pad_y = 30

# difficulty
bombs = 60
holes = 50
game_time  = 120

# creating the board
pad = curses.newpad(pad_y + 2 , pad_x + 2)

draw_frame(pad,pad_y,pad_x)
board = rand_table(bombs = bombs, holes = holes, board_y = pad_y, board_x = pad_x)

# select place for a player
y,x = rand_player(board,pad_y,pad_x)
pad.addch(y,x,'*')

# select a hole for liron
liron = rand_liron(board,pad_y,pad_x)

if cheat == 1:
	board[liron[0]][liron[1]] = "L"

# draw the shit
draw_objs(pad,board,pad_y,pad_x)

# calculating time
future_time = time.time() + game_time

# player last distance
distance = ''
warmcold = ''
# main loop, movement
while 1:
	pad.nodelay(1);
	time_left =  future_time - time.time()
	if time_left < 0:
		board_message("ata lo taamod be mivhan ha metziut")
		break
	
	message = "%3.2f - %s\t%s" % (time_left, "seconds left", warmcold)
	board_message(message,color = "white")

	c = pad.getch()
	if c != -1:
		# clear the last place
		pad.addch(y,x,' ');

		if c == ord('l') and (x + 1 < pad_x):x += 1 # right
		if c == ord('h') and (x - 1 > 0): x -= 1 # left
		if c == ord('k') and (y - 1 > 0): y -= 1 # up
		if c == ord('j') and (y + 1 < pad_y): y += 1 # down
		if c == ord('q'): break  # quit

			
		draw_objs(pad,board,pad_y,pad_x)
		pad.addch(y,x,'*')

		if board[y][x] == 'B':
			board_message("ata lo taamod be mivhan ha metziut")
			time.sleep(5)
			break
		elif board[y][x] == 'O' or board[y][x] == 'L':
			if y == liron[0] and x == liron[1]:
				board_message("ata taamod be mivhan ha metziut", color = "green")
				time.sleep(5)
				break
			else:
				y_dist = abs(y - liron[0])
				x_dist = abs(x - liron[1])

				t_dist = sqrt(y_dist**2 + x_dist**2)

				if distance:
					if t_dist < distance:
						warmcold = "warmer"
					elif t_dist == distance:
						warmcold = "pfft..."
					else:
						warmcold = "colder"
				
				distance = t_dist
				#warmcold = "%d %d " % (x_dist,y_dist)



# end of proggie
curses.endwin()
