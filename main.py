#!/usr/bin/python3
import time
from tkinter import *
from tkinter.font import Font
from modules.player import Player
from modules.networking import networking

root = Tk()
root.title("Gaem") #interesting title
root.geometry("640x640")

font = Font(family="Sans Serif", size=28)

nameInput = Entry()
nameInput.grid_location(320 - nameInput.winfo_height(), 320 - nameInput.winfo_width())
nameInput.pack()

canvas = Canvas(root, width=600, height=600, bg="white")
canvas.pack(padx=20, pady=20)

network = networking()

player = Player()

def update():
    canvas.after(20, update)
    return

update()

root.mainloop()
