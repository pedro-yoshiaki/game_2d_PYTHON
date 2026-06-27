#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from src.Const import WIN_HEIGHT, WIN_WIDTH
from src.menu import Menu

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.current_state = None
        pygame.init()

    def run(self, ):       
        while True:
            menu = Menu(self.window)
            menu.run()
        
    def change_state(self, ):
        pass
