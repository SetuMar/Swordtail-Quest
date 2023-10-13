import pygame

import timer_global
from keys import KeyData

from settings import *

# TODO: USE A LERP IN THE DASH IN ORDER TO MAKE IT SMOOTHER

class Player:
    def __init__(self, position:pygame.Vector2 = pygame.Vector2(0, 0), move_speed:int = 8, fall_speed:int = 0.5, jump_speed:int = -12, dash_speed = 30, camera_move_distance:int = 200) -> None:
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill((255, 0, 0))
        # replace with sprite ASAP
        
        self.rect = self.image.get_rect()
        # generate rectangle from player sprite
        self.rect.topleft = position
        # place the player at the position designated
        
        self.normal_move_speed = move_speed
        self.move_speed = move_speed
        # player move speed
        self.fall_speed = fall_speed
        # player fall speed
        
        self.can_jump = False
        # if the player can jump
        self.jump_speed = jump_speed
        # player jump speed
        self.direction = pygame.Vector2(0, 0)
        # direction of movement (on x and y axes)

        self.free_movement_region = (camera_move_distance, SCREEN_WIDTH - camera_move_distance)
        # area of free movement before camera start to move as well
        
        self.num_jumps = 0
        # how many jumps the player is able to perform 
        # either 0 - none, 1 - 1 jump, or 2 - double jump
        self.can_double_jump = False
        # if the player can double jump
        
        self.dash_speed = dash_speed
        # speed at which the player dashes
        self.can_dash = False
        # if the player can dash
        self.in_dash = False
        # if the player is in dash
        dash_timer = 0.2
        # how long each individual dash lasts
        self.dash_timer = timer_global.Timer(dash_timer)
        # timer for each dash length
        self.dash_cooldown_completed = True
        # if the cooldown for the dash has been completed
        
        dash_cooldown = 5
        # how long the cooldown should last
        self.dash_cooldown_timer = timer_global.Timer(dash_cooldown)
        # dash cooldown timer

        self.key_data = KeyData()
        # pressed and held key data
        
    def update(self, tiles:dict):
        def horizontal_movement():
            self.direction.x = (self.key_data.get_key_on_hold(MOVE_RIGHT_KEY) - self.key_data.get_key_on_hold(MOVE_LEFT_KEY)) * self.move_speed
            # move the player in the x and y axes
            # multiply by scalar of move speed
            
            if self.key_data.get_key_on_keydown(DASH_KEY) and self.direction.x != 0 and self.can_dash and self.dash_cooldown_completed:
            # if dash key is pressed and rh
                self.move_speed = self.dash_speed
                # set the play speed as the dash speed
                self.in_dash = True
                # set the player in dash
                
            if self.in_dash:
                # if the player is in dash
                if self.dash_timer.time_check() or self.direction.x == 0:
                    # if they dash for the stated legal time or exit the dash early by not moving on the axes:
                    self.move_speed = self.normal_move_speed
                    # change the move speed back to normal
                    self.dash_cooldown_completed = False
                    # require player to cooldown dash
                    self.in_dash = False
                    # player is no longer in dash
                    
            if not self.dash_cooldown_completed:
            # if the dash cooldown isn't completed
                if self.dash_cooldown_timer.time_check():
                # wait the cooldown period
                    self.dash_cooldown_completed = True
                    # set the cooldown to completed
            
            if ((self.rect.right > self.free_movement_region[1]) and (self.direction.x > 0) or (self.rect.left < self.free_movement_region[0]) and (self.direction.x < 0)):
            # if the player is trying to move outside of the free_movement_region
                for tile_layer, tile_list in tiles.items():
                    for t in tile_list:
                        if "enemy" in tile_layer: t.anchor_position.x -= self.direction.x
                        t.rect.x -= self.direction.x
                # move the tiles instead of the player
            else:
                self.rect.x += self.direction.x
                # otherwise just move the player
            
            for t in tiles["outline"]:
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
            if self.key_data.get_key_on_keydown(JUMP_KEY) and self.num_jumps > 0: 
                # if JUMP_KEY pressed and the player is allowed to jump (has jumps available)
                self.direction.y = self.jump_speed
                # set y-direction to jump_speed
                #Check whether this is a jump or a double jump
                self.can_jump = False
                #remove ability to jump until landing
                self.num_jumps -= 1
            
            self.direction.y += self.fall_speed
            # add gravity to y-direction 
            self.rect.y += self.direction.y
            # move the player by the y-direction on the y axis
            
            floor_collision_detected = False
            # if a floor direction has been detected
            
            for t in tiles["outline"]:
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
                        self.num_jumps = 1 + (1 * self.can_double_jump)
                        # reset jump (add double jump if allowed)                   
                        floor_collision_detected = True
                        # a collision has been detected
                    
                    elif (self.direction.y < 0) and (self.rect.top > t.rect.top):
                        self.rect.top = t.rect.bottom
                        self.direction.y = 0
                        
            if not floor_collision_detected: self.can_jump = False
            # if a floor is not detected, then do not allow jump

        horizontal_movement()
        # move horizontally (and collisions)
        if not self.in_dash: vertical_movement()
        # move vertically (and collisions)
        
        return self.rect.colliderect(tiles["completed"][0])
            
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
        # draw player onto display