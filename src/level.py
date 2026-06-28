#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import random
import math
import pygame
from pygame import Surface

from src.Const import (
    WIN_WIDTH, WIN_HEIGHT, FPS,
    ARENA_TOP, ARENA_LEFT, ARENA_RIGHT, ARENA_BOTTOM,
    C_WHITE, C_RED, C_YELLOW, C_GREEN, C_DARK, C_BLACK, C_GRAY, C_ORANGE,
    PLAYER_LIVES, EVENT_ENEMY, EVENT_TIMEOUT,
    SPAWN_TIME, TIMEOUT_STEP, TIMEOUT_LEVEL, MAX_ENEMIES,
    SWORD_DURATION, SWORD_OFFSET,
)
from src.entity         import Entity
from src.player         import Player
from src.enemy          import Enemy
from src.sword          import Sword
from src.entityFactory  import EntityFactory
from src.entityMediator import EntityMediator


class Level:
    """
    Loop principal de gameplay.
    Retorna True  → jogador sobreviveu (vitória).
    Retorna False → jogador morreu     (derrota).
    """

    def __init__(self, window: Surface):
        self.window       = window
        self.timeout      = TIMEOUT_LEVEL
        self.entity_list: list[Entity] = []

        self.player = EntityFactory.get_entity('Player')
        self.entity_list.append(self.player)

        pygame.time.set_timer(EVENT_ENEMY,   SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    # ── Loop principal ────────────────────────────────────────────────────────
    def run(self) -> bool:
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)

            # ── Eventos ───────────────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    self._spawn_enemy()
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout <= 0:
                        return True   # VITÓRIA

            # ── Checar derrota ────────────────────────────────────────────────
            if not self.player.is_alive:
                return False   # DERROTA

            # ── Lógica ────────────────────────────────────────────────────────
            new_entities = []

            for ent in self.entity_list:
                ent.move()

                if isinstance(ent, Enemy):
                    ent.update_target(self.player.rect.center)
                    shot = ent.shoot()
                    if shot is not None:
                        new_entities.append(shot)

                if isinstance(ent, Player):
                    swords = ent.attack()   # lista de 0 ou 4 Swords
                    new_entities.extend(swords)

            self.entity_list.extend(new_entities)

            # ── Colisões e remoção ────────────────────────────────────────────
            EntityMediator.verify_collision(self.entity_list)
            EntityMediator.verify_health(self.entity_list)

            # ── Render ────────────────────────────────────────────────────────
            self._draw()
            pygame.display.flip()

    # ── Spawn ─────────────────────────────────────────────────────────────────
    def _spawn_enemy(self):
        enemy_count = sum(1 for e in self.entity_list if isinstance(e, Enemy))
        if enemy_count >= MAX_ENEMIES:
            return
        choice = random.choice(['Enemy1', 'Enemy2'])
        self.entity_list.append(EntityFactory.get_entity(choice))

    # ── Renderização ──────────────────────────────────────────────────────────
    def _draw(self):
        # Fundo
        self.window.fill((40, 40, 40))
        pygame.draw.rect(
            self.window, (55, 55, 55),
            (ARENA_LEFT, ARENA_TOP, ARENA_RIGHT - ARENA_LEFT, ARENA_BOTTOM - ARENA_TOP)
        )
        # Grade
        for x in range(0, WIN_WIDTH, 80):
            pygame.draw.line(self.window, (65, 65, 65), (x, ARENA_TOP), (x, ARENA_BOTTOM))
        for y in range(ARENA_TOP, WIN_HEIGHT, 80):
            pygame.draw.line(self.window, (65, 65, 65), (0, y), (WIN_WIDTH, y))
        # Borda
        pygame.draw.rect(
            self.window, C_GRAY,
            (ARENA_LEFT, ARENA_TOP, ARENA_RIGHT - ARENA_LEFT, ARENA_BOTTOM - ARENA_TOP), 2
        )

        # Entidades
        for ent in self.entity_list:
            if isinstance(ent, Sword):
                self._draw_sword_arc(ent)
            elif isinstance(ent, Player) and ent.invincible > 0:
                if (ent.invincible // 6) % 2 == 0:
                    continue
                self.window.blit(ent.surf, ent.rect)
            else:
                self.window.blit(ent.surf, ent.rect)

        # HUD por cima de tudo
        self._draw_hud()

    def _draw_sword_arc(self, sword: Sword):
        """
        Desenha cada hitbox de espada como um arco brilhante.
        O tamanho e a opacidade diminuem conforme o lifetime acaba (fade out).
        """
        alpha    = int(220 * (sword.lifetime / SWORD_DURATION))
        progress = 1.0 - (sword.lifetime / SWORD_DURATION)   # 0→1 conforme some

        # Determinar direção da hitbox em relação ao centro do player
        pcx, pcy = self.player.rect.center
        scx, scy = sword.rect.center
        dx, dy   = scx - pcx, scy - pcy

        # Ângulo base da hitbox (em graus, 0 = direita)
        angle_deg = math.degrees(math.atan2(dy, dx))

        # Raio do arco (cresce levemente no início)
        radius = int(SWORD_OFFSET * (0.8 + 0.3 * progress))

        # Desenhar arco com pygame.draw.arc
        arc_surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        arc_rect = pygame.Rect(
            pcx - radius, pcy - radius,
            radius * 2,   radius * 2
        )
        start_angle = math.radians(angle_deg - 55)
        end_angle   = math.radians(angle_deg + 55)

        # Arco principal (amarelo brilhante)
        pygame.draw.arc(arc_surf, (255, 230, 60, alpha),
                        arc_rect, start_angle, end_angle, 6)
        # Halo externo mais suave
        outer_rect = arc_rect.inflate(6, 6)
        pygame.draw.arc(arc_surf, (255, 180, 30, alpha // 2),
                        outer_rect, start_angle, end_angle, 3)

        self.window.blit(arc_surf, (0, 0))

    def _draw_hud(self):
        pygame.draw.rect(self.window, C_DARK, (0, 0, WIN_WIDTH, ARENA_TOP))
        pygame.draw.line(self.window, C_GRAY, (0, ARENA_TOP), (WIN_WIDTH, ARENA_TOP), 1)

        self._draw_lives()

        seconds = max(0, self.timeout // 1000)
        color   = C_RED if seconds <= 10 else C_WHITE
        self._hud_text(f"TEMPO: {seconds:02d}s", color,   (WIN_WIDTH // 2, ARENA_TOP // 2))

        enemy_count = sum(1 for e in self.entity_list if isinstance(e, Enemy))
        self._hud_text(f"INIMIGOS: {enemy_count}", C_ORANGE,
                       (WIN_WIDTH - 10, ARENA_TOP // 2), anchor='right')

    def _draw_lives(self):
        heart_color = C_RED
        empty_color = C_GRAY
        size, gap, x0, y = 14, 6, 14, ARENA_TOP // 2

        for i in range(PLAYER_LIVES):
            cx    = x0 + i * (size + gap)
            color = heart_color if i < self.player.lives else empty_color
            r     = size // 2
            pygame.draw.circle(self.window, color, (cx - r // 2, y - 2), r // 2 + 1)
            pygame.draw.circle(self.window, color, (cx + r // 2, y - 2), r // 2 + 1)
            pygame.draw.polygon(self.window, color, [
                (cx - r, y - 2), (cx + r, y - 2), (cx, y + r + 1)
            ])

    def _hud_text(self, text, color, pos, anchor='center'):
        font = pygame.font.SysFont('Arial', 16, bold=True)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if anchor == 'center':
            rect.center = pos
        elif anchor == 'right':
            rect.midright = pos
        else:
            rect.midleft = pos
        self.window.blit(surf, rect)
