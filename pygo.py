#!/usr/bin/env python3

import tkinter
from tkinter import *
from tkinter import ttk, scrolledtext as stext
import telnetlib
import time
import re

# TODO: save corrected buffer to be able to replay forward and backward the game
# TODO: label to show player names, rank, captures


class App(object):

    def __init__(self):

        self.root = tkinter.Tk()
        self.canvas = Canvas(self.root, width=485, height=540)

        self.canvas.grid()
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind('<Motion>', self.mouse_motion)
        self.window = tkinter.Toplevel(self.root, width=665, height=480)
        self.window.withdraw()
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
        self.lastmove = ""
        self.status = "Offline"

        self.site_name = StringVar()
        self.site_nubr = 0

        self.mydict = {}

        self.letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

        self.im_goban = PhotoImage(file="images/goban3.png")
        self.im_white = PhotoImage(file="images/white.png")
        self.im_black = PhotoImage(file="images/black.png")
        self.im_lastm = PhotoImage(file="images/last.png")

        goban_width = (self.im_goban.width())
        goban_height = (self.im_goban.height())
        self.canvas.create_image((goban_width / 2) , (goban_height / 2), image=self.im_goban)

        # ============== IGS term window =============
        self.text1 = stext.ScrolledText(self.window, height=23)
        self.text1.place(x=5, y=40)
        # TODO toggle readonly when going offline/online (allow copy/paste/edit only when offline)
        # make self.text1 readonly
        self.text1.bind("<Key>", lambda e: "break")
        self.text1.bind("<Button-1>", lambda e: "break")
        self.text1.bind("<Motion>", lambda e: "break")

        self.entry_name = ttk.Entry(self.window, text=self.site_name, width=90)
        self.entry_name.place(x=5, y=goban_height - 35)
        self.entry_name.bind('<Return>', self.input_igs)

        button_enter = ttk.Button(self.window, text='match', width=8, state='disabled')
        button_enter['command'] = self.input_igs
        button_enter.place(x=5, y=5)

        # ============== main window ==============
        self.button_enter = ttk.Button(self.root, text='Online', width=8)
        self.button_enter['command'] = self.toggle_net
        self.button_enter.place(x=5, y=goban_height + 5)

        button_rem = ttk.Button(self.root, text='clean', width=8)
        button_rem['command'] = self.clean_board
        button_rem.place(x=85, y=goban_height + 5)

        button_key = ttk.Button(self.root, text='settings', state='disabled')
        button_key['command'] = self.get_key
        button_key.place(x=165, y=goban_height + 5)

        button_key = ttk.Button(self.root, text='debug', width=8)
        button_key['command'] = self.get_key
        button_key.place(x=265, y=goban_height + 5)

    def toggle_net(self):
        if self.button_enter["text"] == "Online":
            self.button_enter["text"] = "Offline"
            self.go_online()
        elif self.button_enter["text"] == "Offline":
            self.button_enter["text"] = "Online"
            self.go_offline()

    def go_online(self):
        self.status = "Online"
        self.window.deiconify()
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
        self.window.withdraw()

    def read_igs(self):
        if self.status == "Online":
            my_buffer = self.tn.read_very_eager().decode('ascii')
            if not my_buffer:
                pass
            else:
                self.text1.insert(INSERT, my_buffer)
                self.text1.see("end")

                if self.observe:
                    # TODO: remove observing status over 'adjourned' message in bufffer
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
            if len(self.mydict) > 0:
                self.canvas.delete(self.lastmove)
            if color is 'B':
                self.mydict[mykey] = self.canvas.create_image(res_x, res_y, image=self.im_black)
            else:
                self.mydict[mykey] = self.canvas.create_image(res_x, res_y, image=self.im_white)
            self.lastmove = self.canvas.create_image(res_x, res_y, image=self.im_lastm)

    def mouse_motion(self, event):
        if event.x >= 32 and event.y >= 32 and event.x <= 450 and event.y <= 450:
            x, y = event.x, event.y
            res_x = str(self.letter_list[(int(x / 23) - 1)])
            res_y = str(int((450 - y + 8) / 23) + 1)
            self.res_x = res_x
            self.res_y = res_y
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
            if len(self.mydict) > 0:
                self.canvas.delete(self.lastmove)
            if self.turn:
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_black)
            else:
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_white)
            self.turn = not self.turn

            self.lastmove = self.canvas.create_image(rel_pos_x, rel_pos_y, image=self.im_lastm)


app = App()
app.root.after(1000, app.read_igs)
app.root.mainloop()


