#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from src.entity import Entity
from src.Const import (
    PLAYER_KEYS, PLAYER_LIVES, ENTITY_SPEED,
    SWORD_COOLDOWN,
    ARENA_LEFT, ARENA_RIGHT, ARENA_TOP, ARENA_BOTTOM,
)


class Player(Entity):
    """Espadachim controlado pelo jogador."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.lives          = PLAYER_LIVES
        self.sword_cooldown = 0
        self.invincible     = 0

    # ── Movimento ──────────────────────────────────────────────────────────────
    def move(self):
        keys = pygame.key.get_pressed()

        if any(keys[k] for k in PLAYER_KEYS['up']):
            self.rect.y -= self.speed
        if any(keys[k] for k in PLAYER_KEYS['down']):
            self.rect.y += self.speed
        if any(keys[k] for k in PLAYER_KEYS['left']):
            self.rect.x -= self.speed
        if any(keys[k] for k in PLAYER_KEYS['right']):
            self.rect.x += self.speed

        # Clampar dentro da arena
        self.rect.left   = max(ARENA_LEFT,   self.rect.left)
        self.rect.right  = min(ARENA_RIGHT,  self.rect.right)
        self.rect.top    = max(ARENA_TOP,    self.rect.top)
        self.rect.bottom = min(ARENA_BOTTOM, self.rect.bottom)

        # Decrementar cooldowns
        if self.sword_cooldown > 0:
            self.sword_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1

    # ── Ataque circular ────────────────────────────────────────────────────────
    def attack(self) -> list:
        """
        Retorna uma lista de 4 Swords (ataque 360°) quando Espaço for
        pressionado e o cooldown permitir. Caso contrário retorna lista vazia.
        """
        if self.sword_cooldown > 0:
            return []

        keys = pygame.key.get_pressed()
        if not any(keys[k] for k in PLAYER_KEYS['attack']):
            return []

        self.sword_cooldown = SWORD_COOLDOWN

        from src.sword import create_sword_ring   # importação local
        return create_sword_ring(self.rect.center)

    # ── Receber dano ───────────────────────────────────────────────────────────
    def take_hit(self):
        if self.invincible == 0:
            self.lives     -= 1
            self.invincible = 90   # 1,5 s de invencibilidade

    @property
    def is_alive(self) -> bool:
        return self.lives > 0
