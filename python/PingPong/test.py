# first things first let's import the libraries
# Import the module of tkinter as 'tk'
import tkinter as tk
from tkinter import ttk # Modern tkinter widgets 'ttk'
import random
import datetime

# ===========
# CONFIGURATION
# ===========
# Initial configuration of the window
root = tk.Tk() 
root.title('PingPong')
root.resizable(False, False)   
window_width = 960
window_height = 720

# Get the screen dimensions to find the "center" point of the window
center_x = int(root.winfo_screenwidth() / 2 - window_width / 2)
center_y = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# 16 bites
# colors_pallete = {}

# Initial game configuration
config = {
    "colors": {
        "background": "#1d2021",
        "foreground0": "#d4be98",
        "foreground1": "#ddc7a1",
        "ball": "#e78a4e",
        "left_paddle": "#7daea3",
        "right_paddle": "#ea6962",
        "ai_paddle": "#d3869b"
    },
    "game": {
        "name1": "The strongest in history",
        "name2": "The strongest of today",
        "bot_name": "AM",
        "fps": 60,
        "ball_radius": 16,
        "paddle_size": [20, 150],
        "ai_reflexes": 60,
        "sets": 3, # 3, 5 o 7
        "set_points": 11 # 11 o 21
    }

}

ball_position = [
    (window_width - 2 * config["game"]["ball_radius"]) / 2,
    (window_height - 2 * config["game"]["ball_radius"]) / 2]

ball_speed = [random.choice([-7.0, 7.0]), random.choice([-4.0, 4.0])] 

score = [0, 0]
sets = [0,0]

game_mode = None

# Canvas window configuration
game_canvas = tk.Canvas(root,
    width=window_width, 
    height=window_height, 
    bg="#1d2021",
    highlightthickness=0)

# ========
# OBJECTS
# ========

def decoration():
    # Raquet and ball decoration (this is optional btw)

    # Ball cords with 3D effect
    x_ball = window_width * 0.78
    y_ball = window_height * 0.18
        
    # Sombra del cuerpo
    for i in range(1, 3):
        game_canvas.create_oval(
            x_ball + i*7,  y_ball + i*7,
            (x_ball + 100) + i*7, (y_ball - 100) + i*7, 
            fill = "#3c3832",
            outline="#3c3832", 
            width = 1)
                
    # Cuerpo
    game_canvas.create_oval(
        x_ball , y_ball,
        x_ball + 100 , y_ball - 100,
        fill="#e78a4e", 
        outline="#3c3832", 
        width=1)
    
    # Efecto de brillo en la pelota
    game_canvas.create_oval(
        x_ball + 5, y_ball - 50,
        x_ball + 45, y_ball - 90,
        fill="#ffffff", 
        outline ="#e78a4e",  
        width=1)
    
    # Vertices del mango
    vertex_handle = [
        277-15, 405-120,
        277-15, 415-120,
        237-15, 455-120,
        227-15, 455-120,
        157-15, 385-120,
        147-15, 385-120,
        207-15, 325-120, 
        207-15, 335-120] 
    
    # Vertices de la raqueta octagonal
    vertex_wood =[
        207-15, 325-120,
        147-15, 385-120,             
        80-15,  385-120, 
        20-15,  325-120,
        20-15,  245-120,
        75-15,  195-120,
        147-15, 195-120,             
        200-15, 245-120]

    # shadow of handle (3 capas)
    for i in range(3, 0, -1):
        shadow_points_handle = [
            p + i*4 for p in vertex_handle
        ]

        game_canvas.create_polygon(
            shadow_points_handle,
            fill="#3c302f",
            outline="#3c3832")
    
    # Sombra de la goma de la raqueta (3 capas)
    for i in range(3, 0, -1):
        shadow_points_wood = [
            p + i*4 for p in vertex_wood
        ] 

        game_canvas.create_polygon(
            shadow_points_wood,
            fill="#3c3832",
            outline="#3c3832")
    
   # Handle
    game_canvas.create_polygon(
            vertex_handle,
            fill="#32302f")

    # Rubber
    game_canvas.create_polygon(
            vertex_wood,
            fill="red",
            outline="#282828")

def draw_net():
    # Draw the center line
    game_canvas.create_line(
        window_width / 2, 0,
        window_width / 2, window_height, 
        fill=config["colors"]["foreground1"],
        dash=(10, 10))

