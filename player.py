import pygame
from settings import *

class Player:
    def __init__(self, position:pygame.Vector2, move_speed:int = 10) -> None:
        self.image = pygame.Surface(BLOCK_SIZE)
        self.image.fill((255, 0, 0))
        # replace with sprite ASAP
        
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        self.move_speed = move_speed
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        self.rect.x += (keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY]) * self.move_speed
    
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
        # draw player onto display