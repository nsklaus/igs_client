#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk

def game():
    root =  Tk()
    canvas = Canvas(root, height=450, width=450)
    canvas.grid()

    goban = PhotoImage( file = "images/goban.png" )
    stone = PhotoImage( file = "images/white.png" )

    goban_width = (goban.width()/2)
    goban_height = (goban.height()/2)
    canvas.create_image(goban_width,goban_height,image=goban)
    canvas.create_image(100,200,image=stone)

    root.mainloop()
game()