def draw_paddles(mode="two_player"):
    global left_paddle, right_paddle

    # Left paddle
    left_paddle = game_canvas.create_rectangle(
        50, 
        window_height / 2 - config["game"]["paddle_size"][1] / 2, 
        50 + config["game"]["paddle_size"][0], 
        window_height / 2 + config["game"]["paddle_size"][1] / 2, 
        fill=config["colors"]["left_paddle"])

    if mode != "ai":
        # Right paddle
        right_paddle = game_canvas.create_rectangle(
            window_width - 50 - config["game"]["paddle_size"][0], 
            window_height / 2 - config["game"]["paddle_size"][1] / 2, 
            window_width - 50, 
            window_height / 2 + config["game"]["paddle_size"][1] / 2, 
            fill=config["colors"]["right_paddle"])
    else:
        # Ai paddle
        right_paddle = game_canvas.create_rectangle(
            window_width - 50 - config["game"]["paddle_size"][0], 
            window_height / 2 - config["game"]["paddle_size"][1] / 2, 
            window_width - 50, 
            window_height / 2 + config["game"]["paddle_size"][1] / 2, 
            fill=config["colors"]["ai_paddle"])

def draw_ball():
    global ball
    # draw the ball at the middle
    ball_radius = config["game"]["ball_radius"]
    ball = game_canvas.create_oval(
        (window_width - ball_radius*2) / 2, 
        (window_height - ball_radius*2) / 2, 
        (window_width + ball_radius*2) / 2, 
        (window_height + ball_radius*2) / 2, 
        fill=config["colors"]["ball"]
    )

def draw_scoreboard():
    global score, sets
    name1 = config["game"]["name1"]
    name2 = config["game"]["name2"]
    bot = config["game"]["bot_name"]

    game_canvas.delete("scoreboard", "sets")

    # Draw the scoreboard at the middle
    game_canvas.create_text(
        window_width / 2, 
        window_height / 2,
        anchor = 'center', 
        text = f"{score[0]}\t", 
        fill = config["colors"]["foreground1"], 
        font = ("Century", 24),
        tags = "scoreboard")
    
    game_canvas.create_text(
        window_width / 2, 
        window_height / 2,
        anchor = 'center', 
        text = f"\t{score[1]}", 
        fill = config["colors"]["foreground1"], 
        font = ("Century", 24),
        tags = "scoreboard")

    # Posición: Esquina superior izquierda (20px desde bordes)
    game_canvas.create_text(
        20, 20,
        anchor='nw',  # Alineación noroeste
        text=f"Sets",
        fill=config["colors"]["foreground1"],
        font=("Century", 18),
        tags="sets") 

    game_canvas.create_text(
        20, 20,
        anchor='nw',  # Alineación noroeste
        text=f"\n{name1} {sets[0]}",
        fill=config["colors"]["left_paddle"],
        font=("Century", 18),
        tags="sets") 

    if game_mode != 0:
        game_canvas.create_text(
        20, 20,
        anchor='nw',  # Alineación noroeste
        text=f"\n\n{name2} {sets[1]}",
        fill=config["colors"]["right_paddle"],
        font=("Century", 18),
        tags="sets") 
    else: 
        game_canvas.create_text(
        20, 20,
        anchor='nw',  # Alineación noroeste
        text=f"\n\n{bot} {sets[1]}",
        fill=config["colors"]["ai_paddle"],
        font=("Century", 18),
        tags="sets") 

def datetime_():
    global date
    # En el game_loop inicial:
    date = game_canvas.create_text(
        window_width - 20, 20,
        anchor='ne',
        text="",
        fill=config["colors"]["foreground1"],
        font=("Consolas", 12))

def update_datetime():
    now = datetime.datetime.now().strftime("%H:%M\n%d/%m/%Y")
    game_canvas.itemconfig(date, text=now)
    root.after(1000, update_datetime)  # Actualizar cada segundo

# ======
# MENU
# ======
def menu():
    game_canvas.delete("all")

    # Decoratives
    decoration()

    # Shadow title
    for i in range(3, 0, -1):
        game_canvas.create_text(
            window_width/2 + i*5, 150 + i*5,
            text="PING PONG",
            fill="#3c3836",
            font=("Impact", 100),
            anchor="center")
    
    # Title 
    game_canvas.create_text(
        window_width/2, 150,
        text="PING PONG",
        fill="#d4be98",
        font=("Impact", 100),
        anchor="center") 

    # button configuration
    y_position = 250
    opciones = [
        ("Two players", twoPlayers),
        ("One player", onePlayer),
        ("Settings", settings),
        ("Exit", root.destroy)
        ]

    for idx, (text, command) in enumerate(opciones):
        per_style = "Red.TButton" if idx == 3 else "TButton"

        button = ttk.Button(
            root,
            text = text,
            command = command,
            style = per_style)

        y_position += 100
        game_canvas.create_window(window_width/2, y_position, window=button)

    game_canvas.pack()

