import time
import pygame
import sys
# import sys and pygame

from settings import *

import level_loader
import player

from powerups import *

pygame.init()
# initialize pygame

display = pygame.display.set_mode(SCREEN_SIZE)
# display

clock = pygame.time.Clock()
# clock -> allows for updating

prev_time = time.time()

player_character = player.Player(pygame.Vector2(0, 0))
# player

tiles = level_loader.generate_level(r"Graphics/Levels/test.tmx")
# get the tiles for the current level
while True:
    display.fill('black')
    # clear background to allow for drawing of next frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    player_character.update(tiles, display)
    # update the player
    player_character.draw(display)
    # draw the player
    
    for layer, layer_tiles in tiles.items():
        for t in layer_tiles:
            if t.image != None and t.rect.left < SCREEN_WIDTH and t.rect.right > 0:
                if layer in Powerup.powerup_layer_names: t.collide(player_character)
                t.draw(display)
    
    current_time = time.time()
    # current time
    difference = current_time - prev_time
    # difference between current time and the previous time measured
    delay = max(1.0/FPS - difference, 0)
    # check if we need to wait to ensure 60 FPS
    time.sleep(delay)
    # wait the delay
    calculated_fps = 1.0/(delay + difference)
    # the FPS we have calculated
    prev_time = current_time
    # set previous time to current time
    pygame.display.set_caption("FRAME RATE: " + str(int(calculated_fps)))
    # update the caption
    pygame.display.update()
    clock.tick(FPS)
    # update the display