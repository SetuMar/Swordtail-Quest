import pygame
import sys
# import sys and pygame

from settings import *
# import settings

import level_loader
import player
# import game scripts
from powerups import *
pygame.init()
# initialize pygame

display = pygame.display.set_mode(SCREEN_SIZE)
# display
clock = pygame.time.Clock()
# clock -> allows for updating

player_character = player.Player(pygame.Vector2(200, 600))
# player

tiles = level_loader.generate_level(r"C:\Users\bpas2\OneDrive\Desktop\hackathon\waterloo-cs-proj-main\Graphics\levels\1.tmx")
# get the tiles for the current level
double_test = Double_jump()
while True:
    display.fill('white')
    # clear background to allow for drawing of next frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # check for exiting the window
    
    player_character.update(tiles)
    # update the player
    player_character.draw(display)
    # draw the player
    
    for layer, layer_tiles in tiles.items():
        for t in layer_tiles:
            if t.rect.left < SCREEN_WIDTH and t.rect.right > 0:
                t.draw(display)
    # draw all tiles in the level
    double_test.draw(display)
    double_test.collide(player_character)
    pygame.display.update()
    clock.tick(FPS)
    # update the display