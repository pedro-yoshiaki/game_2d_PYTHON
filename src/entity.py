#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pygame
from src.Const import ASSET_PATH, ENTITY_DAMAGE, ENTITY_HEALTH, ENTITY_SPEED


class Entity:
    def __init__(self, name: str, position: tuple):
        self.name   = name
        self.surf   = self._load_surface()
        self.rect   = self.surf.get_rect(center=position)
        self.health = ENTITY_HEALTH[name]
        self.damage = ENTITY_DAMAGE[name]
        self.speed  = ENTITY_SPEED[name]
        self.last_dmg = 'None'

    def _load_surface(self) -> pygame.Surface:
            """Carrega a imagem do asset ou gera uma surface de placeholder."""
            try:
                surf = pygame.image.load(ASSET_PATH + self.name + '.png').convert_alpha()
                
                nova_largura = 40
                
                proporcao = surf.get_height() / surf.get_width()
                nova_altura = int(nova_largura * proporcao)
                
                surf_ajustada = pygame.transform.scale(surf, (nova_largura, nova_altura))
                
                return surf_ajustada

            except (pygame.error, FileNotFoundError):
                # Placeholder geométrico se a imagem não for encontrada
                return self._make_placeholder()

    def _make_placeholder(self) -> pygame.Surface:
            """Surface colorida gerada em código, usada quando o PNG não existe."""
            colors = {
                'Player':    (80,  160, 220),
                'Enemy1':    (200, 60,  60),
                'Enemy2':    (180, 40,  140),
                'Sword':     (240, 220, 60),
                'EnemyShot': (255, 120, 30),
            }
            sizes = {
                'Player':    (36, 48),
                'Enemy1':    (36, 36),
                'Enemy2':    (44, 44),
                'Sword':     (32, 12),
                'EnemyShot': (14, 14),
            }
            color = colors.get(self.name, (150, 150, 150))
            size  = sizes.get(self.name, (32, 32))
            surf  = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill(color)
            return surf

    @abstractmethod
    def move(self):
            """Cada entidade define seu próprio movimento."""
            pass
