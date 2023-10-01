import pygame
# import pygame

from settings import *
# import settings

class Player:
    def __init__(self, position:pygame.Vector2, move_speed:int = 7, fall_speed:int = 0.8, jump_speed:int = -12) -> None:
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill((255, 0, 0))
        # replace with sprite ASAP
        
        self.rect = self.image.get_rect()
        # generate rectangle from player sprite
        self.rect.topleft = position
        # place the player at the position designated
        
        self.move_speed = move_speed
        # player move speed
        self.fall_speed = fall_speed
        # player fall speed
        self.jump_speed = jump_speed
        # player jump speed
        
        self.can_jump = False
        # if the player can jump
        
        self.direction = pygame.Vector2(0, 0)
        # direction of movement (on x and y axes)
        
    def update(self, tiles:list):
        keys = pygame.key.get_pressed()
        # pressed keys
        
        def horizontal_movement():
            self.direction.x = (keys[MOVE_RIGHT_KEY] - keys[MOVE_LEFT_KEY]) * self.move_speed
            # move the player in the x and y axes
            # multiply by scalar of move speed
            
            self.rect.x += self.direction.x
            # move the player by the direction
            
            for t in tiles:
            # loop through tiles
                if self.rect.colliderect(t.rect):
                # check for collision with tiles
                    
                    # check if the player has collided with a block to the side
                    
                    if self.direction.x > 0 and self.rect.right > t.rect.left:
                    # check collision for player too far right
                        self.rect.right = t.rect.left
                        # set the player's right to the left of the block (place at boundary)
                        self.direction.x = 0
                        # stop movement on the x for this frame
                    
                    elif self.direction.x < 0 and self.rect.left < t.rect.right:
                    # check collision for player too far left
                        self.rect.left = t.rect.right
                        # set the player's left to the right of the block (place at boundary)
                        self.direction.x = 0
                        # stop movement on the x for this frame
        
        def vertical_movement():
            if keys[JUMP_KEY] and self.can_jump:
            # if JUMP_KEY pressed and player and can_jump
                self.direction.y = self.jump_speed
                # set y-direction to jump_speed
                self.can_jump = False
                # don't allow to jump until hits flow
                
            self.direction.y += self.fall_speed
            # add gravity to y-direction 
            self.rect.y += self.direction.y
            # move the player by the y-direction on the y axis
            
            collision_detected = False
            # if a floor direction has been detected
            
            for t in tiles:
            # loop through tiles
                if self.rect.colliderect(t.rect):
                # check for collision with tiles
                
                    if (self.direction.y > 0) and (self.rect.top < t.rect.top):
                        # if the player is moving down and 
                        # the player's top is farther down than the top of the colliding block 
                        # (a collision was detected on the same level as the player)
                        
                        self.rect.bottom = t.rect.top
                        # place the player at the collided block
                        self.direction.y = 0
                        # stop moving the player down (no need for gravity)
                        self.can_jump = True
                        # allow the player to jump (he is on ground now)
                        collision_detected = True
                        # a collision has been detected
                        
            if not collision_detected: self.can_jump = False
            # if a floor is not detected, then do not allow jump
        
        horizontal_movement()
        # move horizontally (and collisions)
        vertical_movement()
        # move vertically (and collisions)
            
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
        # draw player onto display