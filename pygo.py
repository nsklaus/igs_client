#!/usr/bin/env python3

import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import re

class App(object):

    def __init__(self):

        self.root = tkinter.Tk()
        self.canvas = Canvas(self.root, width=465, height=570)
        self.canvas.grid()
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind('<Motion>', self.mouse_motion)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('go client')


        self.site_name = StringVar()
        self.site_nubr = 0

        self.mydict = {}

        self.letter_list = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T']

        self.im_goban=PhotoImage(file="images/goban2.png")
        self.im_white=PhotoImage(file="images/white.png")
        self.im_black=PhotoImage(file="images/black.png")
        
        goban_width = (self.im_goban.width())
        goban_height = (self.im_goban.height())
        self.canvas.create_image(goban_width/2,goban_height/2,image=self.im_goban)


        self.label_mouse = ttk.Label(self.root, text=str(self.site_nubr))
        self.label_mouse.place( x = 50, y = goban_height+20)

        self.entry_name = ttk.Entry(self.root, text=self.site_name, width=40)
        self.entry_name.insert(END, '15  83(W): D7')
        self.entry_name.place( x = (goban_width - 300), y = goban_height+20)


        button_enter = ttk.Button(self.root, text='ok')
        button_enter['command'] = self.move_stone
        button_enter.place( x = 160, y = goban_height+60)

        button_rem = ttk.Button(self.root,  text='del')
        button_rem['command'] = self.del_stone
        button_rem.place( x = 260, y = goban_height+60)

        button_key = ttk.Button(self.root,  text='key')
        button_key['command'] = self.get_key
        button_key.place( x = 360, y = goban_height+60)


    def move_stone(self):
        move_coords = self.entry_name.get()
        get_letter = (re.findall(r'([A-Z])',move_coords)[-1])
        get_pos_x  = self.letter_list.index(get_letter)
        get_pos_y  = (re.findall(r'(\d+)',move_coords)[-1])
        get_color  = (re.findall(r'([A-Z])',move_coords)[-2])

        rel_pos_x = 33+(int(get_pos_x)*23)
        rel_pos_y = 469-(int(get_pos_y)*23)

        mykey = get_letter+get_pos_y

        if mykey in self.mydict:
            print("already exists!")
        else:
            if get_color is 'B':
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y,image=self.im_black)
            if get_color is 'W':
                self.mydict[mykey] = self.canvas.create_image(rel_pos_x, rel_pos_y,image=self.im_white)

    def get_key(self):
        print("mydict_len=",len(self.mydict))
        print("mydict=",self.mydict)
        for key in self.mydict:
            print("key=",key, "stuff=",self.mydict[key])


    def del_stone(self):
        move_coords = self.entry_name.get()
        get_letter = (re.findall(r'([A-Z])',move_coords)[-1])
        get_pos_y  = (re.findall(r'(\d+)',move_coords)[-1])
        mykey = get_letter+get_pos_y
        print("result2=",self.mydict[mykey])
        self.canvas.delete(self.mydict[mykey])
        del self.mydict[mykey]
        pass

    def mouse_motion(self, event):
        if event.x >= 32 and event.y >= 32 and event.x <=450 and event.y <=450:
            x, y = event.x, event.y
            res_x = str(self.letter_list[(int(x/23)-1)])
            res_y = str(int((450 - y+8)/23)+1)
            mystring=str( res_x + " x " + res_y )
            self.site_nubr=mystring
            self.label_mouse['text']=self.site_nubr


    def mouse_click(self, event):
        print("clicked at", event.x, "x", event.y)

app = App()
app.root.mainloop()





# # telnet program example
# import socket, select, string, sys
 
# #main function
# if __name__ == "__main__":
     
#     if(len(sys.argv) < 3) :
#         print('Usage : python telnet.py hostname port')
#         sys.exit()
     
#     host = sys.argv[1]
#     port = int(sys.argv[2])
     
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.settimeout(2)
     
#     # connect to remote host
#     try :
#         s.connect((host, port))
#     except :
#         print('Unable to connect')
#         sys.exit()
     
#     print('Connected to remote host')
#     data = s.recv(4096)
#     sys.stdout.write(str(data))
     
    # while 1:
    #     socket_list = [sys.stdin, s]
         
    #     # Get the list sockets which are readable
    #     read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
    #     for sock in read_sockets:
    #         #incoming message from remote server
    #         if sock == s:
    #             data = sock.recv(4096)
    #             if not data :
    #                 print('Connection closed')
    #                 sys.exit()
    #             else :
    #                 #print data
    #                 sys.stdout.write(str(data))
             
            # #user entered a message
            # else :
            #     msg = sys.stdin.readline()
            #     s.send(msg)