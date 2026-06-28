# Window
import pygame


WIN_WIDTH = 800
WIN_HEIGHT = 600

# A
ARENA_TOP    = 60
ARENA_LEFT   = 0
ARENA_RIGHT  = WIN_WIDTH
ARENA_BOTTOM = WIN_HEIGHT
ASSET_PATH = './assets/'

# C
COLOR_DARK_ORANGE = (200, 80, 0)
COLOR_MENU_TITLE = (45, 25, 60)
C_WHITE = (255, 255, 255)
C_BLACK   = (0,   0,   0)
C_RED     = (220, 50,  50)
C_YELLOW  = (255, 220, 50)
C_GREEN   = (50,  200, 80)
C_ORANGE  = (255, 140, 0)
C_GRAY    = (120, 120, 120)
C_DARK    = (30,  30,  30)

# E
ENTITY_HEALTH = {
    'Player':    1,
    'Enemy1':    2,
    'Enemy2':    3,
    'Sword':     1,
    'EnemyShot': 1,
}

ENTITY_DAMAGE = {
    'Player':    0,
    'Enemy1':    1,
    'Enemy2':    1,
    'Sword':     1,
    'EnemyShot': 1,
}

ENTITY_SPEED = {
    'Player':    4,
    'Enemy1':    2,
    'Enemy2':    3,
    'Sword':     0,
    'EnemyShot': 5,
}
# F
FPS = 60

# M
MENU_OPTION = ('JOGAR', 'SAIR')

# P
PLAYER_KEYS = {
    'up':     [pygame.K_w,    pygame.K_UP],
    'down':   [pygame.K_s,    pygame.K_DOWN],
    'left':   [pygame.K_a,    pygame.K_LEFT],
    'right':  [pygame.K_d,    pygame.K_RIGHT],
    'attack': [pygame.K_SPACE],
}
PLAYER_LIVES = 3


# S
SWORD_DURATION = 12
SWORD_OFFSET   = 40
SWORD_COOLDOWN = 30