import pygame
from settings import *

class Enemy:
    # parent enemy class for all
    def __init__(self,image:pygame.surface, position:pygame.Vector2):
        self.image = image
        # enemy image
        self.rect = self.image.get_rect()
        # enemy rect
        self.rect.topleft = position
        # enemy position -> what it actually is
        
        self.anchor_position = position

    def draw(self, display:pygame.Surface):
        # if self.image is none, the enemy has been deleted
        # if you try to blit a deleted image the code crashes
        if self.image != None:
        # if image does not exist, then do not draw
            # change the bounds of the rect to the new enemy position
            display.blit(self.image, self.rect.topleft)
            # blit the image
            
    def collide(self, player):
        if self.image is not None and self.rect.colliderect(player.rect):
            self.image = None
            # TODO: Currently, player kills enemy on contact. replace this later
            
class Walker(Enemy):
    def __init__(self, image:pygame.Surface, position:pygame.Vector2, move_speed:int = 2):
        super().__init__(image, position)
        
        self.left_right_move_amt = 3
        # number of tiles the enemy can be moved left or right
            # used to keep game uniform
        
        self.left_boundary = self.anchor_position.x - BLOCK_SIZE * self.left_right_move_amt
        self.right_boundary = self.anchor_position.x + BLOCK_SIZE * self.left_right_move_amt
        # left and right boundaries of enemy movement
        
        self.move_speed = move_speed
        # speed at which the enemy travels
        self.direction = "right"
        # direction is just left or right as a string
        
    def enemy_behaviour(self):
        self.left_boundary = self.anchor_position.x - BLOCK_SIZE * self.left_right_move_amt
        self.right_boundary = self.anchor_position.x + BLOCK_SIZE * self.left_right_move_amt
        # left and right boundaries of enemy movement
        
        if self.direction == "right":
        # If the walker is walking right
        # and moving right would not put the walker over its boundary
            
            if self.rect.right < self.right_boundary - self.move_speed:
            # if the enemy has not yet reached the right boundary, make it move right
                self.rect.x += self.move_speed
                # move the walker right by its move speed
            else: self.direction = "left"
            # if moving would make the walker cross its boundary, make it go left
            
        else:
        # if the walker is moving left
        # Same logic as for right just opposite
            if self.rect.left > self.left_boundary + self.move_speed:
                self.rect.x -= self.move_speed
            else:
                self.direction = "right"