#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Menu:
    def __init__(self, window):
        self.window = window
        # 1. Carregando as imagens (usando convert_alpha para manter a transparência do PNG)
        self.bg_layer1 = pygame.image.load('./assets/background_menu/1.png').convert_alpha()
        self.bg_layer2 = pygame.image.load('./assets/background_menu/2.png').convert_alpha()
        self.bg_layer3 = pygame.image.load('./assets/background_menu/3.png').convert_alpha()
        self.bg_layer4 = pygame.image.load('./assets/background_menu/4.png').convert_alpha()
        
        # 2. Variáveis para controlar a posição X das nuvens (Parallax)
        self.cloud_x3 = 0
        self.cloud_x4 = 0

    def draw(self):
        # Desenhando as camadas estáticas de fundo (Céu e Degradê)
        self.window.blit(self.bg_layer1, (0, 0))
        self.window.blit(self.bg_layer2, (0, 0))
        
        # Desenhando a primeira camada de nuvens (Movimento lento)
        self.window.blit(self.bg_layer3, (self.cloud_x3, 0))
        self.window.blit(self.bg_layer3, (self.cloud_x3 + self.bg_layer3.get_width(), 0)) # Truque do loop
        
        # Desenhando a segunda camada de nuvens (Movimento rápido)
        self.window.blit(self.bg_layer4, (self.cloud_x4, 0))
        self.window.blit(self.bg_layer4, (self.cloud_x4 + self.bg_layer4.get_width(), 0)) # Truque do loop

    def update_animation(self):
        # Aumente ou diminua os valores para alterar a velocidade do vento
        self.cloud_x3 -= 0.01
        self.cloud_x4 -= 0.02

        # Quando a imagem sai totalmente da tela, ela reseta a posição para criar o loop contínuo
        if self.cloud_x3 <= -self.bg_layer3.get_width():
            self.cloud_x3 = 0
        if self.cloud_x4 <= -self.bg_layer4.get_width():
            self.cloud_x4 = 0

    def run(self):
        pygame.mixer_music.load('./assets/soundtrack/Menu_sound.mp3')
        pygame.mixer_music.play(-1)
        while True:
            self.update_animation()
            self.draw()
            pygame.display.flip()
        
            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()         # end pygame

    def handle_input(self, ):
        pass
