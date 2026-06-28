#!/usr/bin/python
# -*- coding: utf-8 -*-
from src.entity     import Entity
from src.player     import Player
from src.enemy      import Enemy
from src.sword      import Sword
from src.projectile import EnemyShot


class EntityMediator:
    """
    Padrão Mediator: resolve todas as interações entre entidades
    (colisões, remoção de mortos) sem que as entidades se conheçam.
    """

    # ── Interações válidas ────────────────────────────────────────────────────
    @staticmethod
    def _resolve_pair(ent1: Entity, ent2: Entity):
        """
        Verifica se o par é uma interação válida e aplica os efeitos.

        Interações:
          • Sword     × Enemy     → Enemy perde health; sword é consumida
          • Player    × Enemy     → Player perde vida (invencibilidade protege)
          • Player    × EnemyShot → Player perde vida; tiro desaparece
        """
        is_sword_enemy  = (isinstance(ent1, Sword)    and isinstance(ent2, Enemy)  or
                           isinstance(ent2, Sword)    and isinstance(ent1, Enemy))
        is_enemy_player = (isinstance(ent1, Enemy)    and isinstance(ent2, Player) or
                           isinstance(ent2, Enemy)    and isinstance(ent1, Player))
        is_shot_player  = (isinstance(ent1, EnemyShot) and isinstance(ent2, Player) or
                           isinstance(ent2, EnemyShot) and isinstance(ent1, Player))

        if not (is_sword_enemy or is_enemy_player or is_shot_player):
            return

        # Usar colliderect nativo do pygame (mais preciso)
        if not ent1.rect.colliderect(ent2.rect):
            return

        # ── Aplicar efeitos ────────────────────────────────────────────────────
        if is_sword_enemy:
            sword = ent1 if isinstance(ent1, Sword) else ent2
            enemy = ent1 if isinstance(ent1, Enemy) else ent2
            enemy.health  -= sword.damage
            enemy.last_dmg = 'Sword'
            sword.health   = 0   # espada consumida após 1 hit

        elif is_enemy_player:
            player = ent1 if isinstance(ent1, Player) else ent2
            player.take_hit()

        elif is_shot_player:
            player = ent1 if isinstance(ent1, Player)    else ent2
            shot   = ent1 if isinstance(ent1, EnemyShot) else ent2
            player.take_hit()
            shot.health = 0

    # ── API pública ───────────────────────────────────────────────────────────
    @staticmethod
    def verify_collision(entity_list: list):
        """Percorre todos os pares únicos e resolve as colisões."""
        n = len(entity_list)
        for i in range(n):
            for j in range(i + 1, n):
                EntityMediator._resolve_pair(entity_list[i], entity_list[j])

    @staticmethod
    def verify_health(entity_list: list):
        """Remove da lista todas as entidades com health <= 0."""
        dead = [e for e in entity_list if e.health <= 0]
        for e in dead:
            entity_list.remove(e)
