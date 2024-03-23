from turtle import *
import random
import time
import pygame
import threading
import fighter
pygame.init()
pygame.mixer.set_num_channels(4)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)
sound1 = pygame.mixer.Sound('explosion.mp3')
sound2 = pygame.mixer.Sound('crunch.mp3')
sound3 = pygame.mixer.Sound('levelup.mp3')
sound4 = pygame.mixer.Sound('siren.mp3')
delay(0)

class Chicken:
    eggs = []
    score = 0
    f = False
    turtle_score = None
    bossState = True

    def __init__(self, win):
        self.health = 300
        self.body = Turtle()
        self.body.hideturtle()
        self.body.penup()
        self.body.speed(0)
        win.register_shape("chick.gif")
        win.register_shape("bigone.gif")
        win.register_shape("bigoneleft.gif")
        win.register_shape("bigoneright.gif")
        win.register_shape("fire.gif")
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
        for row in range(-width//2 + 110, width//2 - 90, 100):
            for column in range(height//2 - 90, -height//7, -120):
                chick = Chicken(win)
                chick.body.goto(row, column)
                time.sleep(0.01)
                grid.append([row, column, chick])
        
        for i in grid:i[2].body.showturtle()
        
        return grid
    
    def shootObject(self, win, ship, dec = True, type = 'egg'):
        while True:
            if Chicken.bossState and len(ship.chicksGrid) == 0:
                threading.Thread(target=lambda:self.finalBoss(win, ship)).start()
                Chicken.bossState = False            
            
            if dec:
                time.sleep(1.7)
                rnd = random.randint(0, max(0,len(ship.chicksGrid) - 1))
                if ship.chicksGrid:
                    Chicken.makeObject(win, ship.chicksGrid[rnd][1], ship.chicksGrid[rnd][0], type)
                    if not Chicken.bossState:
                        Chicken.makeObject(win, ship.chicksGrid[rnd][1], ship.chicksGrid[rnd][0], type, 30, 10)
                        Chicken.makeObject(win, ship.chicksGrid[rnd][1], ship.chicksGrid[rnd][0], type, -30, 10)
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
                    if 40  > x - ship.body.xcor() > -40  and 40  > y - ship.body.ycor() > -40:
                        if self.eggs[i].shape() == "egg.gif":
                            win.onscreenclick(lambda x,y:None)
                            ship.body.shape("fire.gif")
                            channel1.play(sound1)
                            win.onkeypress(None, "d")
                            win.onkeypress(None, "a")
                            
                            for i in range(len(self.eggs)):
                                self.eggs[i].clear()
                                self.eggs[i].hideturtle()
                            Chicken.eggs = []
                            ontimer(lambda: ship.revive(win),1000)
                        elif self.eggs[i].shape() == "food.gif":
                            channel2.play(sound2)
                            self.score += 10
                            self.turtle_score.undo()
                            self.turtle_score.write(f"Current Score : {self.score}" ,align= "left" ,font =("Arial" , 20 , "bold"))
                            self.eggs[i].clear()
                            self.eggs[i].hideturtle()
                            del self.eggs[i]
                        else:
                            channel3.play(sound3)
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
    
    def makeObject(win, y, x, type = 'egg', dx = 0,dy = 0):
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
        egg.setx(x + dx)
        egg.sety(y-25+dy)
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

    def finalBoss(self, win, ship):
        fighter.Fighter.bossdx = 80
        fighter.Fighter.bossdy = 80
        win.onscreenclick(lambda x,y:None)
        channel4.play(sound4)    
        boss = Chicken(win)
        boss.body.shape('bigone.gif')
        boss.body.right(90)
        boss.body.setx(0)
        boss.body.sety(boss.height//2 + 150)
        boss.health = 5000
        boss.body.showturtle()
        while boss.body.ycor() > 100:
            boss.body.forward(1)
            time.sleep(0.01)
        ship.chicksGrid.append([boss.body.xcor(),boss.body.ycor(),boss])
        boss.body.left(90)
        boss.body.shape('bigoneright.gif')
        win.onscreenclick(lambda x,y:ship.fireBullet(win=win))
        while boss.body.xcor() < self.width // 2 - 250:
            boss.body.forward(3)
            ship.chicksGrid[0][0] = boss.body.xcor()
            ship.chicksGrid[0][1] = boss.body.ycor()
            time.sleep(0.01)
        
        self.moveBoss(boss, ship)
    
    def moveBoss(self, boss, ship):
        while True:
            boss.body.shape('bigone.gif')
            time.sleep(3)
            boss.body.left(180)
            if boss.body.xcor() > 0:
                boss.body.shape('bigoneleft.gif')
            else:
                boss.body.shape('bigoneright.gif')
            tmp = boss.body.xcor()
            while (boss.body.xcor() < (self.width // 2 - 250)) if  tmp < 0 else (boss.body.xcor() > (-self.width // 2 + 250)):
                ship.chicksGrid[0][0] = boss.body.xcor()
                ship.chicksGrid[0][1] = boss.body.ycor()
                boss.body.forward(3)
                time.sleep(0.01)
            time.sleep(0.01)