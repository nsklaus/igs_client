# igs_client
a go client for igs, made with python, tkinter, ttk  
igs uses telnet and transmit data in clear.  
see igs_commands.txt (more docs on igs protocol will be added later)  
  
status: pre-alpha, work in progress, functionalities so far:  
- able to join igs  
- follow telnet session  
- issue commands  
- observe others games  
- place stones on the UI according to telnet output when observing games  
- place stones on UI with the mouse when playing alone  
- clear board when finished a game (alone or observed ones)  
  
## quickstart
- click 'Online' button
- wait for IGS welcome message and login prompt
- type in your ID (if already registered or else some guest ID)
- after IGS validate your registered ID (with prompt "1 1") type in your password
- issues commands, like: "games" to see a list of active games and then "observe <game number>"

known issues:  
connection dropped after while watching a game, i don't know why yet.  
you can issue command 'ayt' to ask IGS if you're still connected, that should prevent a connection drop from inactivity.  
  
<img src="https://github.com/nsklaus/igs_client/blob/master/screenshot.png?raw=true" width="300" height="200">  <img src="https://github.com/nsklaus/igs_client/blob/master/screenshot2.png?raw=true" width="300" height="200">  

