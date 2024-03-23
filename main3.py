from pygame import *
from typing import Any
from random import randint
from time import time as timer

win = display.set_mode((700, 500))
display.set_caption('Догонялки')


mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()

#sound = mixer.Sound('hit.mp3')

#damage = mixer.Sound('hit.mp3')
#finish = mixer.Sound('money.mp3')

font.init()
font = font.Font(None, 70)
wind1 = font.render('YOU WIN', True, (225, 255, 0) )
wind2 = font.render('YOU LOSE', True, (255, 0, 0) )



clock = time.Clock()
FPS = 60
game = True


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global last_time
        global num_fire
        global rel_time
    
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 445:
            self.rect.y += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
        if key_pressed[K_SPACE]:
            if num_fire < 5 and rel_time == False:
                num_fire += 1
                #fire1.play()
                self.fire()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
    def fire(self):
        pulia = Pulia('victory.png', self.rect.centerx, self.rect.top, 10, 15, 30)
        pulias.add(pulia)

class Enemy(GameSprite):
    direct = 'left'
    def update(self):
        if self.rect.x >= 450:
            self.direct = 'left'
        if self.rect.x <= 200:
            self.direct = 'right'

        if self.direct == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
lost = 0
class Enemy2(GameSprite):  
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x < 10:
            self.rect.y = randint(50, 400)
            self.rect.x = 650
            lost = lost + 1

class Pulia(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.kill()



class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_widht, wall_hight):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.wall_widht = wall_widht
        self.wall_hight = wall_hight
        self.image = Surface((self.wall_widht, self.wall_hight))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


background = GameSprite('background.jpg', 0, 0, 0, 700, 500)
victory = GameSprite('victory.png', 550, 370, 7, 90, 90)
hero1 = Player('sprite1.png', 100, 70, 5, 65, 65)
hero2 = Enemy('sprite2.png', 400, 300, 5, 100, 100)
pulia = GameSprite('victory.png', 118, 570, 10, 15, 30)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 350, 30, 10, 380)
w3 = Wall(154, 205, 50, 200, 120, 10, 380)


enemys = sprite.Group()
for i in range(1, 9):
    enemy = Enemy2('sprite2.png', 650, randint(50, 400), 1, 100, 100)
    enemys.add(enemy)
pulias = sprite.Group()

score = 0
num_fire = 0
last_time = 0
rel_time = False
finish = False
clock = time.Clock()
FPS = 60
game = True
life = 10
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    
    if not finish:

        background.reset()
        hero1.update()
        hero1.reset()
        hero2.reset()
        hero2.update()
        enemys.draw(win)
        enemys.update()
        pulias.draw(win)
        pulias.update()
        victory.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        collide = sprite.groupcollide(enemys, pulias, True, True)
        #if collide:
            #death.play()
        for i in collide:
            score = score + 1
            enemy = Enemy2('sprite2.png', 650, randint(50, 400), 1, 100, 100)                         
            enemys.add(enemy)
    
        if sprite.spritecollide(hero1, enemys, True):
            life -= 1
            enemy = Enemy2('sprite2.png', 650, randint(50, 400), 1, 100, 100)
            enemys.add(enemy)
        if life <= 0:
            finish = True
            win.blit(wind2, (200, 50))
            hero1.rect.x = 100
            hero1.rect.y = 70
        if sprite.collide_rect(hero1, victory):
            win.blit(wind1, (200, 200))
        #finish.play()

        if sprite.collide_rect(hero1, hero2) or sprite.collide_rect(hero1, w1) or sprite.collide_rect(hero1, w2) or sprite.collide_rect(hero1, w3):
            win.blit(wind2, (200, 200))
            #damage.play()
            hero1.rect.x = 100
            hero1.rect.y = 70

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                ammo_no = font.render('Reload', 1, (255, 0, 0))
                win.blit(ammo_no, (260, 460))
            else:
                num_fire = 0
                rel_time = False
    clock.tick(FPS)
    display.update()