def settings():
    print("Not available yet") 
# ==========
# GAME MODE(s)
# ==========
def twoPlayers():
    global left_paddle, right_paddle, left_paddle_y, right_paddle_y
    global game_mode

    game_mode = 1 # Two players

    # Clear the canvas
    game_canvas.delete("all")

    # Draw the game
    draw_net()
    draw_ball()
    draw_paddles()
    draw_scoreboard()
    datetime_()
    update_datetime()

    # Initial paddle positions 
    left_paddle_y = (window_height - config["game"]["paddle_size"][1]) / 2
    right_paddle_y = (window_height - config["game"]["paddle_size"][1]) / 2

    # connect keydown event to function
    root.bind("<KeyPress>", onKeyDown)
    
    game_loop()
    
def onePlayer():
    global left_paddle_y, right_paddle_y, game_mode

    game_mode = 0 # One player
    
    game_canvas.delete("all")
    
    draw_net()
    draw_paddles("ai")
    draw_ball()
    draw_scoreboard()
    datetime_()
    update_datetime()

    # Initial paddle positions 
    left_paddle_y = (window_height - config["game"]["paddle_size"][1]) / 2
    right_paddle_y = (window_height - config["game"]["paddle_size"][1]) / 2

    # Connect Keydown event to function
    root.bind("<KeyPress>", lambda e: onKeyDown(e, ai_mode=True))

    game_loop()
    start_ai()

# ================
# GAMES LOGIC
# ================

def reset_ball():
    global ball_position, ball_speed

    ball_position = [
        (window_width - 2 * config["game"]["ball_radius"]) / 2,
        (window_height - 2 * config["game"]["ball_radius"]) / 2
        ]
    
    #  Velocidad inicial con direccción aleatoria
    ball_speed = [random.choice([-6.0, 6.0]), random.choice([-3.0, 3.0])] 

    game_canvas.moveto(ball, ball_position[0], ball_position[1])

    # Resetear posición de las paletas
    global left_paddle_y, right_paddle_y
    
    left_paddle_y = (window_height - config["game"]["paddle_size"][1]) / 2
    right_paddle_y = (window_height - config["game"]["paddle_size"][1]) / 2
    
    game_canvas.moveto(left_paddle, 50, left_paddle_y)
    game_canvas.moveto(right_paddle, window_width - 50 - config["game"]["paddle_size"][0], right_paddle_y)
    
