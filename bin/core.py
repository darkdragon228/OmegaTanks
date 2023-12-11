import sys
import random
import time
import copy
import json
import os
from bin.QtResource import *
from screeninfo import get_monitors
import pygame
pygame.init()
pygame.mixer.init(44100, 32, 1, 2048)

sound1 = pygame.mixer.Sound("bin/sounds/fa1.wav")

DEFAULT_COLOR = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 51)
BlUE = (0, 0, 255)
ORANGE = (255, 123, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (0, 255, 255)

for m in get_monitors():
    Wwidth = m.width
    Wheight = m.height

win_ = None
clock = pygame.time.Clock()

Map = []
enemy_list = []

playerScale = 0

globalLocation = 0

layer = 0

EditorLine = False

def core_init():
    global win_
    win_ = pygame.display.set_mode((Wwidth, Wheight))

def buildProcessor(list, size=0, xcor=0, ycor=0, addMap = True):
    #перша Фаза
    global playerScale
    playerScale = size

    buffer = []
    enemy_buffer = []
    x = xcor
    y = ycor
    for i in list["1"]:

        if i == 1:
            buf = 0
            buf = Game(x, y, 64, 64, RED,
                       0, "bin/sprites/floor1.png", "floor1")

            if size != 0:
                buf.scale(64-size, 64-size)

            buffer.append(buf)
            x += 64-size
        elif i == "S":
            buf = 0
            buf = Game(x, y, 64, 64, RED,
                       0, "bin/sprites/floor1.png", "spawn")

            if size != 0:
                buf.scale(64-size, 64-size)

            buffer.append(buf)
            x += 64-size
        elif i == 0:
            x = xcor
            y += 64-size
        else:
            x += 64-size
    #друга Фаза
    x = xcor
    y = ycor
    for i in list["2"]:

        if i == 1:
            x += 64-size
        elif i == 2:
            buf = Wall(x, y, 64, 64, BLACK,
                       0, "bin/sprites/wall1.png", "wall", None, 1, 3)

            if size != 0:
                buf.scale(64-size, 64-size)

            buffer.append(buf)
            x += 64-size
#----------------------------------------
        elif i == 3:
            buf = Wall(x, y, 64, 64, BLACK,
                       0, "bin/sprites/wall2.png", "UltraWall")

            if size != 0:
                buf.scale(64-size, 64-size)

            buffer.append(buf)
            x += 64-size
#---------------------------------------
        elif i == "e":
            buf = EnemyAI(x, y, 64, 64, BLACK,
                       0, "bin/sprites/enemy_tank.png", "enemy")

            if size != 0:
                buf.scale(64-size, 64-size)

            enemy_buffer.append(buf)
            x += 64-size
#----------------------------------------
        elif i == 0:
            x = xcor
            y += 64-size 
#------------------------------------------
        elif i == "F":
            buf = Finish(x, y, 64, 64, BLACK,
                       0, "bin/sprites/finish.png", "finish")

            if size != 0:
                buf.scale(64-size, 64-size)

            buffer.append(buf)
            x += 64-size             
#----------------------------------------
        elif type(i) == type([]):
#----------------------------------------
            if i[0] == "GTa":
                buf = GlobalTelepot(x, y, 64, 64, BlUE,
                    0, None, "GTa", None, 1, i[1], i[2])

                if size != 0:
                    buf.scale(64-size, 64-size)

                buffer.append(buf)
                x += 64-size
#---------------------------------------        
            elif i[0] == "GTb":
                buf = GlobalTelepot(x, y, 64, 64, RED,
                    0, None, "GTb", None, 1, i[1], i[2])

                if size != 0:
                    buf.scale(64-size, 64-size)

                buffer.append(buf)
                x += 64-size
#----------------------------------------
            elif i[0] == "door":
                buf = Door(x, y, 64, 64, RED,
                    0, None, "door", ["bin/sprites/Cdoor.png", "bin/sprites/Odoor.png"], 1, 1, i[1], i[2])

                if size != 0:
                    buf.scale(64-size, 64-size)
                
                if i[3]:
                    buf.rotate = 90

                buffer.append(buf)
                x += 64-size
#------------------------------------------------            
            elif i[0] == "TrigB":
                buf = TrigerButton(x, y, 64, 64, RED,
                    0, None, "TrigB", ["bin/sprites/TButtonC.png", "bin/sprites/TButtonO.png"], 1, i[1], i[2])

                if size != 0:
                    buf.scale(64-size, 64-size)

                buffer.append(buf)
                x += 64-size
#--------------------------------------
            elif i[0] == "boss":
                buf = Boss(x, y, size, LIGHT_BLUE)
            
                buffer.append(buf)
                x += 64-size
#--------------------------------------
        else:
            x += 64-size 
        
    global Map
    global enemy_list

    if addMap:
        Map.append(buffer)
        enemy_list.append(enemy_buffer)

    return enemy_buffer, buffer

def ReadMap(json_):
    buffer = None
    with open(json_) as map:
        buffer = json.load(map)

        map.close()
    
    for i in buffer:
        buildProcessor(buffer[i])
    StartGame()

class Game():
    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1):

        self.rect = pygame.Rect(x, y, x_size, y_size)
        self.thickness = thickness
        self.color = color
        self.win = win_
        self.cadr = 0

        self.rotate = 0
        self.rotate_ = 0

        self.scale_sizeX = 0
        self.scale_sizeY = 0
        
        if sprite != None:
            self.img = pygame.image.load(sprite)
            self.img_reserve = pygame.image.load(sprite)
        else:
            self.img = None
            self.img_reserve = None

        self.ID = ID

        if animation != None:
            self.animation = []
            self.animation_reserve = []
            for i in animation:
                self.animation.append(pygame.image.load(i))
                self.animation_reserve.append(pygame.image.load(i))
        else:
            self.animation = None

        self.animation_status = True
        self.time = [anim_time]
        self.logic_time = [0]
        self.text = [None, 0, 0, 0, 0]
        self.sprite = sprite
        self.animation_ = animation

        self.auto_animation = True # чи буде анімація автоматична
        self.drawRect = False # чи пуде малюватися хідбокс

    def draw(self, hitbox_draw=False):
        if hitbox_draw or self.drawRect:
            pygame.draw.rect(win_, self.color, self.rect, self.thickness)

        if self.img:
            if self.rotate != 0:
                self.img = copy.copy(self.img_reserve)
                self.img = pygame.transform.rotozoom(self.img, self.rotate, 1)
            elif self.rotate == 0:
                self.img = copy.copy(self.img_reserve)
                self.rotate = 0

            if self.scale_sizeX != 0 or self.scale_sizeY != 0:
                self.img = pygame.transform.scale(
                    self.img, (self.scale_sizeX, self.scale_sizeY))

            win_.blit(self.img, (self.rect.x, self.rect.y))

        if self.animation:
            if self.rotate_ != self.rotate:
                self.animation = []

                self.animation = copy.copy(self.animation_reserve)

                for i in range(len(self.animation)):
                    self.animation[i] = pygame.transform.rotozoom(
                        self.animation[i], self.rotate, 1)
                self.rotate_ = self.rotate

            win_.blit(self.animation[self.cadr],
                      (self.rect.x, self.rect.y))

            if self.auto_animation:
                self.nextCadr()

        if self.text[0] != None:
            win_.blit(pygame.font.Font(None, self.text[0]).render(self.text[3], True, self.text[4]),
                      (self.rect.x + self.text[1], self.rect.y + self.text[2]))

    def nextCadr(self):
        if time.time() - self.logic_time[0] > self.time[0] and self.animation_status:
            if self.cadr >= len(self.animation) - 1:
                self.cadr = 0
            else:
                self.cadr += 1
            self.logic_time[0] = time.time()

    def set_text(self, text, x, y, size, color=(0, 0, 0)):
        self.text[0] = size
        self.text[1] = x
        self.text[2] = y
        self.text[3] = text
        self.text[4] = color

    def scale(self, sizeX, sizeY):
        self.rect.width = sizeX
        self.rect.height = sizeY

        self.scale_sizeX = sizeX
        self.scale_sizeY = sizeY

        if self.animation != None:
            for i in range(len(self.animation)):
                self.animation[i] = pygame.transform.scale(
                    self.animation[i], (self.scale_sizeX, self.scale_sizeY))

    def rotate_f(self, r):
        self.rotate = r


