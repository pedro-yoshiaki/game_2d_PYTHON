#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from src.entity import Entity
from src.Const import SWORD_DURATION, SWORD_OFFSET


class Sword(Entity):
    """
    Hitbox de ataque circular ao redor do player.
    São criadas 4 instâncias simultâneas (cima, baixo, esquerda, direita),
    cobrindo 360° ao redor do personagem.
    Fica ativa por SWORD_DURATION frames e some automaticamente.
    """

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.lifetime = SWORD_DURATION

    def move(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.health = 0   # EntityMediator remove quem tem health == 0

    def draw_glow(self, window: pygame.Surface):
        """Desenha o efeito visual da espada (arco brilhante)."""
        glow = pygame.Surface(self.surf.get_size(), pygame.SRCALPHA)
        alpha = int(220 * (self.lifetime / SWORD_DURATION))   # fade out
        glow.fill((240, 220, 60, alpha))
        window.blit(glow, self.rect)


def create_sword_ring(player_center: tuple) -> list:
    """
    Fábrica de ataque circular: retorna uma lista com 4 Swords
    posicionadas ao redor do centro do player.
    """
    cx, cy = player_center
    offsets = {
        'right': ( SWORD_OFFSET,  0),
        'left':  (-SWORD_OFFSET,  0),
        'up':    ( 0, -SWORD_OFFSET),
        'down':  ( 0,  SWORD_OFFSET),
    }
    return [Sword('Sword', (cx + dx, cy + dy)) for dx, dy in offsets.values()]
