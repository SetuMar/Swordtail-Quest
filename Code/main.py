import math
import time
import pygame
import sys
# import sys and pygame

from settings import *

import player
import level_handler

from powerups import *
from ui import PowerupHolder

import block

pygame.init()
# initialize pygame

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# display

clock = pygame.time.Clock()
# clock -> allows for updating

prev_time = time.time()
# time of previous frame update

player_character = player.Player()
# player

game_level_handler = level_handler.GameOverHandler()

tiles, player_character.rect.topleft = game_level_handler.generate_level()
# get the tiles for the current level

powerup_display = PowerupHolder(pygame.Vector2(100, 100))

block.Tile.determine_level_length(tiles)
block.Tile.block_shift(tiles, player_character)

while True:
    display.fill('blue')
    # clear background to allow for drawing of next frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    block.Tile.dimensions = {
        "left":math.inf,
        "top":math.inf,
        "right":-math.inf,
        "bottom":-math.inf
    }

    for layer, layer_tiles in tiles.items():
    # go through all tile layers and the tiles on the layer
        for t in layer_tiles:
        # go through each tile in the layer
            block.Tile.determine_bounds(t)
            if t.image != None and t.rect.left < SCREEN_WIDTH and t.rect.right > 0:
                # so long as the tile is in bounds and the image can be drawn (exists):
                
                if layer in Powerup.powerup_layer_names: t.collide(player_character, powerup_display)
                # check powerup collision
                
                if "enemy" in layer:
                    t.collide(player_character, powerup_display)
                    # check for enemy collision
                    t.enemy_behaviour()
                    # conduct enemy behaviour
                    
                t.draw(display)
                # draw the tile
                
    if not game_level_handler.current_level_completed:
        game_level_handler.current_level_completed = player_character.update(tiles)
        # update the player
        # if there is a collision between the player and a green flag, then change the level
    
    player_character.draw(display)
    # draw the player
    
    if player_character.health <= 0:
    # if the player health is completed
    
        level_data = game_level_handler.restart_level(tiles, player_character)
        # get the data for the current level
        
        if level_data != None:
            tiles = level_data
            # resets the positions of the tiles back to what they were at the start

    if game_level_handler.current_level_completed:
    # if the level is completed
        
        next_level_data = game_level_handler.complete_level(tiles, player_character)
        # get the data for the next level
        
        if next_level_data != None:
            tiles = next_level_data
            # set the tiles in this level the ones the data has been collected for
            
    powerup_display.draw(display)
    
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