class Interface():

    def __init__(self):
        self.widgets = []
        self.status = True

    def add_button(self, x, y, size_x, size_y, sprite, fun, arg=None, text=None, tx=0, ty=0, tsize=50):
        buf = Button(x, y, size_x, size_y, RED, 0, sprite, "button", None, 1, fun, arg)
        if text != None:
            buf.set_text(text, tx, ty, tsize)
        self.widgets.append(buf)
    
    def add_label(self, x, y, text, tsize):
        buf = Game(x, y, 1, 1, DEFAULT_COLOR, 0, None, "label")
        buf.set_text(text, 0, 0, tsize)
        self.widgets.append(buf)
    
    def add_preview(self, x, y, json_, size):
        with open(json_) as m:
            buffer = json.load(m)
            map = buffer["location-1"]
        a, buf = buildProcessor(map, size, x, y, False)
        self.widgets.append(buf)

    def add_frame(self, x, y, xsize, ysize):
        buf = Game(x, y, xsize, ysize, BLACK)
        buf.drawRect = True
        self.widgets.append(buf)

        buf = Game(x+10, y+10, xsize-20, ysize-20, (150, 150, 150))
        buf.drawRect = True
        self.widgets.append(buf)

    def start(self):
        self.status = True

        while self.status:
            win_.fill(LIGHT_BLUE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in self.widgets:
                        if type(i) != type([]):
                            if i.ID == "button":
                                i.check()
            
            for i in self.widgets:
                if type(i) == type([]):
                    for s in i:
                        s.draw()
                else:
                    i.draw()

            pygame.display.update()
            clock.tick(60)
    
    def exit(self):
        self.status = False


class Button(Game):
    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, function = None, arg = None):
        Game.__init__(self, x, y, x_size, y_size, color,
                      thickness, sprite, ID, animation, anim_time)
        self.function = function
        self.arg = None

        if arg != None:
            self.arg = arg

    def check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.arg != None:
                self.function(self.arg)
            else:
                self.function()


