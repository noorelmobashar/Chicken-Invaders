from turtle import *
import random
import time

class Egg:
    def __init__(self ,win , y , x ,ship):
        self.body = Turtle()
        win.register_shape("egg.gif")
        win.register_shape("fire.gif")
        self.body.shape("egg.gif")
        self.body.up()
        self.body.setx(x)
        
        

    