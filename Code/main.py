import pygame
import sys
from settings import *
import level_loader

import player

pygame.init()

display = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

player_character = player.Player(pygame.Vector2(200, 200))

tiles = level_loader.generate_level("/Users/setumarathe/Desktop/coding/Waterloo Game/Graphics/Levels/1.tmx")

while True:
    display.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    player_character.update()
    player_character.draw(display)
    
    for t in tiles:
        t.draw(display)

    pygame.display.update()
    clock.tick(FPS)