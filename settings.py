import pygame as pg
vec = pg.math.Vector2

#MOB SETTINGS (CHANGING ENEMY VALUES)
#Replace png to have different enemies
MOB_IMG = 'zombie.png' 
#Mobs use random speeds. Change list vaues (lower is slower)
MOB_SPEEDS = [150, 100, 75, 125] 
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
#Setting mob health
MOB_HEALTH = 100
#How much damage a mob can do
MOB_DAMAGE = 10
#Knockback of mob
MOB_KNOCKBACK = 50
#The distance mobs use to avoid each other
AVOID_RADIUS = 50

#PLAYER SETTINGS 
#Player health (Keep mob damage in mind when changing this)
PLAYER_HEALTH = 100
#Player speed (Remeber to give it a mid range number. Too fast/slow the game wont be playable but have fun playing with it)
PLAYER_SPEED = 300
#Sets melee damage
MELEE_DAMAGE = 1000
#The time that the melee object will last on screen. Higher: Longer time for melee to hit
MELEE_LIFETIME = 50
#The time that must ellapse before changing weapon
CHANGE_RATE = 1000
#Speed of arrow (Change this if you want but there should be no reason)
ARROW_SPEED = 500
#How long an arrow object lasts on screen. Usually wont make a different due to the fact the arrows dies on wall/mob impact
ARROW_LIFETIME = 1000
#How long before shooting the new arrow
ARROW_RATE = 1000
#Arrow Damage
ARROW_DAMAGE = 50
#Health recovered from health pack / potion
HEALTH_PACK_AMOUNT = 20

#DO NOT TOUCH SETTINGS UNDER THIS LINE
#################################################################################################################################
#COLOUR CODE 
#IF CHANGING THESE ONLY CHANGE THE RGB VALUES. VARIABLE NAME CHANGE CAN BREAK THE GAME
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
TITLE = "Multi-Level Python"
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
MENU_IMG = "start.png"
MENU_IMG_ENDLESS = "start_endless.png"
TRACK = "soundtrack.mp3"

#Player Settings

BOW_IMG = "bow.png"
SWORD_IMG = "sword.png"
IDLE = "idle.png"
WALK_WEST = ["walk_west_1.png","walk_west_2.png","walk_west_3.png","walk_west_4.png","walk_west_5.png"]
WALK_NORTH = ["walk_north_1.png","walk_north_2.png","walk_north_3.png","walk_north_4.png","walk_north_5.png"]
WALK_SOUTH = ["walk_south_1.png","walk_south_2.png","walk_south_3.png","walk_south_4.png","walk_south_5.png"]
WALK_EAST = ["walk_east_1.png","walk_east_2.png","walk_east_3.png","walk_east_4.png","walk_east_5.png"]
ARROW_IMGS = ["arrow_up.png","arrow_right.png","arrow_left.png","arrow_down.png"]
SWORD_SWIPE_VERT = "sword_swipe_vert.png"
SWORD_SWIPE_HOR = "sword_swipe_hor.png"
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BOW_OFFSET=vec(25,15)
#Bow Settings
ARROW_IMG = "arrow.png"
HIT_ALLOWANCE = 1000
#Items
ITEM_IMAGES = {"health":"health.png"}
#layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1