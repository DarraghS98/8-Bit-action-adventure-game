#Importing all modules
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from network import Network
from server import *
from story import *
import pickle


# HUD
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,2)


def draw_player_attack(surf,attack,sword,bow):
    if attack == "melee":
        surf.blit(sword,(0,HEIGHT - 70))
    elif attack == "bow":
        surf.blit(bow,(0,HEIGHT - 70))

def draw_player_gems(surf,x,y,gems):
    if gems < 0:
        gems = 0
    GEM_DIM = 30
    outline= pg.Rect(x,y,GEM_DIM,GEM_DIM)
    fill_rect = pg.Rect(x,y,GEM_DIM,GEM_DIM)
    pg.draw.rect(surf,YELLOW,fill_rect)
    pg.draw.rect(surf,BLACK,outline,2)
    font = pg.font.SysFont('Aerial', 20, True, False)
    text = font.render(str(gems), True, BLACK)
    surf.blit(text,(WIDTH-40,20))#

def draw_player_kills(surf,kills):
    font = pg.font.SysFont('Aerial', 50, True, False)
    text = font.render(str(kills), True, BLACK)
    surf.blit(text,(WIDTH/2,20))

class Endless:
    def __init__(self,game):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.FULLSCREEN)
        self.start_menu = True
        self.story = False
        self.endless = True
        self.game = game
        self.multiplayer = False
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 32)
        self.font_color = (100, 200, 150)
        self.last_hit = 0
        self.player = None
        #Setting repeat rate for buttons
        pg.key.set_repeat(500, 100)
            
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,"img")
        map_folder = path.join(game_folder,"maps")
        self.map = TiledMap(path.join(map_folder,"endless.tmx"))
        self.map_img = self.map.make_map()
        self.melee_hud = pg.image.load(path.join(img_folder, SWORD_IMG)).convert_alpha()
        self.bow_hud = pg.image.load(path.join(img_folder, BOW_IMG)).convert_alpha()
        self.map_rect = self.map_img.get_rect()
        self.sword_swipe_vert = pg.image.load(path.join(img_folder,SWORD_SWIPE_VERT)).convert_alpha()
        self.sword_swipe_hor = pg.image.load(path.join(img_folder,SWORD_SWIPE_HOR)).convert_alpha()
        self.player_idle = pg.image.load(path.join(img_folder,IDLE)).convert_alpha()
        self.player_west = []
        for image in WALK_WEST:
            self.player_west.append(pg.image.load(path.join(img_folder,image)).convert_alpha())
        self.player_north = []
        for image in WALK_NORTH:
            self.player_north.append(pg.image.load(path.join(img_folder,image)).convert_alpha())
        self.player_east = []
        for image in WALK_EAST:
            self.player_east.append(pg.image.load(path.join(img_folder,image)).convert_alpha())
        self.player_south = []
        for image in WALK_SOUTH:
            self.player_south.append(pg.image.load(path.join(img_folder,image)).convert_alpha())
        self.mob_img = pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
        self.arrow_images = []
        for image in ARROW_IMGS:
            self.arrow_images.append(pg.image.load(path.join(img_folder,image)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder,ITEM_IMAGES[item])).convert_alpha()
    
    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.teleport = pg.sprite.Group()
        self.healing_pool = pg.sprite.Group()
        self.melee = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                self.player = Player(self, obj_center.x,obj_center.y)
            if tile_object.name == "mob":
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                Mob(self,obj_center.x,obj_center.y)
            if tile_object.name == "wall":
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name in ["health"]:
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                Item(self, obj_center,tile_object.name)
        print("Tiles loaded")
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = (self.clock.tick(FPS)/1000)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        #mobs hit player
        hits = pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.pos -= vec(MOB_KNOCKBACK,0)
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.game.start = True
                self.game.start_story = False
                self.game.start_endless = False
                self.game.menu()
        # arrows hit mobs
        hits = pg.sprite.groupcollide(self.mobs,self.arrows, False, True)
        for hit in hits:
            print(hit)
            hit.health -= ARROW_DAMAGE
            hit.vel = vec(0,0)
        # Melee hits mob
        hits = pg.sprite.groupcollide(self.mobs,self.melee,False,True)
        for hit in hits:
            print(hit)
            hit.health -= MELEE_DAMAGE
            hit.vel = vec(0,0)

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
    def draw_grid(self):
        for x in range(0,WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY,(0,y),(WIDTH,y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
       # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite,Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #Displays hit rectangle
        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2 )
        draw_player_health(self.screen,10,10,self.player.health / PLAYER_HEALTH)
        draw_player_attack(self.screen,self.player.attack,self.melee_hud,self.bow_hud)
        draw_player_gems(self.screen,WIDTH-50,10,self.player.gems)
        if self.endless == True:
            draw_player_kills(self.screen,self.player.kills)
        pg.display.flip()
    

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
