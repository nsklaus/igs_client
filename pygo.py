#!/usr/bin/env python3

import tkinter
from tkinter import *
from tkinter import ttk
import telnetlib
import re


class App(object):

    def __init__(self):
        self.root = tkinter.Tk()
        self.canvas = Canvas(self.root, width=1120, height=540)
        self.canvas.grid()
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind('<Motion>', self.mouse_motion)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('go client')
        self.HOST = "igs.joyjoy.net"
        self.PORT = 7777
        self.tn = telnetlib.Telnet(self.HOST, self.PORT)

        self.last_x = 0
        self.last_y = 0
        self.res_x = 0
        self.res_y = 0
        self.my_coords = []
        self.my_color = []
        self.observe = False
        self.turn = True

        self.site_name = StringVar()
        self.site_nubr = 0

        self.mydict = {}

        self.letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

        self.im_goban = PhotoImage(file="images/goban2.png")
        self.im_white = PhotoImage(file="images/white.png")
        self.im_black = PhotoImage(file="images/black.png")

        goban_width = (self.im_goban.width())
        goban_height = (self.im_goban.height())
        self.canvas.create_image(goban_width / 2, goban_height / 2, image=self.im_goban)
        # self.canvas.pack()

        self.label_mouse = ttk.Label(self.root, text=str(self.site_nubr))
        self.label_mouse.place(x=50, y=goban_height + 20)
        # self.label_mouse.pack()

        self.text1 = Text(self.root, height=30, width=80)
        self.text1.place(x=(goban_width + 5), y=0)
        # self.text1.pack()

        self.entry_name = ttk.Entry(self.root, text=self.site_name, width=90)
        self.entry_name.place(x=470, y=goban_height + 35)
        self.entry_name.bind('<Return>', self.input_igs)
        # self.entry_name.pack()

        button_enter = ttk.Button(self.root, text='ok')
        button_enter['command'] = self.input_igs
        button_enter.place(x=160, y=goban_height + 25)
        # button_enter.pack()

        button_rem = ttk.Button(self.root, text='clean')
        button_rem['command'] = self.clean_board
        button_rem.place(x=260, y=goban_height + 25)
        # button_rem.pack()

        button_key = ttk.Button(self.root, text='key')
        button_key['command'] = self.get_key
        button_key.place(x=360, y=goban_height + 25)
        # button_key.pack()
        self.input_igs()

    def read_igs(self):
        my_buffer = self.tn.read_very_eager().decode('ascii')
        if not my_buffer:
            pass
        else:
            self.text1.insert(INSERT, my_buffer)
            self.text1.see("end")

            if self.observe:
                # TODO: make it a true list, not fixed to [0], then loop on the list to treat captures
                my_coords = re.findall(r'(?<=\([B-W]\):.).\d+', my_buffer)  # find coords
                my_color = re.findall(r'([BW])', my_buffer)  # find color
                if not my_color or not my_coords:
                    pass
                else:
                    self.put_stone(my_color[0], my_coords[0])
        self.root.after(2000, self.read_igs)

    def input_igs(self, event=None):
        self.tn.write(self.entry_name.get().encode('ascii') + b"\n")
        if "observe" in self.entry_name.get():
            self.observe = True
        self.text1.see("end")
        self.entry_name.delete(0, 'end')

    def get_key(self):
        print("mydict_len=", len(self.mydict))
        print("mydict=", self.mydict)
        for key in self.mydict:
            print("key=", key, "stuff=", self.mydict[key])

    def clean_board(self):
        for stone in list(self.mydict.keys()):
            get_letter = (re.findall(r'([A-Z])', stone)[-1])
            get_pos_y = (re.findall(r'(\d+)', stone)[-1])
            mykey = get_letter + get_pos_y
            self.canvas.delete(self.mydict[mykey])
            del self.mydict[mykey]
        self.mydict.clear()

    def put_stone(self, color, coords):
        # move_coords = self.entry_name.get()
        get_letter = (re.findall(r'([A-Z])', coords)[-1])
        get_pos_y = (re.findall(r'(\d+)', coords)[-1])
        mykey = get_letter + get_pos_y
        res_x = int(self.letter_list.index(get_letter)) * 23 + 32
        res_y = 32 + ((19 - int(get_pos_y)) * 23)   # (32 + (int(get_pos_y) * 23))
        if mykey in self.mydict:
            print("already exists!")
        else:
            if color is 'B':
                self.mydict[mykey] = self.canvas.create_image(res_x, res_y, image=self.im_black)
            else:
                self.mydict[mykey] = self.canvas.create_image(res_x, res_y, image=self.im_white)

    def mouse_motion(self, event):
        if event.x >= 32 and event.y >= 32 and event.x <= 450 and event.y <= 450:
            x, y = event.x, event.y
            res_x = str(self.letter_list[(int(x / 23) - 1)])
            res_y = str(int((450 - y + 8) / 23) + 1)
            self.res_x = res_x
            self.res_y = res_y
            mystring = str(res_x + " x " + res_y)
            self.site_nubr = mystring
            self.label_mouse['text'] = self.site_nubr
            self.last_x = res_x
            self.last_y = res_y

    def mouse_click(self, event):
        # print("clicked --> pixel=[{}] go=[{}]".format(str(event.x) + "x" + str(event.y), self.last_x + self.last_y))
        get_pos_x = self.letter_list.index(self.last_x)
        get_pos_y = self.last_y
        rel_pos_x = 33 + (int(get_pos_x) * 23)
        rel_pos_y = 469 - (int(get_pos_y) * 23)
        mykey = self.last_x + self.last_y

        self.turn = not self.turn
        if mykey in self.mydict:
            print("already exists!")
        else:
            if self.turn:
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_black)
            else:
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_white)


app = App()
app.root.after(1000, app.read_igs)
app.root.mainloop()

