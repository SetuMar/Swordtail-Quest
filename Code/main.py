import time
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

prev_time = time.time()

player_character = player.Player(pygame.Vector2(0, 0))
# player

tiles = level_loader.generate_level(r"Graphics/Levels/1.tmx")
# get the tiles for the current level

double_test = Powerup(r"Graphics/doublejumpplaceholder.png", pygame.Vector2(200, 400), "double_jump")

# #this is a test doublejump object
# dash_test = Dash()
# #this is a test dash object
# #define refresh_dash as a pygame event(to let it work on a timer)
# refresh_dash = pygame.USEREVENT + 1
# #let player dash again after every 4 seconds
# pygame.time.set_timer(refresh_dash,4000)

while True:
    display.fill('black')
    # clear background to allow for drawing of next frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # check for exiting the window
    
        # if event.type == refresh_dash:
        #     if player_character.has_dash:
        #         player_character.can_dash = True
    
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
    #draw in the doublejump object
    double_test.collide(player_character)
    #check for doublejump collisions
    # dash_test.draw(display)
    # #draw in the dash object
    # dash_test.collide(player_character)
    #check for dash collisions
    
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