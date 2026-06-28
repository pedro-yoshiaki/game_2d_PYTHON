#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from src.entity import Entity
from src.Const import WIN_WIDTH, WIN_HEIGHT


class EnemyShot(Entity):
    """
    Projétil disparado pelo inimigo em direção ao player.
    A direção é calculada no momento do disparo e permanece fixa.
    """

    def __init__(self, name: str, position: tuple, target_pos: tuple):
        super().__init__(name, position)

        # Calcular vetor de direção normalizado
        dx = target_pos[0] - position[0]
        dy = target_pos[1] - position[1]
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.vx = self.speed * dx / dist
            self.vy = self.speed * dy / dist
        else:
            self.vx, self.vy = self.speed, 0   # fallback: vai para a direita

    def move(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # Sai da tela → remove
        if (self.rect.right  < 0 or self.rect.left  > WIN_WIDTH or
                self.rect.bottom < 0 or self.rect.top   > WIN_HEIGHT):
            self.health = 0
