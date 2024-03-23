from turtle import *
import random
import time
import pygame
pygame.init()
pygame.mixer.set_num_channels(10)
delay(0)
class Chicken:
    eggs = []
    score = 0
    f = False
    turtle_score = None
    def __init__(self, win):
        self.health = 300
        self.body = Turtle()
        self.body.hideturtle()
        self.body.penup()
        self.body.speed(0)
        win.register_shape("chick.gif")
        win.register_shape("fire.gif")
        win.register_shape("eggafter.gif")
        self.body.shape("chick.gif")
        self.height = win.window_height()
        self.width = win.window_width()
        self.body.setx(-self.width//2 - 25)
        self.body.sety(self.height//2 - 50)
        if not Chicken.f:
            Chicken.turtle_score = self.current_score()
            Chicken.f = True

    def makeChicksGrid(width, height, win):

        grid = []
        for row in range(-width//2 + 110, width//2 - 90, 110):
            for column in range(height//2 - 90, -height//7, -80):
                chick = Chicken(win)
                chick.body.goto(row, column)
                time.sleep(0.01)
                grid.append([row, column, chick])
        
        for i in grid:i[2].body.showturtle()
        
        return grid
    
    def shootObject(self, win, ship, dec = True, type = 'egg'):
        while True:
            
            
            if dec:
                time.sleep(1.7)
                rnd = random.randint(0, len(ship.chicksGrid) - 1)
                Chicken.makeObject(win, ship.chicksGrid[rnd][1], ship.chicksGrid[rnd][0], type)
            else:
                Chicken.makeObject(win, self.body.ycor(), self.body.xcor(), type)
                break
            
    def moveEggs(self ,ship, win):
        while True:
            for i in range(len(self.eggs)):
                if self.eggs[i].ycor() > -self.height//2 + 50:
                    self.eggs[i].back(2)
                    x = self.eggs[i].xcor()
                    y = self.eggs[i].ycor()
                    if 40 > x - ship.body.xcor() > -40 and 40 > y - ship.body.ycor() > -40:
                        if self.eggs[i].shape() == "egg.gif":
                            win.onscreenclick(lambda x,y:None)
                            ship.body.shape("fire.gif")
                            pygame.mixer.music.load('explosion.mp3')
                            pygame.mixer.music.play()
                            win.onkeypress(None, "d")
                            win.onkeypress(None, "a")
                            
                            for i in range(len(self.eggs)):
                                self.eggs[i].clear()
                                self.eggs[i].hideturtle()
                            Chicken.eggs = []
                            ontimer(lambda: ship.revive(win),1000)
                        elif self.eggs[i].shape() == "food.gif":
                            pygame.mixer.music.load('crunch.mp3')
                            pygame.mixer.music.play()
                            self.score += 10
                            self.turtle_score.undo()
                            self.turtle_score.write(f"Current Score : {self.score}" ,align= "left" ,font =("Arial" , 20 , "bold"))
                            self.eggs[i].clear()
                            self.eggs[i].hideturtle()
                            del self.eggs[i]
                        else:
                            pygame.mixer.music.load('levelup.mp3')
                            pygame.mixer.music.play()
                            if ship.level == 'bullet.gif':
                                ship.level = 'bullet2.gif'
                                ship.damage = 100
                            elif ship.level == 'bullet2.gif':
                                ship.level = 'bullet3.gif'
                                ship.damage = 150
                            elif ship.level == 'bullet3.gif':
                                ship.level = 'bullet4.gif'
                                ship.damage = 200
                            else:
                                ship.level = 'bullet5.gif'
                                ship.damage = 350
                            self.eggs[i].clear()
                            self.eggs[i].hideturtle()
                            del self.eggs[i]
                            pass
                        break
                        
                else:
                    self.eggs[i].clear()
                    self.eggs[i].hideturtle()
                    del self.eggs[i]
                    break
            time.sleep(0.01) 
    
    def makeObject(win, y, x, type = 'egg'):
        egg = Turtle()
        egg.hideturtle()
        egg.speed(0)
        win.register_shape("egg.gif")
        win.register_shape("food.gif")
        win.register_shape("atom.gif")
        if type == 'egg':
            egg.shape("egg.gif")

        elif type == 'food':
            egg.shape("food.gif")
        else:
            egg.shape("atom.gif")
        egg.up()
        egg.setx(x)
        egg.sety(y-25)
        egg.showturtle()
        egg.left(90)
        Chicken.eggs.append(egg)
    
    def current_score(self):
        t = Turtle()
        t.hideturtle()
        t.up()
        t.pencolor("white")
        t.sety(self.height//2 -50)
        t.setx(-self.width//2 +50)
        t.write(f"Current Score : {self.score}" ,align= "left" ,font =("Arial" , 20 , "bold"))
        return t