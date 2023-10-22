import copy
import pygame
from particles import Particle
from settings import *


class Enemy:
    # parent enemy class for all
    def __init__(self, image: pygame.surface, position: pygame.Vector2):
        self.image = image
        # enemy image
        self.rect = self.image.get_rect()
        # enemy rect
        self.rect.topleft = position
        # enemy position -> what it actually is
        self.position = position
        
        self.type = "enemy"

    def draw(self, display: pygame.Surface):
        self.rect.topleft = self.position
        # if self.image is none, the enemy has been deleted
        # if you try to blit a deleted image the code crashes
        
        if self.image != None:
            # if image does not exist, then do not draw
            # change the bounds of the rect to the new enemy position
            display.blit(self.image, self.rect.topleft)
            # blit the image
            
    def draw_particles(self, display):
        Particle.simulate_system(self.particles, display)

    def collide(self, player, powerup_holder):
        if self.image is not None and self.rect.colliderect(player.rect):            
            player.health -= 1
            self.image = None
            if len(powerup_holder.held_powerups) > 0:
                match powerup_holder.held_powerups[-1]:
                    case "double_jump":
                        player.can_double_jump = False
                    case "dash":
                        player.can_dash = False
                
                del powerup_holder.held_powerups[-1]

            self.particles = Particle.generate_system((128, 15, 27), self.rect.center, 5, 5, 0.9, 10)

class Walker(Enemy):
    def __init__(self, image: pygame.Surface, position: pygame.Vector2, move_speed: int = 2):
        super().__init__(image, position)

        self.left_right_move_amt = 1
        # number of tiles the enemy can be moved left or right
        # used to keep game uniform
        
        self.anchor_position = copy.deepcopy(position)

        self.move_speed = move_speed
        # speed at which the enemy travels
        self.direction = "right"
        # direction is just left or right as a string
        
        self.max_left = self.anchor_position.x - (self.left_right_move_amt * BLOCK_SIZE)
        self.max_right = (self.anchor_position.x + BLOCK_SIZE) + (self.left_right_move_amt * BLOCK_SIZE)

    def enemy_behaviour(self):
        self.max_left = self.anchor_position.x - (self.left_right_move_amt * BLOCK_SIZE)
        self.max_right = (self.anchor_position.x + BLOCK_SIZE) + (self.left_right_move_amt * BLOCK_SIZE)
        
        if self.direction == "right" and self.rect.right < self.max_right:
            self.position.x += self.move_speed
            
        if self.direction == "left" and self.rect.left > self.max_left:
            self.position.x -= self.move_speed
        
        if self.rect.right >= self.max_right: self.direction = "left"
        if self.rect.left <= self.max_left: self.direction = "right"