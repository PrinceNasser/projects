import tkinter as tk
from tkinter import ttk
import tkinter
from copy import copy

# create game window
window = tk.Tk()

# create window size and set no-resize option
window_dimensions = [1000, 700]
window.geometry(str(window_dimensions[0]) + "x" + str(window_dimensions[1]))
window.resizable(0, 0)

# set window title
window.title("Pong Game")

# choose fps for game
frames_per_second = 30

# create game canvas
game_canvas = tkinter.Canvas(window, width=window_dimensions[0], height=window_dimensions[1], bd=0, highlightthickness=0, background="#1d2021")
game_canvas.pack()

# create game variables

# paddle sizes
paddle_size = [15, 125]

# initial centered Y position for both paddles
initial_y_position = (window_dimensions[1] - paddle_size[1]) / 2

# player variables
player_y_position = initial_y_position
player_y_velocity = 0

# player2 variables
player2_y_position = initial_y_position
player2_y_velocity = 0

# ball variables
ball_diameter = 15

initial_ball_position = [(window_dimensions[0] - 35 - paddle_size[0]) - (int(window_dimensions[1] / 2)), ((window_dimensions[1] - ball_diameter) / 2) - (int(window_dimensions[1] / 2))]
initial_ball_velocity = [12, 12]

ball_position = copy(initial_ball_position)
ball_velocity = copy(initial_ball_velocity)

# score variable and widget
score = [0, 0]

# delete useless global variables
del initial_y_position

# display instructions variable
display_instructions = True
# Show options
def Options():
    # Theres actually no options available yet jeje
    meh = ttk.Label(
        window,
        text = "Not available yet... lol",
        font = ("serif", 10)
        )
    meh.place(relx = 0.75, rely = 0.55, anchor = 'center')
    window.after(400, meh.place_forget)

# Prompt the user a spoiler
def Soon():
    # Coming Soon!!
    spoiler = ttk.Label(
        window,
        text = "Coming Soon!",
        font = ("serif", 30),
        )
    spoiler.place(relx = 0.35, rely = 0.3, anchor = 'center')
    window.after(400, spoiler.place_forget)

# Prompt a menu to select which mode the user want to play
def Modes():    
    command = modes.place_forget()
    singlePlayer.place(relx = 0.35, rely = 0.4, anchor = 'center')
    twoPlayers.place(relx = 0.65, rely = 0.4, anchor = 'center')

# Hide all widgets of menu
def hide():
    command = [
        title.place_forget(), 
        singlePlayer.place_forget(), 
        twoPlayers.place_forget(),
        preferences.place_forget(), 
        close.place_forget()
        ]

# Starts game
# gameloop
def gameloop():
	# declare use of global variables
	global frames_per_second
	global game_canvas
	global window_dimensions
	global player_y_position
	global paddle_size
	global player2_y_position
	global ball_diameter
	global ball_position
	global ball_velocity
	global player_y_velocity
	global player2_y_velocity
	global display_instructions

	# call gameloop again in 100 milleseconds (gameloops is called every 100 MS)
	window.after(int(1000 / frames_per_second), gameloop)

	# clear canvas
	game_canvas.delete("all")
	
	# display player paddle (35 pixels from left)
	game_canvas.create_rectangle(35, player_y_position, 35 + paddle_size[0], player_y_position + paddle_size[1], fill="#ffffff", outline="#ffffff")

	# display player2 paddle (35 pixels from right)
	game_canvas.create_rectangle(window_dimensions[0] - 35, player2_y_position, (window_dimensions[0] - 35) - paddle_size[0], player2_y_position + paddle_size[1], fill="#ffffff", outline="#ffffff")

	# display ball
	game_canvas.create_rectangle(ball_position[0], ball_position[1], ball_position[0] + ball_diameter, ball_position[1] + ball_diameter, fill="#ffffff", outline="#ffffff")

	# display score (centered)
	game_canvas.create_text(window_dimensions[0] / 2, 35, anchor="center", font="Monaco 28 bold", fill="#ffffff", text=str(score[0]) + "   " + str(score[1]))

	# display center separator line
	game_canvas.create_line((window_dimensions[0] / 2) , 0, (window_dimensions[0] / 2), window_dimensions[1], fill="#ffffff", dash=(6, 10), width=3)

	# display instructions
	if(display_instructions):
		game_canvas.create_text((window_dimensions[0] / 2) - 30, window_dimensions[1] - 40, anchor="ne", font="Monaco 16 bold", fill="#ffffff", text="Move w/WASD")
		game_canvas.create_text((window_dimensions[0] / 2) + 30, window_dimensions[1] - 40, anchor="nw", font="Monaco 16 bold", fill="#ffffff", text="Move w/Arrows")

	# update player Y position and movement
	player_y_position += player_y_velocity

	# update player2 Y position and movement
	player2_y_position += player2_y_velocity
	
	# set window boundaries for max and min position for paddles
	
	# player paddle
	if(player_y_position + paddle_size[1] > window_dimensions[1]):
		player_y_position = window_dimensions[1] - paddle_size[1]
	elif(player_y_position < 0):
		player_y_position = 0

	# player2 paddle
	if(player2_y_position + paddle_size[1] > window_dimensions[1]):
		player2_y_position = window_dimensions[1] - paddle_size[1]
	elif(player2_y_position < 0):
		player2_y_position = 0

	# update ball position
	ball_position[0] += ball_velocity[0]
	ball_position[1] += ball_velocity[1]

	# set window boundaries for ball

	# top and bottom of screen
	if(ball_position[1] >= window_dimensions[1] - ball_diameter or ball_position[1] <= 0):
		ball_velocity[1] = -ball_velocity[1]

	# left side and right side of screen --> update score accordingly and reset ball vars
	if(ball_position[0] <= 0):
		# point for player2
		score[1] += 1
		
		# reset ball vars
		ball_position = copy(initial_ball_position)
		ball_velocity = copy(initial_ball_velocity)

	if(ball_position[0] >= window_dimensions[0] - ball_diameter):
		# point for player
		score[0] += 1

		# reset ball vars
		ball_position = copy(initial_ball_position)
		ball_velocity = copy(initial_ball_velocity)

	# paddle collision (also possibly one of the longest if statements you've seen in your life)
	if(((ball_position[0] >= 35 and ball_position[0] <= 35 + paddle_size[0]) and (ball_position[1] + ball_diameter >= player_y_position and ball_position[1] <= player_y_position + paddle_size[1])) or ((ball_position[0] + ball_diameter <= window_dimensions[0] - 35 and ball_position[0] + ball_diameter >= (window_dimensions[0] - 35) - paddle_size[0]) and (ball_position[1] + ball_diameter >= player2_y_position and ball_position[1] <= player2_y_position + paddle_size[1]))):
		ball_velocity[0] = -ball_velocity[0]

		# switch Y velocity if collision was on top or bottom sides of paddle

		# player paddle
		if(ball_velocity[0] >= 0):
			if((ball_position[1] + ball_diameter <= player_y_position + paddle_size[0] and ball_velocity[1] >= 0) or (ball_position[1] >= player_y_position + paddle_size[1] - paddle_size[0] and ball_velocity[1] <= 0)):
				ball_velocity[1] = -ball_velocity[1]

		# player2 paddle
		if(ball_velocity[0] <= 0):
			if((ball_position[1] + ball_diameter <= player2_y_position + paddle_size[0] and ball_velocity[1] >= 0) or (ball_position[1] >= player2_y_position + paddle_size[1] - paddle_size[0] and ball_velocity[1] <= 0)):
				ball_velocity[1] = -ball_velocity[1]

