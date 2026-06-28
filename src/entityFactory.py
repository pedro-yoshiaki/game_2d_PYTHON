#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from src.Const import (
    WIN_WIDTH, WIN_HEIGHT, ARENA_TOP, ARENA_LEFT, ARENA_RIGHT, ARENA_BOTTOM
)
from src.player  import Player
from src.enemy   import Enemy


class EntityFactory:
    """
    Padrão Factory: centraliza a criação e o posicionamento inicial
    de todas as entidades do jogo.
    """

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:

            case 'Player':
                # Nasce no centro da arena
                cx = WIN_WIDTH  // 2
                cy = ARENA_TOP + (WIN_HEIGHT - ARENA_TOP) // 2
                return Player('Player', (cx, cy))

            case 'Enemy1':
                pos = EntityFactory._random_border_position()
                return Enemy('Enemy1', pos)

            case 'Enemy2':
                pos = EntityFactory._random_border_position()
                return Enemy('Enemy2', pos)

            case _:
                raise ValueError(f"EntityFactory: entidade desconhecida '{entity_name}'")

    # ── Posição aleatória na borda da arena ────────────────────────────────────
    @staticmethod
    def _random_border_position() -> tuple:
        """
        Sorteia um ponto em uma das quatro bordas da arena para que os
        inimigos apareçam vindo de diferentes direções.
        """
        margin = 30   # fora da área visível para não "nascer" na frente do player
        side   = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'top':
            return (random.randint(ARENA_LEFT, ARENA_RIGHT), ARENA_TOP - margin)
        elif side == 'bottom':
            return (random.randint(ARENA_LEFT, ARENA_RIGHT), WIN_HEIGHT + margin)
        elif side == 'left':
            return (ARENA_LEFT - margin, random.randint(ARENA_TOP, WIN_HEIGHT))
        else:  # right
            return (ARENA_RIGHT + margin, random.randint(ARENA_TOP, WIN_HEIGHT))
