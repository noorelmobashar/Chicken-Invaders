from turtle import *
import random
import time
import threading
from chicken import Chicken
import pygame
delay(0)
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(4)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)
sound1 = pygame.mixer.Sound('shootsound.mp3')
sound2 = pygame.mixer.Sound('chickhit.mp3')
sound3 = pygame.mixer.Sound('chickdie.mp3')
sound4 = pygame.mixer.Sound('shipenter.mp3')
class Fighter:

    def __init__(self, win):
        self.score = 0
        self.lives = 2
        self.damage = 50
        self.level = 'bullet.gif'
        self.bullets = []
        self.chicksGrid = []
        self.body = Turtle()
        self.height = win.window_height()
        self.width = win.window_width()
        self.body.penup()
        self.body.speed(0)
        channel4.play(sound4)
        win.register_shape("fighter.gif")
        self.body.shape("fighter.gif")
        self.body.sety(-self.height//2 - 20)
        for i in range(110):
            self.body.sety(self.body.ycor() + 1)
            win.update()
            time.sleep(0.01)
        for i in range(10):
            self.body.sety(self.body.ycor() - 1)
            win.update()
            time.sleep(0.01)
        
        win.register_shape("bullet.gif")
        win.register_shape("bullet2.gif")
        win.register_shape("bullet3.gif")
        win.register_shape("bullet4.gif")
        win.register_shape("bullet5.gif")

    def moveUp(self):
        if self.body.ycor() + 15 < self.height // 2 - 50:
            self.body.sety(self.body.ycor() + 15)

    def moveDown(self):
        if self.body.ycor() - 15 > -self.height // 2 + 50:
            self.body.sety(self.body.ycor() - 15)

    def moveRight(self):
        if self.body.xcor() + 15 < self.width // 2 - 50:
            self.body.setx(self.body.xcor() + 15)

    def moveLeft(self):
        if self.body.xcor() - 15 > -self.width // 2 + 50:
            self.body.setx(self.body.xcor() - 15)
    
    def enableClick(self, win):
        onscreenclick(lambda x,y: self.fireBullet(win))

    def shoot(self, win):
        while True:
            for bullet in self.bullets:
                if bullet.ycor() < self.height//2 + 330:
                    bullet.forward(7)
                else:
                    self.bullets.pop(self.bullets.index(bullet))
                    break
            time.sleep(0.01) 

    def fireBullet(self, win):
        onscreenclick(None)

        bullet = Turtle(shape=self.level)
        bullet.hideturtle()
        bullet.penup()
        bullet.speed(0)
        bullet.left(90)
        bullet.setx(self.body.xcor())
        bullet.sety(self.body.ycor() + 40)
        bullet.showturtle()
        print('fire')
        channel1.play(sound1)
        self.bullets.append(bullet)
        ontimer(lambda: self.enableClick(win), 500)
        
    def checkBullet(self, win):
        while True:
            for i in self.bullets:
                xbul, ybul = i.xcor(), i.ycor()
                for j in self.chicksGrid:
                    x, y, tur = j[0], j[1], j[2]

                    if 50 > xbul - x > -50 and 50 > ybul - y > -50:

                        self.bullets[self.bullets.index(i)].clear()
                        self.bullets[self.bullets.index(i)].hideturtle()
                        del self.bullets[self.bullets.index(i)]

                        tur.health -= self.damage
                        for r in range(8):
                            tur.body.sety(tur.body.ycor()+1)
                            time.sleep(0.001)
                        for r in range(8):
                            tur.body.sety(tur.body.ycor()-1)
                            time.sleep(0.001)
                        if tur.health <= 0:
                            channel3.play(sound3)
                            x = random.randint(1,50)
                            type = 'food' if x > 10 else 'atom'
                            if x < 40:
                                Chicken.shootObject(tur, win, self, dec = False, type=type)
                            self.chicksGrid.remove(j)
                            tur.body.hideturtle()
                            del tur
                        else:
                            channel2.play(sound2)
                        break
            time.sleep(0.01)
    
    def revive(self, win):
        for i in range(len(self.bullets)):
            self.bullets[i].clear()
            self.bullets[i].hideturtle()   
        self.bullets = []     
        if self.lives:
            self.body.shape("fighter.gif")
            self.body.sety(-self.height//2 - 20)
            self.body.setx(0)
            for i in range(110):
                self.body.sety(self.body.ycor() + 1)
                time.sleep(0.01)
            for i in range(10):
                self.body.sety(self.body.ycor() - 1)
                time.sleep(0.01) 
            self.lives -= 1
            self.level = 'bullet.gif'
            self.damage = 50
            win.onkeypress(self.moveRight, "d")
            win.onkeypress(self.moveLeft, "a")
            win.onkeypress(win.bye, "Escape")
            win.onscreenclick(lambda x,y:self.fireBullet(win=win))
        else:
            for i in range(len(self.chicksGrid)):
                self.chicksGrid[i][2].body.clear()
                self.chicksGrid[i][2].body.hideturtle()
            self.chicksGrid.clear()
            self.chicksGrid = []
            self.body.clear()
            self.body.hideturtle()
            text = Turtle()
            text.hideturtle()
            text.pencolor('white')
            text.write("GAME OVER", align="center", font=("Arial", 60, "bold"))