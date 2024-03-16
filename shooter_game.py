from pygame import *
from random import *
from time import time as tm
window = display.set_mode((700,500))
display.set_caption('SUSLIK')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
clock = time.Clock()
mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play(-1)
fire_sound = mixer.Sound('hehehe.ogg')
finish = False
game = True
class GaveSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image),(size_x,size_y)) 
       self.speed = player_speed
       self.rect =self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GaveSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def slaves_fire(self):
        bulet = Bullet('big_carrot_pencil.png',self.rect.centerx,self.rect.top,45,40,-15)
        krovavaya_morkva.add(bulet)
krovavaya_morkva = sprite.Group()


class Bullet(GaveSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
crosh = Player('CHURKA-transformed.png',250,400,50,50,10)

font.init()
font1 = font.SysFont('Arial',30)
win = font1.render('be positiv',True,(255,0,255))
lose = font1.render('you lose',True,(255, 0, 255))

score = 0
lost = 0
class Enemy(GaveSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(50,650)
            self.rect.y = 0
            lost += 1


live = 3

num_fire = 0
rel_time = False

nigers = sprite.Group()
for i in range(5):
    monsters = Enemy('niger.png',randint(50,650),-50,65,65,randint(1,3))
    nigers.add(monsters)

medovuxa = sprite.Group()
for i in range(3):
    kopatych = Enemy('kakish.png',randint(50,650),-50,65,65,randint(1,2))
    medovuxa.add(kopatych)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 20 and rel_time == False:
                    num_fire += 1
                    crosh.slaves_fire()
                    fire_sound.play()
                if num_fire >= 20 and rel_time == False:
                    rel_time = True
                    les_time = tm()


    if finish != True:

        window.blit(background,(0,0))
        text_lose = font1.render('Попущено: ' + str(lost),1,(255,0,255))
        window.blit(text_lose,(10,30))
        nigers.update()
        medovuxa.update()
        medovuxa.draw(window)
        krovavaya_morkva.update()
        krovavaya_morkva.draw(window)
        nigers.draw(window)
        crosh.update()
        crosh.reset()
        if rel_time == True:
            new_time = tm()
            if new_time - les_time < 3:
                reload = font1.render('выйди и зайди нормально!!',1,(244,66,156))
                window.blit(reload,(200,250))
            else:
                num_fire = 0
                rel_time = False
        stolknoveniya = sprite.groupcollide(nigers,krovavaya_morkva,True,True)
        for h in stolknoveniya:
            score += 1
            monsters = Enemy('niger.png',randint(50,650),-50,65,65,randint(1,3))
            nigers.add(monsters)
        if sprite.spritecollide(crosh,nigers,False)  or sprite.spritecollide(crosh,medovuxa,False):
            sprite.spritecollide(crosh,nigers,True) 
            sprite.spritecollide(crosh,medovuxa,True)
            live -= 1



        if live == 0 or lost >= 3:
            finish = True
            window.blit(lose,(200,200))
        if score >=10:
            finish = True
            window.blit(win,(250,350))
        schet = font1.render('счет:'+str(score),True,(255,255,255))
        window.blit(schet,(10,60))
        text_live = font1.render('жизни:' + str(live),True,(255,0,255))
        window.blit(text_live,(500,400))
    display.update()
    clock.tick(60)