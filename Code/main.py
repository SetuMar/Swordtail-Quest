import pygame
import sys
# import sys and pygame

from settings import *
# import settings

import level_loader
import player
# import game scripts

pygame.init()
# initialize pygame

display = pygame.display.set_mode(SCREEN_SIZE)
# display
clock = pygame.time.Clock()
# clock -> allows for updating

player_character = player.Player(pygame.Vector2(200, 300))
# player

tiles = level_loader.generate_level("/Users/setumarathe/Desktop/coding/Waterloo Game/Graphics/Levels/1.tmx")
# get the tiles for the current level

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
    
    for t in tiles:
        t.draw(display)
    # draw all tiles in the level

    pygame.display.update()
    clock.tick(FPS)
    # update the display