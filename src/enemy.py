#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import pygame
from src.entity import Entity
from src.Const import ENEMY_SHOT_DELAY, WIN_WIDTH, WIN_HEIGHT


class Enemy(Entity):
    """
    Inimigo que persegue o jogador e dispara projéteis periodicamente.
    A IA calcula a direção até o player a cada frame e avança um passo.
    """

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay  = ENEMY_SHOT_DELAY[name]
        self.shot_timer  = self.shot_delay    # começa já com delay cheio
        self.target_pos  = (WIN_WIDTH // 2, WIN_HEIGHT // 2)  # posição inicial do alvo

    # Atualizar alvo
    def update_target(self, pos: tuple):
        """Level chama isso a cada frame com a posição atual do player."""
        self.target_pos = pos

    # Movimento (IA de perseguição)
    def move(self):
        tx, ty = self.target_pos
        dx = tx - self.rect.centerx
        dy = ty - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.rect.x += int(self.speed * dx / dist)
            self.rect.y += int(self.speed * dy / dist)

        # Decrementar timer de disparo
        if self.shot_timer > 0:
            self.shot_timer -= 1

    # ── Disparo ────────────────────────────────────────────────────────────────
    def shoot(self):
        """
        Retorna um EnemyShot apontado para o player quando o timer zerar,
        caso contrário retorna None.
        """
        if self.shot_timer > 0:
            return None

        self.shot_timer = self.shot_delay

        from src.projectile import EnemyShot   # importação local
        return EnemyShot(
            name='EnemyShot',
            position=(self.rect.centerx, self.rect.centery),
            target_pos=self.target_pos,
        )