class Player(Game):
    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1):
        self.speed = 4
        super().__init__(x, y, x_size, y_size, color,
                         thickness, sprite, ID, animation, anim_time)
        self.was_x = self.rect.x
        self.was_y = self.rect.y
        self.bulletList = []
        self.bulletTime = 0
        self.logicTimeSpeed = time.time()

    def update_control(self):
        self.animation_status = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.was_y = self.rect.y
            self.rect.y -= self.speed
            self.animation_status = True
            self.rotate = 0
        elif keys[pygame.K_s]:
            self.was_y = self.rect.y
            self.rect.y += self.speed
            self.animation_status = True
            self.rotate = 180
        elif keys[pygame.K_a]:
            self.was_x = self.rect.x
            self.rect.x -= self.speed
            self.animation_status = True
            self.rotate = 90
        elif keys[pygame.K_d]:
            self.was_x = self.rect.x
            self.rect.x += self.speed
            self.animation_status = True
            self.rotate = -90
        if keys[pygame.K_q]:
            if time.time() - self.logicTimeSpeed >= 1:
                if self.speed == 4:
                    self.speed = 1
                else:
                    self.speed = 4
                self.logicTimeSpeed = time.time()
        if keys[pygame.K_SPACE]:
            if time.time() - self.bulletTime >= 2:
                self.bulletTime = time.time()
                sound1.play()
                return self.shoot()
    
    def shoot(self):
        vec = [0, 0]
        rot = 0
        cor = []
        size = []

        if self.rotate == 0:
            vec = [0, -5]
            cor = [23, 0]
            size = [3, 11]
        elif self.rotate == 90:
            vec = [-5, 0]
            cor = [0, 23]
            size = [11, 3]
        elif self.rotate == -90:
            vec = [5, 0]
            cor = [0, 23]
            size = [11, 3]
        elif self.rotate == 180:
            vec = [0, 5]
            cor = [23, 0]
            size = [3, 11]

        rot = self.rotate

        return Bullet(self.rect.x + cor[0], self.rect.y + cor[1], size[0], size[1], BLACK, 0, "bin/sprites/bullet.png", "bullet", None, 1, ["wall", "UltraWall", "enemy", "GTa", "door"], vec, rot)