# handle arrow keys keydown events
def onKeyDown(e):
	# declare use of global variable(s)
	global player_y_velocity
	global player2_y_velocity
	global display_instructions

	# record current player velocities
	player_y_velocity_current = player_y_velocity
	player2_y_velocity_current = player2_y_velocity

	# bind arrow keys to player velocity changes
	if(e.keysym == "w"):
		# start movement up when up arrow is pressed down
		player_y_velocity = -15
	elif(e.keysym == "s"):
		# start movement down when down arrow is pressed down
		player_y_velocity = 15

	# bind WASD arrow keys to player2 velocity changes
	if(e.keysym == "Up"):
		# start movement up when w key is pressed down
		player2_y_velocity = -15
	elif(e.keysym == "Down"):
		# start movement down when s key is pressed down
		player2_y_velocity = 15
	
	# turn off instructions if either paddle has moved
	if(player_y_velocity_current != player_y_velocity or player2_y_velocity_current != player2_y_velocity):
		display_instructions = False

# handle arrow keys keyup events
def onKeyUp(e):
	# declare use of global variable(s)
	global player_y_velocity
	global player2_y_velocity

	# bind arrow keys to player velocity change
	if(e.keysym == "w" or e.keysym == "s"):
		# stop movement when either arrow key is released
		player_y_velocity = 0

	# bind WASD arrow keys to player2 velocity changes
	if(e.keysym == "Up" or e.keysym == "Down"):
		# stop movement when either w or s key is pressed down
		player2_y_velocity = 0

# Define Style
style = ttk.Style()
style.theme_use("clam")

# Buttons style
style.configure(
    "TButton", 
    font = ("serif", 30), 
    foreground = "#d4be98",
    bordercolor = "#ddc7a1"
    )

style.map(
    "TButton",
    background = [('active', '#3c3836'),('!disabled','#282828')],
    )

# Label style
style.configure(
    'TLabel', 
    font = ("serif",50),
    foreground = '#d4be98', 
    background = '#1d2021', 
    )

# Title of the game
title = ttk.Label(
    window,
    text = "Ping Pong!",
    )

# Display modes
modes = ttk.Button(
    window,
    text = "Play",
    command = Modes,
    )

# Single player mode. player vs AI
singlePlayer = ttk.Button(
    window,
    text = "Single player",
    command = Soon
    )

# Two player mode. Player vs Player
twoPlayers = ttk.Button(
    window,
    text = "Two players",
    command = lambda: [hide(), gameloop()]
    )

# Show options for the game
preferences = ttk.Button(
    window,
    text = "Options",
    command = Options,
    )

# Exit the window
close = ttk.Button(
    window,
    text = "Exit",
    command = lambda: window.quit()
    )

# Shows the widget. Statement positions.
title.place(relx = 0.5, rely = 0.1, anchor = 'center')
modes.place(relx = 0.5, rely = 0.4, anchor = 'center')
preferences.place(relx = 0.5, rely=0.55, anchor = 'center')
close.place(relx = 0.5, rely = 0.7, anchor = 'center')

# connect keydown event to function
window.bind("<KeyPress>", onKeyDown)

# connect keyup event to function
window.bind("<KeyRelease>", onKeyUp)

# method to keep the window alive and running.
window.mainloop() 
