from tkinter import *
from tkinter.font import Font

root = Tk()
root.title("Gaem")
root.geometry("640x640")

font = Font(family="Sans Serif", size=28)

canvas = Canvas(root, width=600, height=600, bg="white")
canvas.pack(padx=20, pady=20)

def update():
    canvas.after(20, update)
    return

update()

root.mainloop()
