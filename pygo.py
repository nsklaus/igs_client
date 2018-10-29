#!/usr/bin/env python3

import tkinter
from tkinter import *
from tkinter import ttk, scrolledtext as sText
import telnetlib
import time
import re


class App(object):

    def __init__(self):
        self.root = tkinter.Tk()
        # self.frame_main = Frame(self.root, bg="gray")
        # self.frame_main.pack()
        self.canvas = Canvas(self.root, width=1120, height=470)

        self.canvas.grid()
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind('<Motion>', self.mouse_motion)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('go client')
        self.HOST = "igs.joyjoy.net"
        self.PORT = 7777
        self.tn = telnetlib.Telnet()

        self.last_x = 0
        self.last_y = 0
        self.res_x = 0
        self.res_y = 0
        self.my_coords = []
        self.my_color = []
        self.observe = False
        self.turn = True
        self.status = "Offline"

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

        # self.label_mouse = ttk.Label(self.root, text=str(self.site_nubr))
        # self.label_mouse.place(x=1024, y=5)

        # self.text1 = Text(self.root, height=30, width=80)
        # self.text1.place(x=(goban_width + 5), y=0)
        # self.vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.text1.yview)
        # self.vsb.grid(column=1, row=0, sticky='ns')
        # self.text1.configure(yscrollcommand=self.vsb.set)

        # self.textframe = Text(self.root, bd=2, bg='#CEF6EC', relief=RAISED)
        # self.txscroll = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.textframe.yview)
        # self.txscroll.grid(row=0, column=1, sticky='ns')
        # self.textframe.configure(yscroll=self.txscroll.set)
        # self.textframe.grid(row=0, column=0, padx=2, pady=2)

        self.text1 = sText.ScrolledText(self.root, height=23)
        self.text1.place(x=(goban_width + 5), y=55)
        # make self.text1 readonly
        # TODO toggle readonly when going offline/online
        self.text1.bind("<Key>", lambda e: "break")
        self.text1.bind("<Button-1>", lambda e: "break")
        self.text1.bind("<Motion>", lambda e: "break")

        self.entry_name = ttk.Entry(self.root, text=self.site_name, width=90)
        self.entry_name.place(x=470, y=goban_height - 20)
        self.entry_name.bind('<Return>', self.input_igs)

        self.button_enter = ttk.Button(self.root, text='Online', width=8)
        self.button_enter['command'] = self.toggle_net
        self.button_enter.place(x=goban_width + 5, y=10)

        button_enter = ttk.Button(self.root, text='match', width=8, state='disabled')
        button_enter['command'] = self.input_igs
        button_enter.place(x=goban_width + 85, y=10)

        button_rem = ttk.Button(self.root, text='clean', width=8)
        button_rem['command'] = self.clean_board
        button_rem.place(x=goban_width + 165, y=10)

        button_key = ttk.Button(self.root, text='settings', state='disabled')
        button_key['command'] = self.get_key
        button_key.place(x=goban_width + 245, y=10)

        button_key = ttk.Button(self.root, text='debug', width=8)
        button_key['command'] = self.get_key
        button_key.place(x=goban_width + 345, y=10)

    def toggle_net(self):
        if self.button_enter["text"] == "Online":
            self.button_enter["text"] = "Offline"
            self.go_online()
        elif self.button_enter["text"] == "Offline":
            self.button_enter["text"] = "Online"
            self.go_offline()

    def go_online(self):
        self.status = "Online"
        self.text1.insert(INSERT, "\n" + " === Connecting to IGS ===" + "\n\n")
        self.tn = telnetlib.Telnet(self.HOST, self.PORT)
        self.read_igs()
        self.input_igs()

    def go_offline(self):
        self.status = "Offline"
        try:
            self.tn.write(b"exit" + b"\n")
            time.sleep(1)
            self.text1.insert(INSERT, "\n\n" + " === IGS connection terminated ===" + "\n")
        except EOFError as e:
            self.text1.insert(INSERT, str(e))
        self.text1.see("end")

    def read_igs(self):
        if self.status == "Online":
            my_buffer = self.tn.read_very_eager().decode('ascii')
            if not my_buffer:
                pass
            else:
                self.text1.insert(INSERT, my_buffer)
                self.text1.see("end")

                if self.observe:
                    # TODO: when starting to observe, loop first through previous moves (moves <game_id>)
                    my_coords = re.findall(r'(?<=\([B-W]\):.).*', my_buffer)  # find coords
                    my_color = re.findall(r'([BW])', my_buffer)  # find color

                    if not my_color and not my_coords:
                        pass
                    # TODO: Handle Handicap string: "15   0(B): Handicap 2"
                    else:  # if "Handicap" not in my_coords[0]:
                        my_temp = re.sub(r'\r', '', my_coords[0])
                        my_temp = my_temp.split( )
                        my_move = my_temp[0]
                        del my_temp[0]
                        if len(my_temp) > 0:
                            self.del_stone(my_temp)
                            pass
                        self.put_stone(my_color[0], my_move)
            self.root.after(2000, self.read_igs)

    def input_igs(self, event=None):
        if self.status == "Online":
            self.tn.write(self.entry_name.get().encode('ascii') + b"\n")
            self.text1.insert(INSERT, self.entry_name.get().encode('ascii') + b"\n")
            if "observe" in self.entry_name.get():
                self.observe = True
            self.text1.see("end")
            self.entry_name.delete(0, 'end')

    def get_key(self):
        print("mydict_len=", len(self.mydict))
        print("mydict=", self.mydict)
        for key in self.mydict:
            print("key=", key, "stuff=", self.mydict[key], "type= ", type(self.mydict[key]))

    def clean_board(self):
        for stone in list(self.mydict.keys()):
            get_letter = (re.findall(r'([A-Z])', stone)[-1])
            get_pos_y = (re.findall(r'(\d+)', stone)[-1])
            mykey = get_letter + get_pos_y
            self.canvas.delete(self.mydict[mykey])
            del self.mydict[mykey]
        self.mydict.clear()

    def del_stone(self, coords):
        for stone in coords:
            self.canvas.delete(self.mydict[stone])
            del self.mydict[stone]

    def put_stone(self, color, coords):
        get_letter = re.sub('[^A-Za-z]', '', coords)
        get_pos_y = re.sub('[^0-9]', '', coords)
        mykey = get_letter + get_pos_y
        res_x = int(self.letter_list.index(get_letter)) * 23 + 32  # letter_index * offset + bordersize
        res_y = 32 + ((19 - int(get_pos_y)) * 23)  # bordersize + (boardsize - letter) * offset
        if mykey in self.mydict:
            print("already exists!")
            # self.del_stone(mykey)
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
            # mystring = str(res_x + " x " + res_y)
            # self.site_nubr = mystring
            # # self.label_mouse['text'] = self.site_nubr
            self.last_x = res_x
            self.last_y = res_y

    def mouse_click(self, event):
        get_pos_x = self.letter_list.index(self.last_x)
        get_pos_y = self.last_y
        rel_pos_x = 33 + (int(get_pos_x) * 23)
        rel_pos_y = 469 - (int(get_pos_y) * 23)
        mykey = self.last_x + self.last_y

        if mykey in self.mydict:
            temp_list = [mykey]
            self.del_stone(temp_list)
        else:
            if self.turn:
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_black)
            else:
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_white)
            self.turn = not self.turn


app = App()
app.root.after(1000, app.read_igs)
app.root.mainloop()


