from main import *
import os
import subprocess
class StartScreen:
    def __init__(self,game):
        self.start = True
        pg.init()
        self.game = game
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.start_menu = True

    def show_start_screen(self):
        while self.start == True:
            game_folder = path.dirname(__file__)
            img_folder = path.join(game_folder,"img")
            music_folder = path.join(game_folder,"music")
            settings = path.join(game_folder,"settings.py")
            pg.mixer.music.load(path.join(music_folder,TRACK))
            try:
                menu = pg.image.load(path.join(img_folder,MENU_IMG)).convert_alpha()
            except:
                menu = pg.image.load(path.join(img_folder,MENU_IMG_ENDLESS)).convert_alpha()
            self.screen.blit(menu,(0,0))
            pg.display.flip()
            pg.mixer.music.play(-1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN]:
                    self.game.start_story = True
                    self.game.start = False
                    self.game.story()
                if keys[pg.K_RSHIFT] or keys[pg.K_LSHIFT]:
                    self.game.start_endless = True
                    self.game.start = False
                    self.game.endless()
                
    def quit(self):
        pg.quit()
        sys.exit()
    