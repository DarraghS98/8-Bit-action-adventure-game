import socket
from _thread import *
from sprites import *
import pickle
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from network import Network
from _thread import *
import socket
from server import *
from endless import *
from story import *
from client import *
import pickle
import json

class Server:
    def __init__(self,game):
        self.game = game
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.start_menu = True
        self.story = False
        self.endless = False
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
        self.map = TiledMap(path.join(map_folder,"test.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
        self.melee_img = pg.image.load(path.join(img_folder,ARROW_IMG)).convert_alpha()
        self.arrow_img = pg.image.load(path.join(img_folder,ARROW_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
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
        if self.multiplayer == True:
            n.send(self.player)
        #mobs hit player
        hits = pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.pos -= vec(MOB_KNOCKBACK,0)
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.endless = False
                self.story = False
                self.start_menu = True
                self.nav()
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

    
    def run(self):
        #IPv4 ip address
        server = "192.168.1.119"
        #Port number
        port = 5555

        #Creating a socket for server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Try and bind socket to ip,port
        try:
            s.bind((server,port))
        #Return error if fail
        except socket.error as e:
            str(e)

        #Print statement to show state of server
        print("Waiting for connection, Server started....")

        #Creating 2 players
        players = [Player(self,2832,2832), Player(self,2832,368)]

        #Function for sending and recv data
        def connected_client(conn,player):
            #Sends current player using pickle
            conn.send(pickle.dumps(players[player]))
            reply = ""
            #Starts loop
            while True:
                #Tries to recieve data
                try:
                    data = pickle.loads(conn.recv(2048))
                    #Current player = recieved data
                    players[player] = data

                    #No data was recieved
                    if not data:
                        #Client disconnected
                        print("Disconnected")
                        break
                    else:
                        #If player = player 1
                        if player == 1:
                            #Set reply to player[0] information
                            reply = players[0]
                        else:
                            #Set reply to player[1] information
                            reply = players[1]
                    #Sends information dependent on player
                    conn.sendall(pickle.dumps(reply))
                except:
                    break
            
            print("Lost Connection")
            conn.close()

        currentPlayer = 0

        #Loop for client connections
        while True:
            #Listening for client
            s.listen()
            #Gets connection and address of client that connected
            conn, addr = s.accept()
            print("Coneected to:" , addr)
            #Runs function to send client data
            start_new_thread(connected_client, (conn,currentPlayer))
            #Increase player counter
            currentPlayer += 1
