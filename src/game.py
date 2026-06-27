#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from src.menu import Menu

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(size=(600, 480))
        self.current_state = None
        pygame.init()

        

    def run(self, ):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

            # Check for all events
            #for event in pygame.event.get():
             #   if event.type == pygame.QUIT:
              #      pygame.quit()  # Close Window
               #     quit()         # end pygame

    def change_state(self, ):
        pass
