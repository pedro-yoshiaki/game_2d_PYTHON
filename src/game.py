#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from pygame import Surface

from src.Const  import WIN_WIDTH, WIN_HEIGHT, WIN_TITLE, FPS, MENU_OPTION
from src.Const  import C_WHITE, C_YELLOW, C_RED, C_GREEN, C_DARK, C_GRAY, C_ORANGE
from src.menu   import Menu
from src.level  import Level


class Game:
    """
    Gerenciadora central: inicializa o pygame e orquestra o fluxo
    Menu → Level → Tela de resultado → Menu.
    """

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(WIN_TITLE)

    # ── Loop eterno ───────────────────────────────────────────────────────────
    def run(self):
        while True:
            menu        = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:   # 'JOGAR'
                level  = Level(self.window)
                result = level.run()             # True = vitória, False = derrota
                self._show_result(result)

            elif menu_return == MENU_OPTION[1]:  # 'SAIR'
                pygame.quit()
                sys.exit()

    # ── Tela de resultado ─────────────────────────────────────────────────────
    def _show_result(self, victory: bool):
        """
        Exibe tela de VITÓRIA ou GAME OVER por 3 segundos e retorna ao menu.
        """
        clock = pygame.time.Clock()
        timer = 180   # 3 s a 60 fps

        if victory:
            title    = 'VITÓRIA!'
            subtitle = 'Você sobreviveu à arena!'
            color    = C_GREEN
        else:
            title    = 'GAME OVER'
            subtitle = 'Suas vidas acabaram...'
            color    = C_RED

        while timer > 0:
            clock.tick(FPS)
            timer -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return   # qualquer tecla pula a tela

            # Fundo escuro
            self.window.fill((15, 15, 15))

            # Painel central
            panel_w, panel_h = 440, 200
            panel_x = (WIN_WIDTH  - panel_w) // 2
            panel_y = (WIN_HEIGHT - panel_h) // 2
            pygame.draw.rect(self.window, (30, 30, 30),
                             (panel_x, panel_y, panel_w, panel_h), border_radius=12)
            pygame.draw.rect(self.window, color,
                             (panel_x, panel_y, panel_w, panel_h),
                             2, border_radius=12)

            cx = WIN_WIDTH // 2
            self._text(title,    48, color,   (cx, panel_y + 70),  bold=True)
            self._text(subtitle, 20, C_WHITE, (cx, panel_y + 130))
            self._text('Pressione qualquer tecla para continuar', 13, C_GRAY,
                       (cx, panel_y + 175))

            # Barra de progresso mostrando o tempo restante
            bar_w = int((timer / 180) * (panel_w - 40))
            pygame.draw.rect(self.window, color,
                             (panel_x + 20, panel_y + panel_h - 12, bar_w, 6),
                             border_radius=3)

            pygame.display.flip()

    def _text(self, text: str, size: int, color: tuple, pos: tuple, bold: bool = False):
        font = pygame.font.SysFont('Arial', size, bold=bold)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=pos)
        self.window.blit(surf, rect)
