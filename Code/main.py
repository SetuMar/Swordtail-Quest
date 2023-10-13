import time
import pygame
import sys
# import sys and pygame

from settings import *

import player
import level_handler

from powerups import *

pygame.init()
# initialize pygame

display = pygame.display.set_mode(SCREEN_SIZE)
# display

clock = pygame.time.Clock()
# clock -> allows for updating

prev_time = time.time()

player_character = player.Player()
# player

game_level_handler = level_handler.GameOverHandler()

tiles, player_character.rect.topleft = game_level_handler.generate_level()
# get the tiles for the current level

while True:
    display.fill('black')
    # clear background to allow for drawing of next frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if not game_level_handler.current_level_completed:
        game_level_handler.current_level_completed = player_character.update(tiles)
        # update the player
        # if there is a collision between the player and a green flag, then change the level
    
    player_character.draw(display)
    # draw the player

    for layer, layer_tiles in tiles.items():
        for t in layer_tiles:
            if t.image != None and t.rect.left < SCREEN_WIDTH and t.rect.right > 0:
                if layer in Powerup.powerup_layer_names: t.collide(player_character)
                if "enemy" in layer:
                    t.collide(player_character)
                    t.enemy_behaviour()
                    
                t.draw(display)

    if game_level_handler.current_level_completed:
        next_level_data = game_level_handler.complete_level(tiles, player_character)
        if next_level_data != None:
            tiles = next_level_data
    
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