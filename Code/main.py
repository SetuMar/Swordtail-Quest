import math
import time
import pygame
import sys
import keyboard
# import sys and pygame
from settings import *
from keys import KeyData

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
# initialize pygame sound

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

current_file = pl.Path(__file__)
parent_directory = current_file.parent.parent
graphics_path = pl.Path(parent_directory / 'Graphics')

music_path = pl.Path(parent_directory / 'Music')


def load_bg():
    if game_level_handler.level_number < 3:
        path = pl.Path(graphics_path / "backgrounds/forest_background.png")

    if 2 < game_level_handler.level_number < 5:
        path = pl.Path(graphics_path / "backgrounds/pirate_bay_background.png")

    if 4 < game_level_handler.level_number < 7:
        path = pl.Path(graphics_path / "backgrounds/volcano_background.png")

    if 6 < game_level_handler.level_number:
        path = pl.Path(graphics_path / "backgrounds/ice_background.png")

    background = pygame.transform.scale(pygame.image.load(path), (SCREEN_WIDTH, SCREEN_HEIGHT))

    return background


# Load Title Screen
title_path = pl.Path(graphics_path / "transitions/title_screen.png")
title_screen = pygame.transform.scale(pygame.image.load(title_path), (SCREEN_WIDTH, SCREEN_HEIGHT))
display.blit(title_screen, (0, 0))
pygame.display.update()

while True:
    if keyboard.is_pressed("space"):

        background = load_bg()

        proceed_to_level_load = False
        global llplayed
        llplayed = False
        mPlaying = False
        while True:
            if not mPlaying:
                if game_level_handler.level_number < 3:

                    pygame.mixer.music.load(music_path / "Forest_Theme.mp3")
                    pygame.mixer.music.play(-1)
                    mPlaying = True
                elif 2 < game_level_handler.level_number < 5:
                    pygame.mixer.music.load(music_path / "Pirate_Theme.mp3")
                    pygame.mixer.music.play(-1)
                    mPlaying = True

                elif 4 < game_level_handler.level_number < 7:
                    pygame.mixer.music.load(music_path / "Volcano_Theme.mp3")
                    pygame.mixer.music.play(-1)
                    mPlaying = True

                elif 6 < game_level_handler.level_number:
                    pygame.mixer.music.load(music_path / "Ice_Theme.mp3")
                    pygame.mixer.music.play(-1)
                    mPlaying = True

            display.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            block.Tile.dimensions = {
                "left": math.inf,
                "top": math.inf,
                "right": -math.inf,
                "bottom": -math.inf
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

            if player_character.health <= 0 or game_level_handler.current_level_completed or (
                    player_character.rect.bottom - BLOCK_SIZE) >= SCREEN_HEIGHT:
                # if the player health is completed

                level_data = None

                restart_path = pl.Path(graphics_path / "transitions/restart.png")
                restart_screen = pygame.transform.scale(pygame.image.load(restart_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

                level_cleared_path = pl.Path(graphics_path / "transitions/level_cleared.png")
                level_cleared_screen = pygame.transform.scale(pygame.image.load(level_cleared_path),
                                                              (SCREEN_WIDTH, SCREEN_HEIGHT))

                if player_character.health <= 0 or (player_character.rect.bottom - BLOCK_SIZE) >= SCREEN_HEIGHT:
                    if not llplayed:
                        llplayed = True
                        pygame.mixer.Sound.play(loseLifeSound)
                        pygame.mixer.music.stop()
                    display.blit(restart_screen, (0, 0))

                    proceed_to_level_load = in_between_level_display.draw("", display)
                    if proceed_to_level_load:
                        level_data = game_level_handler.restart_level(tiles, player_character)
                        pygame.mixer.music.stop()
                        mPlaying = False
                # get the data for the current level

                if game_level_handler.current_level_completed and game_level_handler.level_number < 9:
                    display.blit(level_cleared_screen, (0, 0))
                    proceed_to_level_load = in_between_level_display.draw("", display)
                    if proceed_to_level_load:
                        pygame.mixer.music.stop()
                        mPlaying = False
                        level_data = game_level_handler.complete_level(tiles, player_character)

                elif game_level_handler.level_number == 9:
                    pygame.mixer.music.stop()
                    credit_path = pl.Path(graphics_path / "transitions/credit_screen.png")
                    credit_screen = pygame.transform.scale(pygame.image.load(credit_path),
                                                           (SCREEN_WIDTH, SCREEN_HEIGHT))
                    display.blit(credit_screen, (0, 0))

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

            delay = max(1.0 / FPS - difference, 0)
            # check if we need to wait to ensure 60 FPS

            time.sleep(delay)
            # wait the delay

            calculated_fps = 1.0 / (delay + difference)
            # the FPS we have calculated

            prev_time = current_time
            # set previous time to current time

            pygame.display.set_caption("FRAME RATE: " + str(int(calculated_fps)))
            # update the caption

            pygame.display.update()
            clock.tick(FPS)
            # update the display
