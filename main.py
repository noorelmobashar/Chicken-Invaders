from turtle import *
import random
import time
from fighter import Fighter
from chicken import Chicken
import threading

def editMove(win):
    onkeypress(ship.moveRight, "d")
    onkeypress(ship.moveLeft, "a")
    onkeypress(win.bye, "Escape")
    onscreenclick(lambda x,y:ship.fireBullet(win=win))
    

win = Screen()
wintk = win.getcanvas().winfo_toplevel()
wintk.attributes('-fullscreen', True)
win.title("Chickens Game")
win.bgpic("background.gif")
#win.tracer(0)
win.listen()
ship = Fighter(win)
win.delay(0)
chicksGrid = Chicken.makeChicksGrid(win.window_width(), win.window_height(), win)
ship.chicksGrid = chicksGrid
thread = threading.Thread(target=lambda: ship.shoot(win))
thread2 = threading.Thread(target=lambda: ship.checkBullet(win))
thread3 = threading.Thread(target=lambda: chicksGrid[0][2].shootObject(win, ship))
thread4 = threading.Thread(target=lambda: chicksGrid[0][2].moveEggs(ship, win))
thread.start()
thread2.start()
thread3.start()
thread4.start()
win.onkeypress(ship.moveRight, "d")
win.onkeypress(ship.moveLeft, "a")
win.onkeypress(win.bye, "Escape")
win.onscreenclick(lambda x,y:ship.fireBullet(win=win))
win.mainloop()


