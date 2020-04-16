import pygame as pg
import time
from settings import *
from random import uniform, choice, randint
from tilemap import collide_hit_rect
vec = pg.math.Vector2

def healing_pool_check(sprite,group):
    hits = pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
    if hits:
        sprite.health = PLAYER_HEALTH

def teleport_player(sprite,group):
    hits = pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
    if hits:
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            if hits[0].name == "teleport_1":
                sprite.pos = vec(1056.0,256.0)
                time.sleep(.2)
            elif hits[0].name == "teleport_2":
                sprite.pos = vec(1440.0,256.0)
                time.sleep(.2)
            elif hits[0].name == "teleport_3":
                sprite.pos = vec (1824.0,288.0)
                time.sleep(.2)
            elif hits[0].name == "teleport_4":
                sprite.pos = vec(544.0,256.0)
                time.sleep(.2)

def collide_with_walls(sprite,group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == "y":
        hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.width / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = game.player_idle
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.game = game
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.rot = 0
        self.last_shot = 0
        self.change = 0
        self.arrow_image = None
        self.health = 100
        self.controls = True
        self.potions = 0
        self.direction = "south"
        self.counter = 0
        self.gems = 0
        self.attack = "melee"
        self.kills = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            for images in range(0,len(self.game.player_west)):
                self.image = self.game.player_west[images//randint(1,5)]
            self.arrow_image = self.game.arrow_images[2]
            self.sword_swipe = self.game.sword_swipe_hor
            self.rot = 180
            self.vel = vec(-PLAYER_SPEED,0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            for images in range(0,len(self.game.player_east)):
                self.image = self.game.player_east[images//randint(1,5)]
            self.arrow_image = self.game.arrow_images[1]
            self.sword_swipe = self.game.sword_swipe_hor
            self.rot = 0
            self.vel = vec(PLAYER_SPEED,0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            for images in range(0,len(self.game.player_north)):
                self.image = self.game.player_north[images//randint(1,5)]
            self.arrow_image = self.game.arrow_images[0]
            self.sword_swipe = self.game.sword_swipe_vert
            self.rot = 90
            self.vel = vec(0,-PLAYER_SPEED)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            for images in range(0,len(self.game.player_south)):
                self.image = self.game.player_south[images//randint(1,5)]
            self.arrow_image = self.game.arrow_images[3]
            self.sword_swipe = self.game.sword_swipe_vert
            self.rot = 270
            self.vel = vec(0,PLAYER_SPEED)
        if keys[pg.K_q]:
            now = pg.time.get_ticks()
            if now - self.change > CHANGE_RATE:
                self.change = now
                if self.attack == "melee":
                    self.attack = "bow"
                else:
                    self.attack = "melee"

        if keys[pg.K_SPACE]:
            if self.attack == "bow":
                now = pg.time.get_ticks()
                if now - self.last_shot > ARROW_RATE:
                    self.last_shot = now
                    dir = vec(1,0).rotate(-self.rot)
                    pos = self.pos + BOW_OFFSET.rotate(-self.rot)
                    Arrow(self.game,pos,dir,self.arrow_image)
            elif self.attack == "melee":
                now = pg.time.get_ticks()
                if now - self.last_shot > ARROW_RATE:
                    self.last_shot = now
                    if self.rot >= 315 or self.rot <= 45:
                        Melee(self.game,vec(self.pos.x + TILESIZE,self.pos.y),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x + TILESIZE,self.pos.y-TILESIZE),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x + TILESIZE,self.pos.y+TILESIZE),self.sword_swipe)
                    elif self.rot >= 46 and self.rot <= 135:
                        Melee(self.game,vec(self.pos.x,self.pos.y - TILESIZE),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x - TILESIZE,self.pos.y-TILESIZE),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x + TILESIZE,self.pos.y-TILESIZE),self.sword_swipe)
                    elif self.rot >= 136 and self.rot <= 225:
                        Melee(self.game,vec(self.pos.x - TILESIZE,self.pos.y),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x - TILESIZE,self.pos.y - TILESIZE),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x - TILESIZE,self.pos.y + TILESIZE),self.sword_swipe)
                    elif self.rot >= 226 and self.rot <= 315:
                        Melee(self.game,vec(self.pos.x,self.pos.y+TILESIZE),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x - TILESIZE,self.pos.y+TILESIZE),self.sword_swipe)
                        Melee(self.game,vec(self.pos.x + TILESIZE,self.pos.y+TILESIZE),self.sword_swipe)

    def update(self):
        self.get_keys()
        self.rot = (self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self,self.game.walls,"x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self,self.game.walls, "y")
        self.rect.center = self.hit_rect.center
        teleport_player(self,self.game.teleport)
        healing_pool_check(self,self.game.healing_pool)
        

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
    
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            if self.game.endless == True:
                mob1, mob2 = Mob(self.game,randint(1100,1500),randint(1100,1500)),Mob(self.game,randint(1100,1500),randint(1100,1500))
                if self.game.player.kills == 5:
                    ARROW_RATE = 800
                elif self.game.player.kills == 10:
                    ARROW_RATE = 100
                elif self.game.player.kills == 15:
                    ARROW_RATE = 1
                self.game.player.kills += 1
            
    
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0,width,7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
            

class Obstacle(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y 

class Level(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):
        self.groups = game.levels
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y 

class Teleport(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h,name):
        self.groups = game.teleport
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.controls = True
    
class HealingPool(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):
        self.groups = game.healing_pool
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Arrow(pg.sprite.Sprite):
    def __init__(self,game,pos,dir,arrow_image):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.arrows
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = arrow_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * ARROW_SPEED
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > ARROW_LIFETIME:
            self.kill()

class Melee(pg.sprite.Sprite):
    def __init__(self,game,pos,image):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.arrows
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MELEE_LIFETIME:
            self.kill()

            
class Item(pg.sprite.Sprite):
    def __init__(self,game,pos,type):
        self.layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos