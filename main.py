#!/usr/bin/python3
import time
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

def submitted():
    global nameInput
    global network
    global submit
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

def update():
    canvas.after(20, update)
    return

update()

root.mainloop()