def game_loop():
    global ball_position, ball_speed, score

    ball_radius = config["game"]["ball_radius"]
    paddle_width, paddle_height = config["game"]["paddle_size"]

    # Update the position of the ball
    ball_position[0] += ball_speed[0]
    ball_position[1] += ball_speed[1]

    # Ball collision with top and bottom(using diameter)
    if (ball_position[1] <= 0 or 
        ball_position[1] + 2 * ball_radius >= window_height):
        ball_speed[1] *= -1

    # Ball collision with right side
    if ball_position[0] + 2 * ball_radius >= window_width:
        score[0] += 1
        # Number of sets
        if score[0] == config["game"]["set_points"] and score[1] + 2 <= score[0]:
            score = [0, 0]
            sets[0] += 1
            draw_scoreboard()

        elif score[0] > config["game"]["set_points"] and score[1] + 2 <= score[0]:
            score = [0, 0]
            sets[0] += 1
            draw_scoreboard()

        draw_scoreboard()
        reset_ball()
            
    # Ball collision with left
    if ball_position[0] <= 0:
        score[1] += 1
        # Number of sets
        if score[1] == config["game"]["set_points"] and score[0] + 2 <= score[1]:
            score = [10, 0]
            sets[1] += 1
            draw_scoreboard()
        elif score[1] > config["game"]["set_points"] and score[0] + 2 <= score[1]:
            score = [10, 0]
            sets[1] += 1
            draw_scoreboard()

        draw_scoreboard()
        reset_ball()

    if sum(sets) == config["game"]["sets"]:
        menu()
        return

    # Variables for collision detection
    ball_left = ball_position[0]
    ball_right = ball_position[0] + 2 * ball_radius
    ball_top = ball_position[1]
    ball_bottom = ball_position[1] + 2 * ball_radius
    
    # left paddle collision
    paddle_left = 50
    paddle_right = 50 + config["game"]["paddle_size"][0]
    paddle_top = left_paddle_y
    paddle_bottom = left_paddle_y + config["game"]["paddle_size"][1]
    
    if (ball_right >= paddle_left and ball_left <= paddle_right and
        ball_bottom >= paddle_top and ball_top <= paddle_bottom):
        ball_speed[0] *=  -1.05  # Aumento de velocidad progresivo
        ball_speed[1] += ((ball_position[1] + config["game"]["ball_radius"]) - (left_paddle_y + config["game"]["paddle_size"][1]/2)) * 0.05 
        
    # right paddle collision
    paddle_left2 = window_width - 50 - config["game"]["paddle_size"][0]
    paddle_right2 = window_width - 50
    paddle_top2= right_paddle_y
    paddle_bottom2= right_paddle_y + config["game"]["paddle_size"][1] 

    if (ball_right >= paddle_left2 and ball_left <= paddle_right2 and
        ball_bottom >= paddle_top2 and ball_top <= paddle_bottom2):
        ball_speed[0] *= -1.05    
        ball_speed[1] += ((ball_position[1] + config["game"]["ball_radius"]) - (right_paddle_y + config["game"]["paddle_size"][1]/2)) * 0.05

    #game_canvas.move(ball, ball_speed[0], ball_speed[1])
    game_canvas.moveto(ball, ball_position[0], ball_position[1])
    
    # Call the function
    root.after(1000 // config["game"]["fps"], game_loop)

def move_ai():
    global right_paddle_y

    # Central position of the ball
    ball_center_y = ball_position[1] + config["game"]["ball_radius"]

    # Paddle ideal position (centered)
    target_y = ball_center_y - config["game"]["paddle_size"][1] / 2
    
    if right_paddle_y < target_y:
        right_paddle_y += 15
    elif right_paddle_y > target_y:
        right_paddle_y -= 15
    
    game_canvas.moveto(right_paddle,
                       window_width - 50 - config["game"]["paddle_size"][0],
                       right_paddle_y)

def start_ai():
    def ai_task():
        if game_mode == 0 and ball_speed[0] > 0:
            move_ai()
            root.after(config["game"]["ai_reflexes"], ai_task)

        else:
            root.after(15, ai_task)
    
    ai_task()

def return_to_menu():
    game_canvas.delete("all")
    menu()
    
def onKeyDown(e, ai_mode=False):
	# declare use of global variable(s)
    global right_paddle_y, left_paddle_y

    paddle_height = config["game"]["paddle_size"][1]
    speed = 18

	# bind arrow keys to player velocity changes
    if(e.keysym == "w"):
		# start movement up when up arrow is pressed down
        left_paddle_y = max(0, left_paddle_y - speed)
    elif(e.keysym == "s"):
		# start movement down when down arrow is pressed down
        left_paddle_y = min(window_height - paddle_height, left_paddle_y + speed)

	# record current player velocities
    game_canvas.moveto(left_paddle, 50, left_paddle_y)

    if not ai_mode:
        # Second player
        if(e.keysym == "Up"):
            right_paddle_y = max(0, right_paddle_y - speed)
        elif(e.keysym == "Down"):
            right_paddle_y = min(window_height - paddle_height, right_paddle_y + speed)
    
        game_canvas.moveto(right_paddle, window_width - 50 - config["game"]["paddle_size"][0], right_paddle_y)

# =============
# WIDGETS STYLE
# =============
s = ttk.Style()
s.theme_use('clam')

# Base Button style
s.configure("TButton", 
    background = "#3c3836",
    foreground = "#ddc7a1",
    bordercolor = "#7daea3",
    darkcolor = "#7daea3",
    lightcolor = "#a9b665",
    relief = "raised", 
    borderwidth = 3,
    font = "Segoe_UI 28",
    padding=(25, 5, 25, 5))
s.map('TButton', 
    background=[('active', '#504946')],
    foreground=[('active', '#89b482')],
    relief=[('pressed', '!disabled', 'sunken')])

# Special style to exit button
s.configure("Red.TButton", 
    bordercolor = "#ea6962",
    darkcolor = "#ea6962",
    lightcolor = "#e78a4e",)
s.map("Red.TButton",
    foreground = [('active', '#ea6962')],
    relief=[('pressed', '!disabled', 'sunken')])

# Style to back to menu button

menu()

root.mainloop()