class EnemyAI(Game):
    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, health=1):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)
        self.collidDetect = True
        self.logic_vector = [0, 0]
        self.logic_random = [-1, 1]
        self.ID = ID
        self.health = health
        self.Time = random.randint(3, 5)
        self.logicTime = time.time()
        self.shootTime = random.randint(5, 7)
        self.LogicShootTime = time.time()

    def AIupdate(self):
        if self.collidDetect:
            self.logic_vector = [0, 0]
            if random.randint(0, 1) == 1:
                if random.choice(self.logic_random) == 1:
                    self.logic_vector[0] = 1
                    self.rotate = -90
                else:
                    self.logic_vector[0] = -1
                    self.rotate = 90
            else:
                if random.choice(self.logic_random) == 1:
                    self.logic_vector[1] = -1
                    self.rotate = 0
                else:
                    self.logic_vector[1] = 1
                    self.rotate = 180

            self.collidDetect = False

        if time.time() - self.logicTime >= self.Time:
            self.collidDetect = True

            self.logicTime = time.time()
            self.Time = random.randint(3, 5)
        
        if time.time() - self.LogicShootTime >= self.shootTime:
            self.LogicShootTime = time.time()
            self.shootTime = random.randint(5, 7)
            return self.shoot()

        self.rect.x += self.logic_vector[0]
        self.rect.y += self.logic_vector[1]
    
    def shoot(self):
        vec = [0, 0]
        rot = 0
        cor = []
        size = []

        if self.rotate == 0:
            vec = [0, -5]
            cor = [23, 0]
            size = [3, 11]
        elif self.rotate == 90:
            vec = [-5, 0]
            cor = [0, 23]
            size = [11, 3]
        elif self.rotate == -90:
            vec = [5, 0]
            cor = [0, 23]
            size = [11, 3]
        elif self.rotate == 180:
            vec = [0, 5]
            cor = [23, 0]
            size = [3, 11]

        rot = self.rotate

        return Bullet(self.rect.x + cor[0], self.rect.y + cor[1], size[0], size[1], BLACK, 0, "bin/sprites/bullet.png", "bullet", None, 1, ["wall", "UltraWall", "GTa", "door", "player"], vec, rot)


class Wall(Game):
    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, health=1):
        super().__init__(x, y, x_size, y_size, color,
                         thickness, sprite, ID, animation, anim_time)
        self.health = health

    def update_collision(self, object):
        if self.rect.colliderect(object.rect):

            if object.rotate == 0:
                object.rect.y += self.rect.y + self.rect.height - object.rect.y
            if object.rotate == 180:
                object.rect.y -= object.rect.y + object.rect.height - self.rect.y
            if object.rotate == -90:
                object.rect.x -= object.rect.x + object.rect.width - self.rect.x
            if object.rotate == 90:
                object.rect.x += self.rect.x + self.rect.width - object.rect.x
            
            if object.ID == "enemy":
                object.collidDetect = True
    


class Bullet(Game):
    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, target=None, Vector = [None, None], rotateB = 0):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)
        self.Target = target
        self.Vector = Vector
        self.rotate = rotateB

    def Move(self):
        self.rect.x += self.Vector[0]
        self.rect.y += self.Vector[1]
    
    def update_collision(self, object):
        if self.rect.colliderect(object.rect):
            for i in self.Target:
                if object.ID == i:
                    return True

