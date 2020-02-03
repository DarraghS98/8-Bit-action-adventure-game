import pygame as pg
vec = pg.math.Vector2

# Defining some colours
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BROWN = (106,55,5)

#Game Settings
WIDTH = 1024
HEIGHT = 760
FPS = 60
TITLE = "map"
BGCOLOR = BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
#Wall Settings
WALL_IMG = 'wall.png'
MENU_IMG = "menu_img.png"
#Mob Settings
MOB_IMG = 'zombie.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
#Player Settings
PLAYER_HEALTH = 3
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 2
PLAYER_IMG = 'robot.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BOW_OFFSET=vec(25,15)
MELEE_DAMAGE = 10
CHANGE_RATE = 1000

#Bow Settings
ARROW_IMG = "arrow.png"
ARROW_SPEED = 500
ARROW_LIFETIME = 1000
ARROW_RATE = 1000
ARROW_DAMAGE = 50

#Items
ITEM_IMAGES = {"potion":"potion.png","gem":"gem.png"}

#layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1