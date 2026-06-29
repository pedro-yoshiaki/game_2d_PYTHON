#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from pygame import Surface
from pygame.font import Font

from src.Const import (
    WIN_WIDTH, WIN_HEIGHT, FPS,
    C_WHITE, C_YELLOW, C_ORANGE, C_GRAY, C_DARK, C_BLACK,
    MENU_OPTION, ASSET_PATH,
)


class Menu:
  
    # Constantes visuais do menu
    _BG_LAYERS = [
        {'file': 'background_menu/1.png', 'speed': 0.2},
        {'file': 'background_menu/2.png', 'speed': 0.5},
        {'file': 'background_menu/3.png', 'speed': 0.9},
        {'file': 'background_menu/4.png', 'speed': 1.4},
    ]
    _CONTROLS = [
        ('WASD  /  ←↑↓→',  'Mover o personagem'),
        ('ESPAÇO',          'Atacar com a espada / Proteger'),
        ('ENTER',           'Confirmar no menu'),
        ('ESC',             'Sair do jogo'),
    ]

    def __init__(self, window: Surface):
        self.window = window
        self.clock  = pygame.time.Clock()

        self.layers = []
        for layer in self._BG_LAYERS:
            surf = self._load_layer(layer['file'])
            
            self.layers.append({
                'surf':  surf,
                'speed': layer['speed'],
                'x':     0.0,
                'x2':    float(surf.get_width()),
            })

        try:
            pygame.mixer_music.load(ASSET_PATH + 'soundtrack/Menu_sound.mp3')
            pygame.mixer_music.set_volume(0.35)
            pygame.mixer_music.play(-1)
        except pygame.error:
            pass   

    def _load_layer(self, filename: str) -> Surface:
        try:
            surf = pygame.image.load(ASSET_PATH + filename).convert_alpha()
            
            ratio  = WIN_HEIGHT / surf.get_height()
            new_w  = int(surf.get_width() * ratio)
            return pygame.transform.scale(surf, (new_w, WIN_HEIGHT))
        except (pygame.error, FileNotFoundError):
            
            surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            surf.fill((20, 20, 40))
            return surf

    def run(self) -> str:
        selected = 0

        while True:
            self.clock.tick(FPS)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(MENU_OPTION)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        return MENU_OPTION[selected]
                    elif event.key == pygame.K_ESCAPE:
                        return MENU_OPTION[-1]

            self._draw(selected)
            pygame.display.flip()

    def _draw(self, selected: int):
        for layer in self.layers:
            layer['x']  -= layer['speed']
            layer['x2'] -= layer['speed']

            sw = layer['surf'].get_width()
            if layer['x'] + sw <= 0:
                layer['x'] = layer['x2'] + sw
            if layer['x2'] + sw <= 0:
                layer['x2'] = layer['x'] + sw

            self.window.blit(layer['surf'], (int(layer['x']),  0))
            self.window.blit(layer['surf'], (int(layer['x2']), 0))

        # Painel central semitransparente
        panel_w, panel_h = 500, 440
        panel_x = (WIN_WIDTH  - panel_w) // 2
        panel_y = (WIN_HEIGHT - panel_h) // 2
        panel   = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 160))
        self.window.blit(panel, (panel_x, panel_y))

        cx = WIN_WIDTH // 2

        # Título
        self._text('ARENA',    56, C_ORANGE,  (cx, panel_y + 55),  bold=True)
        self._text('SURVIVAL', 56, C_YELLOW,  (cx, panel_y + 115), bold=True)

        # Separador
        pygame.draw.line(self.window, C_GRAY,
                         (panel_x + 30, panel_y + 148),
                         (panel_x + panel_w - 30, panel_y + 148), 1)

        # Controles
        self._text('CONTROLES', 14, C_GRAY, (cx, panel_y + 170))
        for i, (key, desc) in enumerate(self._CONTROLS):
            y = panel_y + 192 + i * 22
            self._text(f'{key}', 14, C_YELLOW, (cx - 5, y), anchor='right')
            self._text(f'— {desc}', 14, C_WHITE,  (cx + 5, y), anchor='left')

        # Separador
        pygame.draw.line(self.window, C_GRAY,
                         (panel_x + 30, panel_y + 285),
                         (panel_x + panel_w - 30, panel_y + 285), 1)

        # Opções de menu
        for i, option in enumerate(MENU_OPTION):
            y     = panel_y + 315 + i * 48
            color = C_YELLOW if i == selected else C_WHITE
            size  = 28      if i == selected else 22
            self._text(option, size, color, (cx, y), bold=(i == selected))
            if i == selected:
                # Indicador de seleção
                self._text('►', 22, C_ORANGE, (cx - 120, y))
                self._text('◄', 22, C_ORANGE, (cx + 120, y))

        # Rodapé
        self._text('↑↓ para navegar   ENTER para selecionar', 12, C_GRAY,
                   (cx, panel_y + panel_h - 18))

    def _text(self, text: str, size: int, color: tuple, pos: tuple,
              bold: bool = False, anchor: str = 'center'):
        font = pygame.font.SysFont('Arial', size, bold=bold)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if anchor == 'center':
            rect.center = pos
        elif anchor == 'right':
            rect.midright = pos
        else:
            rect.midleft = pos
        self.window.blit(surf, rect)