class GlobalTelepot(Game):

    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, locationCor=None, flow=None):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)

        if flow == None or locationCor == None:
            raise NameError("GT: creatError")

        self.Tflow = flow
        self.locationCor = locationCor
    
    def update_collision(self, object):
        logic = 0
        if self.rect.colliderect(object.rect):
            if object.ID == "player" and self.ID == "GTa":
                logic = GlobalTeleportation(object, self.locationCor, self.Tflow)
            elif object.ID == "enemy":
                if object.rotate == 0:
                    object.rect.y += self.rect.y + self.rect.height - object.rect.y
                if object.rotate == 180:
                    object.rect.y -= object.rect.y + object.rect.height - self.rect.y
                if object.rotate == -90:
                    object.rect.x -= object.rect.x + object.rect.width - self.rect.x
                if object.rotate == 90:
                    object.rect.x += self.rect.x + self.rect.width - object.rect.x
            
                object.collidDetect = True
        if logic:
            return True

class Door(Wall):

    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, health=1, flow = None, status_=True):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time, health)
        self.status = status_
        self.auto_animation = False
        self.TrigerFlow = flow
        if not self.status:
            self.nextCadr()
    
    def DoorUpdate_collision(self, obj):
        if self.status:
            self.update_collision(obj)
    
    def update_status(self):
        if self.status:
            self.status = False
        else:
            self.status = True
        
        self.nextCadr()

class TrigerButton(Game):

    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1, trigetObj = None, trigerFlow = None):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)

        self.TrigerObject = trigetObj
        self.TrigetFlow = trigerFlow
        self.status = True
        self.auto_animation = False
    
    def check_triger(self, obj):
        if self.rect.colliderect(obj.rect) and self.status:
            FireTriger(self.TrigerObject, self.TrigetFlow)
            self.status = False
            self.nextCadr()

class Finish(Wall):

    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)
    
    def check(self, obj):
        if self.rect.colliderect(obj):
            return True

class Boss():

    def __init__(self, x, y, size=0, color=(0, 0, 0)):
        self.sizeX = 128-size*2
        self.sizeY = 192-size*3
        self.ID = "boss"

        self.backrect1 = Game(x, y, self.sizeX, self.sizeY*2, LIGHT_BLUE)

        self.train1 = Wall(x, y, 128, 192, DEFAULT_COLOR, 0, "bin/sprites/train1.png")
        self.train1.scale(self.sizeX, self.sizeY)

        self.train2 = Wall(x, y+self.sizeY, 128, 192, DEFAULT_COLOR, 0, "bin/sprites/train2.png")
        self.train2.scale(self.sizeX, self.sizeY)

        self.logik = 0
    
    def Update(self, player):
        if self.logik <= self.sizeY*2:
            self.train1.rect.y -= 1
            self.train1.update_collision(player)

            self.train2.rect.y -= 1
            self.train2.update_collision(player)

            self.logik += 1
        else:
            self.train1.update_collision(player)
            self.train2.update_collision(player)
    
    def draw(self):
        self.train1.draw()
        self.train2.draw()
        self.backrect1.draw(1)
        
class EditBloc(Game):

    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)

        self.thickness = 3
        self.drawRect = True

        self.code = None

        self.CodeBaseLevel1 = {
            0: "bin/sprites/button2.png",
            1: "bin/sprites/floor1.png"
        }

        self.CodeBaseLevel2 = {
            0: "bin/sprites/button2.png",
        }
    
    def setCode(self, code, level_):
        level = None

        if level_ == 1:
            level = self.CodeBaseLevel1
        elif level_ == 2:
            level = self.CodeBaseLevel2
        
        if not level:
            return
        elif not code in level:
            return
        
        self.img = pygame.image.load(level[code])
        self.img_reserve = pygame.image.load(level[code])

        self.code = code


class BlocksBar():

    def __init__(self, cor, color1, color2):

        self.Rect1 = pygame.Rect(cor, 0, 158, Wheight)
        self.Rect2 = pygame.Rect(cor, 0-5, 158, Wheight+10)
        
        self.color1 = color1
        self.color2 = color2
        self.cor = cor

        self.ListWidgets = []
        self.initedCode = None

    def draw(self):

        pygame.draw.rect(win_, self.color1, self.Rect1)
        pygame.draw.rect(win_, self.color2, self.Rect2, 5)

        for i in self.ListWidgets:
            i.draw()
        
    
    def setCodeButtons(self, ConfigurList: dict):
        x = self.cor + 10
        y = 10

        resizeY = False

        for i in ConfigurList:

            self.ListWidgets.append(Button(x, y, 64, 64, DEFAULT_COLOR, 0, ConfigurList[i], None, None, 1, self.initCode, i))

            if resizeY:
                x -= 76
                y += 76
            else:
                x += 76
            
            resizeY = not resizeY 
    
    def initCode(self, code):
        self.initedCode = code
    
    def checkButtons(self):
        for i in self.ListWidgets:
            i.check()

