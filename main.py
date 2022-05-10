#!/usr/bin/python3
from time import time
from tkinter import *
from tkinter.font import Font
from modules.player import Player
from modules.screen import TileMap
from modules.networking import networking

root = Tk()
root.title("Gaem") #interesting title
root.geometry("640x640")

font = Font(family="Sans Serif", size=28)

network = networking()

nameInput = Entry()
nameInput.grid_location(320 - nameInput.winfo_height(), 320 - nameInput.winfo_width())
nameInput.pack()

canvas = Canvas(root, width=600, height=600, bg="white")
canvas.create_rectangle(0, 0, 600, 600, fill="black")

def submitted():
    global nameInput
    global submit

    global network
    global canvas

    val: str = nameInput.get()

    nameInput.pack_forget()
    submit.pack_forget()

    canvas.pack(padx=20, pady=20)
    return

submit = Button(root, text="Submit", command=submitted)
submit.pack()

screen = TileMap(network, 80)
player = Player((40, 40), network, screen)

view: tuple = player.getView()
background: list = screen.getDrawScreen(view)
for column in background:
    for tile in column:
        canvas.create_rectangle(tile[0], tile[1], tile[2], tile[3], fill=tile[4], tags="redraw")

def draw():
    global screen
    global player
    global canvas
    global view
    global background

    canvas.delete("redraw")
    nextView = player.getView()

    if abs(nextView[0] - view[0]) > 0.2\
    or abs(nextView[1] - view[1]) > 0.2:
        view = nextView
        background = screen.getDrawScreen(view)
        for column in background:
            for tile in column:
                canvas.create_rectangle(tile[0], tile[1], tile[2], tile[3], fill=tile[4], tags="redraw")
    return

def update():
    global player
    global canvas

    player.gameTick(time())
    canvas.after(20, update)
    return

update()

root.mainloop()
