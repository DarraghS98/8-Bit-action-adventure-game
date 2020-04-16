#Importing all modules
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from start import *
from endless import *
from story import *
from client import *
""" 
    This is the game class. It is a clean way to run the game. FOR PEOPLE WITH KNOWLEDGE OF PYTHON. Menu is the default method that will start the initial GUI and give users an option on what to play it calls start.py.
    Story is what menu calls to start story.py
    Endless calls endless.py
    Client and Server are currently not active, if you feel you could get it working then scroll down below to __name__ == "__main__": to call these methods 
    *****GAME MAY CRASH ****** however there is some framework for a network between a client and a server
"""
class Game:
    def __init__(self):
        self.start = True
        self.start_story = False
        self.start_endless = False

    def menu(self):
        while self.start == True:
            menu = StartScreen(self)
            menu.show_start_screen()
    def story(self):
        while self.start_story == True:
            story = Story(self)
            story.new()
            story.run()
            story.show_go_screen()
            story.draw_grid()
    
    def endless(self):
        endless = Endless(self)
        endless.new()
        endless.run()
        endless.show_go_screen()
        endless.draw_grid()

    def client(self):
        client = Client(self)
        client.new()
        client.run()
        client.show_go_screen()
        client.draw_grid()

    def server(self):
        server = Server(self)
        server.new()
        server.run()
        server.start()


if __name__ == "__main__":
    #Creating Game
    game = Game()
    #game.server()
    #game.client()
    game.menu()