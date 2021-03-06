#!/usr/bin/python3
from time import time
from tkinter import *
from tkinter.font import Font
from modules.player import Player
from modules.screen import TileMap
from modules.networking import networking
from modules.constants import *

root = Tk()
root.title("Gaem") #interesting title
root.geometry(f"{SCREENWIDTH}x{SCREENHEIGHT}")

font = Font(family="Sans Serif", size=28)

network: networking
screen: TileMap
player: Player
view: tuple
background: list

frame = Frame(root)
frame.pack(padx=20, pady=20)

nameLabel = Label(frame, text="Input a username:")
nameLabel.pack()
nameInput = Entry(frame)
nameInput.grid_location((SCREENHEIGHT >> 2) - nameInput.winfo_height(), (SCREENWIDTH >> 2) - nameInput.winfo_width())
nameInput.pack()

hostLabel = Label(frame, text="Input the host:")
hostLabel.pack()
hostInput = Entry(frame)
hostInput.pack()

canvas = Canvas(root, width=CANVASWIDTH, height=CANVASHEIGHT, bg="white")
canvas.create_rectangle(0, 0, CANVASWIDTH, CANVASHEIGHT, fill="black")

up: bool = False
left: bool = False
right: bool = False
click: bool = False
clickQueued: bool = False
clickCoords: tuple = (0, 0)
respawnQueued: bool = False

def keyPress(event):
    global up
    global left
    global right
    global respawnQueued
    keyName = event.keysym
    if keyName == "Up" or keyName == "w" or keyName == "W":
        up = True
    elif keyName == "Left" or keyName == "a" or keyName == "A":
        left = True
    elif keyName == "Right" or keyName == "d" or keyName == "D":
        right = True
    elif keyName == "r":
        respawnQueued = True
    return

def keyRelease(event):
    global up
    global left
    global right
    global click
    keyName = event.keysym
    if keyName == "Up" or keyName == "w" or keyName == "W":
        up = False
    elif keyName == "Left" or keyName == "a" or keyName == "A":
        left = False
    elif keyName == "Right" or keyName == "d" or keyName == "D":
        right = False
    return

def clickPress(event):
    global click
    global clickQueued
    global clickCoords
    if event.num == 1:
        click = True
        clickQueued = True
        clickCoords = (event.x, event.y)
    return

def clickRelease(event):
    global click
    if event.num == 1:
        click = False
    return

def mouseMoved(event):
    global click
    global clickCoords
    if click:
        clickCoords = (event.x, event.y)

def submitted():
    global frame
    global nameLabel
    global nameInput
    global hostLabel
    global hostInput
    global submit

    global network
    global canvas
    global root
    global screen
    global player
    global view
    global background

    username: str = nameInput.get()
    host: str = hostInput.get()

    frame.pack_forget()
    nameLabel.pack_forget()
    nameInput.pack_forget()
    hostLabel.pack_forget()
    hostInput.pack_forget()
    submit.pack_forget()

    network = networking(host, username)
    screen = TileMap(network, 80)
    player = Player((40, 40), network, screen)
    view = player.getView(CANVASWIDTH, CANVASHEIGHT)
    background = screen.getDrawScreen(view)

    canvas.pack(padx=20, pady=20)

    for column in background:
        for tile in column:
            canvas.create_rectangle(tile[0], tile[1], tile[2], tile[3], fill=tile[4], tags="redraw")
    canvas.create_rectangle(
        (CANVASWIDTH >> 1) - (player.size[0] >> 1),
        (CANVASHEIGHT >> 1) - (player.size[1] >> 1),
        (CANVASWIDTH >> 1) + (player.size[0] >> 1),
        (CANVASHEIGHT >> 1) + (player.size[1] >> 1),
        fill="black",
        tags="redraw"
    )

    root.bind("<KeyPress>", keyPress)
    root.bind("<KeyRelease>", keyRelease)
    root.bind("<Button>", clickPress)
    root.bind("<ButtonRelease>", clickRelease)
    root.bind("<Motion>", mouseMoved)
    
    update()

    return

submit = Button(frame, text="Submit", command=submitted)
submit.pack()

def draw():
    global screen
    global player
    global canvas
    global view
    global background

    #print("Drawing screen")

    #print("Getting view")
    nextView = player.getView(CANVASWIDTH, CANVASHEIGHT)
    #print("Getting bullets")
    bullets = player.getDrawnBullets(CANVASWIDTH, CANVASHEIGHT)
    #print("Getting players")
    players = player.getDrawnOtherPlayers(CANVASWIDTH, CANVASHEIGHT)
    r = 4

    #print("Drawing map")
    if abs(nextView[0] - view[0]) > 0.2\
    or abs(nextView[1] - view[1]) > 0.2:
        canvas.delete("tiles")
        view = nextView
        background = screen.getDrawScreen(view)
        for column in background:
            for tile in column:
                canvas.create_rectangle(tile[0], tile[1], tile[2], tile[3], fill=tile[4], tags="tiles")
        canvas.create_rectangle(
            (CANVASWIDTH >> 1) - (player.size[0] >> 1),
            (CANVASHEIGHT >> 1) - (player.size[1] >> 1),
            (CANVASWIDTH >> 1) + (player.size[0] >> 1),
            (CANVASHEIGHT >> 1) + (player.size[1] >> 1),
            fill="black",
            tags="tiles"
        )
    
    canvas.delete("redraw")

    #print("Drawing bullets")
    for bullet in bullets:
        canvas.create_oval(bullet[0] - r, bullet[1] - r, bullet[0] + r, bullet[1] + r, fill="black", tags="redraw")

    #print("Drawing players")
    canvas.create_text(
        CANVASWIDTH >> 1,
        (CANVASHEIGHT >> 1) - player.size[1],
        text=f"\n{player.score}",
        justify=CENTER,
        tags="redraw"
    )
    
    #print("Loop?")
    for otherPlayer in players:
        calcedPos = (
            otherPlayer["pos"][0],
            otherPlayer["pos"][1],
            otherPlayer["pos"][0] + player.size[0],
            otherPlayer["pos"][1] + player.size[1]
        )
        canvas.create_rectangle(
            calcedPos[0],
            calcedPos[1],
            calcedPos[2],
            calcedPos[3],
            fill="black",
            tags="redraw"
        )
        #print("Getting data")
        playerName = otherPlayer["name"]
        playerScore = otherPlayer["score"]
        canvas.create_text(
            calcedPos[0] + (player.size[0] >> 1),
            calcedPos[1] - (player.size[1] >> 1),
            text=f"{playerName}\n{playerScore}",
            justify=CENTER,
            tags="redraw"
        )

    return

def update():
    global player
    global canvas
    global up
    global left
    global right
    global click
    global clickQueued
    global clickCoords
    global respawnQueued

    player.gameTick(time(), up, left, right, click or clickQueued, clickCoords, respawnQueued, CANVASWIDTH, CANVASHEIGHT)
    clickQueued = False
    respawnQueued = False
    draw()
    canvas.after(20, update)
    return

root.mainloop()
