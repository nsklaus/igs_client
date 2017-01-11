#!/usr/bin/env python3

import tkinter
from tkinter import *
from tkinter import ttk
import os

class App(object):

    def __init__(self):

        self.root = tkinter.Tk()
        self.canvas = Canvas(self.root, width=465, height=570)
        self.canvas.grid()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('go client')
        self.site_name = StringVar()

        self.letter_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']

        self.im_goban=PhotoImage(file="images/goban2.png")
        self.im_white=PhotoImage(file="images/white.png")
        self.im_black=PhotoImage(file="images/black.png")

        goban_width = (self.im_goban.width())
        goban_height = (self.im_goban.height())
        self.canvas.create_image(goban_width/2,goban_height/2,image=self.im_goban)

        self.entry_name = ttk.Entry(self.root, text=self.site_name, width=50)
        self.entry_name.place( x = 50, y = goban_height+20)


        button_enter = ttk.Button(self.root,  text='ok')
        button_enter['command'] = self.move_stone
        button_enter.place( x = 200, y = goban_height+60)

    def move_stone(self):
        move_coords = self.entry_name.get()
        print("coords={}".format(move_coords))
        print(self.letter_list.index(move_coords))
        posx=self.letter_list.index(move_coords)*20
        # stone(color='black',x=15,y=52)
        self.canvas.create_image(posx,100,image=self.im_black)


class stone(object):
    
    def __init__(self,color,x,y):
        self.im_white=PhotoImage(file="images/white.png")
        self.im_black=PhotoImage(file="images/black.png")
        self.canvas.create_image(100,200,image=self.im_black)
        print("C=[{}] x=[{}] y=[{}]".format(color,x,y))






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