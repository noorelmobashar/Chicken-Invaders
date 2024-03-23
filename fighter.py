from turtle import *
import random
import time
import threading
from chicken import Chicken
import pygame
delay(0)
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(6)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)
channel5 = pygame.mixer.Channel(4)
channel6 = pygame.mixer.Channel(5)
sound1 = pygame.mixer.Sound('shootsound.mp3')
sound2 = pygame.mixer.Sound('chickhit.mp3')
sound3 = pygame.mixer.Sound('chickdie.mp3')
sound4 = pygame.mixer.Sound('shipenter.mp3')
sound5 = pygame.mixer.Sound('victory.mp3')
sound6 = pygame.mixer.Sound('gameover.mp3')
class Fighter:
    bossdx = 0
    bossdy = 0
    def __init__(self, win):
        self.score = 0
        self.lives = 4
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
            dx = Fighter.bossdx
            dy = Fighter.bossdy
            for i in self.bullets:
                xbul, ybul = i.xcor(), i.ycor()
                for j in self.chicksGrid:
                    x, y, tur = j[0], j[1], j[2]

                    if 50 + dx > xbul - x > -50 - dx and 50 + dy > ybul - y > -50 - dy:

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
                            if Chicken.bossState == False:
                                for i in range(len(Chicken.eggs)):
                                    Chicken.eggs[i].clear()
                                    Chicken.eggs[i].hideturtle()
                                Chicken.eggs = []
                                win.onscreenclick(lambda x,y:None)
                                time.sleep(1)
                                win.onkeypress(None, "d")
                                win.onkeypress(None, "a")
                                channel5.play(sound5)
                                if self.body.xcor() < 0:
                                    for i in range(abs(int(self.body.xcor()))):
                                        self.body.forward(1)
                                        time.sleep(0.01)
                                else:
                                    for i in range(abs(int(self.body.xcor()))):
                                        self.body.back(1)
                                        time.sleep(0.01)
                                self.body.left(90)
                                while self.body.ycor() > -self.height // 2 + 50:
                                    self.body.back(1)
                                    time.sleep(0.06)

                                while self.body.ycor() < -(self.height // 3) + 50:
                                    self.body.forward(1)
                                    time.sleep(0.06)

                                vic = Turtle()
                                vic.hideturtle()
                                vic.pencolor('yellow')
                                vic.write("VICTORY", align='center', font=("Arial", 60, "bold"))  
                                while self.body.ycor() < (self.height // 2) + 100:
                                    self.body.forward(3)
                                    time.sleep(0.01)                         
                        else:
                            channel2.play(sound2)
                        break
            time.sleep(0.01)
    
    def revive(self, win):
        for i in range(len(self.bullets)):
            self.bullets[i].clear()
            self.bullets[i].hideturtle()   
        self.bullets = []     
        if self.lives > 1:
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
            Chicken.bossState = False
            for i in range(len(Chicken.eggs)):
                Chicken.eggs[i].clear()
                Chicken.eggs[i].hideturtle()
            Chicken.eggs = []
            for i in range(len(self.chicksGrid)):
                self.chicksGrid[i][2].body.clear()
                self.chicksGrid[i][2].body.hideturtle()
            self.chicksGrid.clear()
            self.chicksGrid = []
            self.body.clear()
            self.body.hideturtle()
            time.sleep(2)
            channel6.play(sound6)
            time.sleep(2.5)
            text = Turtle()
            text.hideturtle()
            text.pencolor('white')
            text.write("GAME OVER", align="center", font=("Arial", 60, "bold"))