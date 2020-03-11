#Importing all modules
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

class Game:
    def __init__(self):
        self.test = None

        
    def story(self):
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
        server.run()


if __name__ == "__main__":
    #Creating Game
    game = Game()
    game.server()
    #game.client()