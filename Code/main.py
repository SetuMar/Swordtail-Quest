import math
import time
import pygame
import sys
# import sys and pygame
from settings import *

import player
import level_handler

from powerups import *
import ui

import pathlib as pl

import block
from sounds import loseLifeSound
pygame.init()
# initialize pygame
pygame.mixer.init()
#initialize pygame sound

display = pygame.display.set_mode(SCREEN_SIZE)
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

in_between_level_display = ui.BetweenLevelHolderMenu()

powerup_display = ui.PowerupHolder()

block.Tile.determine_level_length(tiles)
block.Tile.block_shift(tiles, player_character)

def load_bg():
    if game_level_handler.level_number < 2: path = pl.Path("Graphics/backgrounds/forest_background.png")
    background = pygame.transform.scale(pygame.image.load(path), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    return background

background = load_bg()

proceed_to_level_load = False
global llplayed
llplayed = False
while True:
    display.blit(background, (0, 0))
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
            if t.image != None:
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
            else:
                if layer in Powerup.powerup_layer_names or "enemy" in layer: t.draw_particles(display)
                
    
    if player_character.health <= 0 or game_level_handler.current_level_completed or (player_character.rect.bottom - BLOCK_SIZE) >= SCREEN_HEIGHT:
    # if the player health is completed
        
        level_data = None
        
        if player_character.health <= 0 or (player_character.rect.bottom - BLOCK_SIZE) >= SCREEN_HEIGHT: 
            if not llplayed:
                llplayed = True
                pygame.mixer.Sound.play(loseLifeSound)
            proceed_to_level_load = in_between_level_display.draw("OH NO! PRESS SPACE TO RETRY.", display)
            if proceed_to_level_load: level_data = game_level_handler.restart_level(tiles, player_character)
        # get the data for the current level
        
        if game_level_handler.current_level_completed: 
            proceed_to_level_load = in_between_level_display.draw("LEVEL COMPLETE! PRESS SPACE TO CONTINUE.", display)
            if proceed_to_level_load: level_data = game_level_handler.complete_level(tiles, player_character)
        # get the data for the next level
        
        if level_data != None:
            powerup_display.held_powerups = []
            tiles = level_data
            in_between_level_display.key_pressed = False
            in_between_level_display.current_level_completed = False
            in_between_level_display.opacity_transition_completed = False
            in_between_level_display.opacity = 0
            # resets the positions of the tiles back to what they were at the start
            
        player_character.can_dash = False
        player_character.can_double_jump = False
        background = load_bg()

    else:
        game_level_handler.current_level_completed = player_character.update(tiles)
        # update the player
        # if there is a collision between the player and a green flag, then change the level
        llplayed = False
        player_character.draw(display)
        # draw the player
    
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