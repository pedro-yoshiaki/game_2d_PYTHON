#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from src.entity import Entity
from src.Const import (
    PLAYER_KEYS, PLAYER_LIVES, ENTITY_SPEED,
    SWORD_COOLDOWN, SWORD_DURATION, SWORD_OFFSET,
    ARENA_LEFT, ARENA_RIGHT, ARENA_TOP, ARENA_BOTTOM,
    WIN_WIDTH, WIN_HEIGHT,
)


class Player(Entity):
    """Espadachim controlado pelo jogador."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.lives          = PLAYER_LIVES
        self.sword_cooldown = 0          # contador de cooldown do ataque
        self.invincible     = 0          # frames de invencibilidade após levar dano
        self.facing         = 'right'    # direção para posicionar a espada

    # ── Movimento ──────────────────────────────────────────────────────────────
    def move(self):
        keys = pygame.key.get_pressed()

        if any(keys[k] for k in PLAYER_KEYS['up']):
            self.rect.y -= self.speed
            self.facing  = 'up'
        if any(keys[k] for k in PLAYER_KEYS['down']):
            self.rect.y += self.speed
            self.facing  = 'down'
        if any(keys[k] for k in PLAYER_KEYS['left']):
            self.rect.x -= self.speed
            self.facing  = 'left'
        if any(keys[k] for k in PLAYER_KEYS['right']):
            self.rect.x += self.speed
            self.facing  = 'right'

        self.rect.left   = max(ARENA_LEFT,  self.rect.left)
        self.rect.right  = min(ARENA_RIGHT, self.rect.right)
        self.rect.top    = max(ARENA_TOP,   self.rect.top)
        self.rect.bottom = min(ARENA_BOTTOM, self.rect.bottom)

        if self.sword_cooldown > 0:
            self.sword_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1

    # ── Ataque ─────────────────────────────────────────────────────────────────
    def attack(self):
        """
        Retorna uma instância de Sword se Espaço for pressionado e o
        cooldown permitir; caso contrário retorna None.
        Importação local para evitar circular import.
        """
        if self.sword_cooldown > 0:
            return None

        keys = pygame.key.get_pressed()
        if not any(keys[k] for k in PLAYER_KEYS['attack']):
            return None

        self.sword_cooldown = SWORD_COOLDOWN
        cx, cy = self.rect.centerx, self.rect.centery

        offsets = {
            'right': (SWORD_OFFSET, 0),
            'left':  (-SWORD_OFFSET, 0),
            'up':    (0, -SWORD_OFFSET),
            'down':  (0,  SWORD_OFFSET),
        }
        dx, dy = offsets[self.facing]

        from src.sword import Sword 
        return Sword('Sword', (cx + dx, cy + dy))

    # ── Receber dano ───────────────────────────────────────────────────────────
    def take_hit(self):
        """Chamado pelo EntityMediator quando o player leva dano."""
        if self.invincible == 0:
            self.lives    -= 1
            self.invincible = 90   # 1,5 s de invencibilidade (60 fps × 1.5)

    @property
    def is_alive(self) -> bool:
        return self.lives > 0
