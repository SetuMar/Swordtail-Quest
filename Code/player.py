import time
import pygame

import timer
from keys import KeyData

from settings import *

import math

# TODO: USE A LERP IN THE DASH IN ORDER TO MAKE IT SMOOTHER

class Player:
    def __init__(self, position:pygame.Vector2, move_speed:int = 8, fall_speed:int = 0.5, jump_speed:int = -12, dash_tile_distance = 10, camera_move_distance:int = 200) -> None:
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
        double_jump_powerup_length = 3
        # how long the powerup should last
        self.double_jump_timer = timer.Timer(double_jump_powerup_length)
        # timer for powerup length
        
        self.can_dash = False
        # if player is allowed to dash
        self.dash_tile_distance = dash_tile_distance
        # the distance the player traverses each dash
        self.is_dashing = False
        # if the player is currently dashing
        dash_powerup_length = 5
        # how long the powerup should last
        self.dash_timer = timer.Timer(dash_powerup_length)
        # timer for powerup length

        self.key_data = KeyData()
        # pressed and held key data
        
    def update(self, tiles:dict, display):
        def horizontal_movement():
            h_direction = (self.key_data.get_key_on_hold(MOVE_RIGHT_KEY) - self.key_data.get_key_on_hold(MOVE_LEFT_KEY)) * self.move_speed
            # move the player in the x and y axes
            # multiply by scalar of move speed
            
            if self.can_dash:
            # if the player can dash
                if self.dash_timer.time_check():
                # wait until the time is up for dashing
                    self.can_dash = False
                    # stop letting player dash
            
            if self.key_data.get_key_on_keydown(DASH_KEY) and self.direction.x != 0 and self.can_dash:
            # if dash key pressed and the player is holding a direction key and the player has the ability to dash
                self.direction.y = 0
                # set y direction to 0 (stop anything weird from happening on the y axis)
                dash_rect = pygame.Rect(0, self.rect.y - 1, 20, 20)
                # create a smaller rectangle used for simulating the dash distance
                dash_direction = math.copysign(1, self.direction.x)
                # the direction of the dash's movement
                
                if dash_direction < 0: dash_rect.left = self.rect.left - 1
                if dash_direction > 0: dash_rect.right = self.rect.right + 1
                # place the dash rectangle to the side where the movement is occuring
                
                for i in range(0, self.dash_tile_distance):
                # for each section of tile distance
                    collision_detected = False
                    # check for a collision
                    dash_rect.x += dash_direction * BLOCK_SIZE
                    # move the dash rectangle
                    
                    for t in tiles["outline"]:
                    # loop through tiles
                        if dash_rect.colliderect(t.rect):
                            collision_detected = True
                            break
                        # check for a collision (where to end dash)
                    
                    if collision_detected: break
                    # break if collision detected to end dash
                
                if dash_rect.left > self.free_movement_region[0] and dash_rect.right < self.free_movement_region[1]:
                # check if end of dash is within free_movement_region
                    if dash_direction < 0: 
                        self.rect.right = dash_rect.right
                        
                    if dash_direction > 0: 
                        self.rect.left = dash_rect.left
                    # place the rectangle at the end of the dash position
                else:
                # if dash ends outside of the free_movement_region
                    tile_x_offset = 0
                    # amount to offset the tiles by
                    
                    if dash_direction < 0: 
                        self.rect.left = self.free_movement_region[0] + 1
                        tile_x_offset = self.free_movement_region[0] - dash_rect.left
                        
                    if dash_direction > 0: 
                        self.rect.left = self.free_movement_region[1] - 1
                        tile_x_offset = -(dash_rect.left - self.free_movement_region[1])
                    # determine how much to offset the tiles by
                    
                    for layer, layer_tiles in tiles.items():
                        for t in layer_tiles:
                            t.rect.x += tile_x_offset
                    # offset all of the tiles
            else:
                self.direction.x = h_direction
                # if no dash, then just move the player
            
            if ((self.rect.right > self.free_movement_region[1]) and (self.direction.x > 0) or (self.rect.left < self.free_movement_region[0]) and (self.direction.x < 0)):
            # if the player is trying to move outside of the free_movement_region
                for tile_list in tiles.values():
                    for t in tile_list:
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
            if self.can_double_jump:
                if self.double_jump_timer.time_check():
                    self.num_jumps = 1
                    self.can_double_jump = False
                
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
        vertical_movement()
        # move vertically (and collisions)
            
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
        # draw player onto display