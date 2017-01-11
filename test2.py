#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk

def game():
    root =  Tk()
    root.geometry("450x450")

    goban = PhotoImage( file = "images/goban.png" )
    stone = PhotoImage( file = "images/white.png" )

    label_go = Label(root, image=goban)
    label_go.place( x = 0, y = 0)

    white = Label(root, image = stone)
    white.place( x = 100, y = 200 )

    root.mainloop()
game()