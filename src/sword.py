#!/usr/bin/python
# -*- coding: utf-8 -*-
from src.entity import Entity
from src.Const import SWORD_DURATION


class Sword(Entity):
    """
    Hitbox temporária do ataque de espada do Player.
    Fica ativa por SWORD_DURATION frames e some automaticamente.
    Não se move — permanece no ponto de criação.
    """

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.lifetime = SWORD_DURATION

    def move(self):
        """A espada não se move; apenas decresce o tempo de vida."""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.health = 0   # EntityMediator vai remover quem tem health == 0