class CodeBloc(Game):

    def __init__(self, x, y, x_size, y_size, color, thickness=0, sprite=None, ID=None, animation=None, anim_time=1):
        super().__init__(x, y, x_size, y_size, color, thickness, sprite, ID, animation, anim_time)

        self.thickness = 5
        self.drawRect = True
        self.code = "$"
        self.settings = None
        self.ActivCodeDict = {
            "door": QtSetDoorSettings,
            "GTa": QtSetTeleport_A_PointSettings,
            "GTb": QtSetTeleport_B_PointSettings,
            "TrigB": QtSetTrigerFlow
        }
    
    def setCode(self, code, sprite):
        if self.rect.collidepoint(pygame.mouse.get_pos()):

            if code == "set":

                for i in self.ActivCodeDict:

                    if type(self.code) == type([]):
                        if self.code[0] == i:
                            self.code = self.ActivCodeDict[i]()

                    elif self.code == i:
                        self.code = self.ActivCodeDict[i]()
            else:

                self.code = code
                self.img = pygame.image.load(sprite)
                self.img_reserve = pygame.image.load(sprite)


def StartGame():

    game = True

    global Map
    global enemy_list
    global globalLocation

    object = Map
 
    spawn_pos = []

    for i in object[globalLocation]:
        if i.ID == "spawn":
            spawn_pos.append(i.rect.x)
            spawn_pos.append(i.rect.y)
            break

    player = Player(spawn_pos[0], spawn_pos[1], 64, 64, BLACK, 0, "bin/sprites/tank.png", "player", None, 0.05)
    player.scale(64-playerScale, 64-playerScale)

    while game:
        win_.fill(LIGHT_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        bulletBuf = None

        bulletBuf = player.update_control()

        if bulletBuf != None:
            object[globalLocation].append(bulletBuf)

        for i in object[globalLocation]:
            try:

                if i.ID == "wall" or i.ID == "UltraWall":
                    i.update_collision(player)

                    for s in enemy_list[globalLocation]:
                        i.update_collision(s)
                
                elif i.ID == "finish":
                    if i.check(player):
                        game = False
                    
                    for s in enemy_list[globalLocation]:
                        i.update_collision(s)
                
                elif i.ID == "door":
                    i.DoorUpdate_collision(player)

                    for s in enemy_list[globalLocation]:
                        i.DoorUpdate_collision(s)
                
                elif i.ID == "GTa":
                    if i.update_collision(player):
                        break

                    for s in enemy_list[globalLocation]:
                        i.update_collision(s)
                
                elif i.ID == "TrigB":
                    i.check_triger(player)
                
                elif i.ID == "boss":
                    i.Update(player)
               
                elif i.ID == "bullet":
                    i.Move()
                    for s in object[globalLocation]:

                        for b in i.Target:

                            if s.ID == b:

                                if i.update_collision(s):
                                    object[globalLocation].remove(i)
                                    if s.ID != "UltraWall" and s.ID != "door":
                                        s.health -= 1

                                        if s.health <= 0:
                                            object[globalLocation].remove(s)

                                    break
                    for s in i.Target:
                        if s == "player":
                            if i.update_collision(player):
                                game = False

                    for s in enemy_list[globalLocation]:

                        for b in i.Target:

                            if s.ID == b:

                                if i.update_collision(s):

                                    s.health -= 1

                                    if s.health <= 0:
                                        enemy_list[globalLocation].remove(s)

                                    object[globalLocation].remove(i)
                                    break
            except Exception:
                pass
        
        MoveCamera(player, object[globalLocation], enemy_list[globalLocation])
                
        for i in enemy_list[globalLocation]:
            bulletBuf = i.AIupdate()
            if bulletBuf != None:
                object[globalLocation].append(bulletBuf)

        for i in object[globalLocation]:
            i.draw()
        
        for i in enemy_list[globalLocation]:
            i.draw()

        player.draw()
        pygame.display.update()
        clock.tick(60)

    Map.clear()
    enemy_list.clear()
    globalLocation = 0


def MapEditor():
    global Map
    global globalLocation
    #global initedloc
    global EditorLine

    globalLocation = 0
    Path, map = QtMapEditor()

    if map == None:
        return
    
    Xx, Yy = QtSizeWin()

    BarList = [
        BlocksBar(Wwidth-158, (200, 200, 200), RED),
        BlocksBar(Wwidth-158, (200, 200, 200), RED)
    ]
    
    CodeBase = [
    {
        1: "bin/sprites/floor1.png",
        "S": "bin/sprites/tank.png"
    },
    {
        "set": "bin/sprites/add_button.png",
        2: "bin/sprites/wall1.png",
        3: "bin/sprites/wall2.png",
        "e": "bin/sprites/enemy_tank.png",
        "GTa": "bin/sprites/GTa.png",
        "GTb": "bin/sprites/GTb.png",
        "TrigB": "bin/sprites/TbuttonC.png",
        "door": "bin/sprites/Cdoor.png",
        "F": "bin/sprites/finish.png"
    }
    ]
    BarList[0].setCodeButtons(CodeBase[0])
    BarList[1].setCodeButtons(CodeBase[1])

    codeBlocList = []

    global layer
    layer = 0

    codeBlocList.append(buildMaketLocation(Xx, Yy, "start"))

    button_up = Button(30, Wheight - 170, 50, 50, DEFAULT_COLOR, 0, "bin/sprites/button_up.png", None, None, 1, setLayer, "up")
    button_down = Button(30, Wheight - 70, 50, 50, DEFAULT_COLOR, 0, "bin/sprites/button_up.png", None, None, 1, setLayer, "down")
    button_down.rotate = 180
    button_setLoc = Button(130, Wheight - 70, 50, 50, DEFAULT_COLOR, 0, "bin/sprites/button_up.png", None, None, 1, setLoc, [False, codeBlocList])
    button_setLoc.rotate = 90
    button_setLoc2 = Button(230, Wheight - 70, 50, 50, DEFAULT_COLOR, 0, "bin/sprites/button_up.png", None, None, 1, setLoc, [True, codeBlocList])
    button_setLoc2.rotate = -90
    button_addLoc = Button(300, Wheight - 70, 50, 50, DEFAULT_COLOR, 0, "bin/sprites/add_button.png", None, None, 1, add_maket, codeBlocList)
    button_save = Button(370, Wheight - 70, 50, 50, DEFAULT_COLOR, 0, "bin/sprites/save_button.png", None, None, 1, save_map_in_json, [codeBlocList, Path])

    while True:

        win_.fill(LIGHT_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    BarList[layer].checkButtons()
                    button_up.check()
                    button_down.check()
                    button_setLoc.check()
                    button_setLoc2.check()
                    button_addLoc.check()
                    button_save.check()

                    EditorLine = True

                    if BarList[layer].initedCode:
                    
                        for i in codeBlocList[globalLocation]["matrix"][layer]:
                            i.setCode(BarList[layer].initedCode, CodeBase[layer][BarList[layer].initedCode])
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    
                    EditorLine = False
        
        if EditorLine:
            if BarList[layer].initedCode:
                    
                for i in codeBlocList[globalLocation]["matrix"][layer]:
                    i.setCode(BarList[layer].initedCode, CodeBase[layer][BarList[layer].initedCode])
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            for i in codeBlocList[globalLocation]["matrix"][0]:
                i.rect.y -= 5
            for i in codeBlocList[globalLocation]["matrix"][1]:
                i.rect.y -= 5

        elif keys[pygame.K_s]:
            for i in codeBlocList[globalLocation]["matrix"][0]:
                i.rect.y += 5
            for i in codeBlocList[globalLocation]["matrix"][1]:
                i.rect.y += 5

        elif keys[pygame.K_a]:
            for i in codeBlocList[globalLocation]["matrix"][0]:
                i.rect.x -= 5
            for i in codeBlocList[globalLocation]["matrix"][1]:
                i.rect.x -= 5

        elif keys[pygame.K_d]:
            for i in codeBlocList[globalLocation]["matrix"][0]:
                i.rect.x += 5
            for i in codeBlocList[globalLocation]["matrix"][1]:
                i.rect.x += 5
        
        BarList[layer].draw()
        button_up.draw()
        button_down.draw()
        button_setLoc.draw()
        button_setLoc2.draw()
        button_addLoc.draw()
        button_save.draw()

        print_text(str(layer), 45, Wheight-110, 50)
        print_text(str(globalLocation), 195, Wheight-60, 50)

        for i in codeBlocList[globalLocation]["matrix"][layer]:
            i.draw()

        pygame.display.update()
        clock.tick(60)

def setLayer(arg):
    global layer    
    if arg == "up":
        if layer < 1:
            layer+=1

    elif arg == "down":
        if layer > 0:
            layer-=1

def setLoc(arg):
    global globalLocation

    if arg[0] and len(arg[1])-1 > globalLocation:
        globalLocation += 1

    elif not arg[0] and globalLocation > 0:
        globalLocation -= 1

def InvertELine():
    not EditorLine

def buildMaketLocation(sizeX, sizeY, name):
    mainBuffer = []
    for i in range(2):
        x = 0
        y = 0
        buffer = []

        for s in range(sizeX):
            x = 0
            y += 64
            for t in range(sizeY):
                buffer.append(CodeBloc(x, y, 64, 64, RED))
                x += 64
        
        mainBuffer.append(buffer)
    
    mainBuffer = {
        "info":{
            "name":name,
            "sizeX":sizeX,
            "sizeY":sizeY
        },
        "matrix":mainBuffer
    }
    return mainBuffer

def add_maket(list):
    x, y = QtSizeWin()
    list.append(buildMaketLocation(x, y, "q"))

def save_map_in_json(map):
    build_buffer = {}
    map_buffer = []
    numLoc = 0

    Ysize = 0
    Ynum = 0

    layer = 1

    for i in map[0]:
        build_buffer[numLoc] = {}
        build_buffer[numLoc]["info"] = i["info"]
        Ysize = i["info"]["sizeY"]

        for s in i["matrix"]:
            
            for j in s:
                map_buffer.append(j.code)
                print(j.code)
                Ynum += 1

                if Ynum >= Ysize:
                    map_buffer.append(0)
                    Ynum = 0
            
            build_buffer[numLoc][layer] = copy.copy(map_buffer)
            map_buffer.clear()
            layer = 2

        layer = 1
        numLoc += 1
    
    with open("bin/maps/" + map[1] + ".json", "w") as f:
        json.dump(build_buffer, f)
            


def print_text(text, x=50, y=50, size=50):
    win_.blit(pygame.font.Font(None, size).render(text, True, BLACK), (x, y))
    
def GlobalTeleportation(player, Lcor, flow):
    global Map
    global globalLocation

    globalLocation = Lcor

    for i in Map[Lcor]:
        if i.ID == "GTb":
            if i.Tflow == flow:
                player.rect.x = i.rect.x
                player.rect.y = i.rect.y

                return True

def FireTriger(objID, TrigerFlow):
    global Map

    for i in Map:
        for s in i:
            if s.ID == objID:
                if s.TrigerFlow == TrigerFlow:
                    s.update_status()

def MoveCamera(player, map, enemy):
    Vector = [0, 0]
    Vector[0] = Wwidth/2 - player.rect.x
    Vector[1] = Wheight/2 - player.rect.y

    for i in map:
        i.rect.x += Vector[0]
        i.rect.y += Vector[1]
    
    for i in enemy:
        i.rect.x += Vector[0]
        i.rect.y += Vector[1]
    
    player.rect.x += Vector[0]
    player.rect.y += Vector[1]

if __name__ == "__main__":
    core_init()
    MapEditor()
    pass   