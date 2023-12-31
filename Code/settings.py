import pygame
# import pygame
from screeninfo import get_monitors
# get monitor size -> pip install screeninfo

# SCREEN_WIDTH = get_monitors()[0].width
# SCREEN_HEIGHT = get_monitors()[0].height

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# screen dimensions

FPS = 60
# FPS of game (frames per second)

BLOCK_SIZE = 64
# 32 x 32 size for each block

MOVE_LEFT_KEY = ord("a")
MOVE_RIGHT_KEY = ord("d")
JUMP_KEY = ord("w")
DASH_KEY = pygame.K_SPACE
MAC_DASH_KEY = pygame.K_SPACE
# keys used for movement