import pygame
from settings import *

class Player:
    def __init__(self, position:pygame.Vector2, move_speed:int = 7, fall_speed = 0.8, jump_speed = -12) -> None:
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill((255, 0, 0))
        # replace with sprite ASAP
        
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        self.move_speed = move_speed
        self.fall_speed = fall_speed
        self.jump_speed = jump_speed
        
        self.can_jump = False
        
        self.direction = pygame.Vector2(0, 0)
        
    def update(self, tiles:list):
        keys = pygame.key.get_pressed()
        
        self.direction.x = (keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY]) * self.move_speed
        
        self.rect.x += self.direction.x
        
        def vertical_movement():
            if keys[JUMP_KEY] and self.can_jump:
                self.direction.y = self.jump_speed
                self.can_jump = False
                
            self.direction.y += self.fall_speed                
            self.rect.y += self.direction.y
            
            collision_detected = False
            
            for t in tiles:
                if self.rect.colliderect(t.rect):
                    if self.direction.y > 0 and self.rect.top < t.rect.top:
                        self.rect.bottom = t.rect.top
                        self.direction.y = 0
                        self.can_jump = True
                        collision_detected = True
                        
            if not collision_detected: self.can_jump = False
                        
        vertical_movement()
            
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
        # draw player onto display