import pygame

import timer_global
from keys import KeyData

from settings import *
from block import Tile

from os import walk
from pathlib import Path
from sounds import jumpSound
class Player:
    def __init__(self, position: pygame.Vector2 = pygame.Vector2(0, 0), move_speed: int = 8, fall_speed: int = 0.5,
                 jump_speed: int = -12, dash_speed = 20, h_camera_move_distance: int = 200, v_camera_move_distance: int = 100) -> None:
        self.sprites = self.get_sprites(r"Graphics/Player Sprites")
        self.previous_image_state = "idle"
        self.image_state = "idle"
        self.frame_number = 0
        time_between_frames = 0.1
        self.animation_timer = timer_global.Timer(time_between_frames)
        
        self.look_dir = "right"
        
        self.image = self.sprites[self.image_state][0]
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

        # if the player can jump
        self.jump_speed = jump_speed
        # player jump speed
        self.direction = pygame.Vector2(0, 0)
        # direction of movement (on x and y axes)

        self.h_free_movement_region = (h_camera_move_distance, SCREEN_WIDTH - h_camera_move_distance)
        self.v_free_movement_region = (v_camera_move_distance, SCREEN_HEIGHT - v_camera_move_distance)
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
        
        self.prev_on_floor = True
        self.on_floor = True

        dash_cooldown = 1
        # how long the cooldown should last
        self.dash_cooldown_timer = timer_global.Timer(dash_cooldown)
        # dash cooldown timer

        self.key_data = KeyData()
        # pressed and held key data

        self.health = 1
        # player health
        
        self.h_lock_camera = False
        self.v_lock_camera = False
        
        self.powerup_history = []
        
    def get_sprites(self, sprites_location):
        sprites = {}
        sprites_location = Path(sprites_location)
        for path in sprites_location.iterdir():
            if path.is_dir():
                state_name = path.name
                sprites[state_name] = [pygame.image.load(str(image_path)) for image_path in path.iterdir()]
        return sprites


    def update(self, tiles: dict,) -> bool:        
        self.prev_on_floor = self.on_floor
        
        def horizontal_movement():
            self.direction.x = (self.key_data.get_key_on_hold(MOVE_RIGHT_KEY) - self.key_data.get_key_on_hold(
                MOVE_LEFT_KEY)) * self.move_speed
            # move the player in the x and y axes
            # multiply by scalar of move speed
            
            if self.direction.x != 0:
                self.look_dir = "left" if self.direction.x < 0 else "right"

            if self.can_dash:
                if self.key_data.get_key_on_keydown(DASH_KEY) and \
                self.direction.x != 0 and \
                self.can_dash and \
                self.dash_cooldown_completed:
                    # if dash key is pressed and the player is moving
                    # and the cooldown has completed and the player can dash
                    
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
                        
            if (self.direction.x < 0 and Tile.dimensions["left"] >= 0) or \
                (self.direction.x > 0 and Tile.dimensions["left"] <= -(Tile.level_length - SCREEN_WIDTH)):
                self.h_lock_camera = True
            else:
                self.h_lock_camera = False

            if (self.rect.right > self.h_free_movement_region[1] and self.direction.x > 0 or \
               self.rect.left < self.h_free_movement_region[0] and self.direction.x < 0) and \
                   not self.h_lock_camera:
                # if the player is trying to move outside the h_free_movement_region
                for tile_layer, tile_list in tiles.items():
                    for t in tile_list:
                        if "enemy" in tile_layer:
                            t.anchor_position.x -= self.direction.x
                        t.position.x -= self.direction.x
                # move the tiles instead of the player
            else:
                self.rect.x += self.direction.x
                # otherwise just move the player

            for t in tiles["outline"]:
                # loop through tiles
                if self.rect.colliderect(t.rect):

                    # check if the player has collided with a block to the side

                    if self.direction.x > 0:
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
            if self.key_data.get_key_on_keydown(JUMP_KEY) and (self.num_jumps > 0 or self.on_floor):
                # if JUMP_KEY pressed and the player is allowed to jump (has jumps available)
                self.direction.y = self.jump_speed
                # set y-direction to jump_speed
                # Check whether this is a jump or a double jump
                self.num_jumps -= 1
                pygame.mixer.Sound.play(jumpSound)
                self.on_floor = False

            self.direction.y += self.fall_speed
            # add gravity to y-direction
            
            if self.rect.bottom <= Tile.dimensions["bottom"] - BLOCK_SIZE * 2:
                self.v_lock_camera = False
            else:
                self.v_lock_camera = True
            
            if ((self.rect.top < self.v_free_movement_region[0] and self.direction.y < 0) or \
                (self.rect.bottom > self.v_free_movement_region[1] and self.direction.y > 0)) and \
                not self.v_lock_camera:
                    
                    for tile_layer, tile_list in tiles.items():
                        for t in tile_list:
                            t.position.y -= self.direction.y
                    # move the tiles instead of the player      
            
            else:
                self.rect.y += self.direction.y
                # move the player by the y-direction on the y axis

            for t in tiles["outline"]:
                # loop through tiles
                if self.rect.colliderect(t.rect):
                    # check for collision with tiles

                    if (self.direction.y > 0) and (self.rect.top <= t.rect.top):
                        # if the player is moving down and 
                        # the player's top is farther down than the top of the colliding block 
                        # (a collision was detected on the same level as the player)

                        self.rect.bottom = t.rect.top
                        # place the player at the collided block
                        self.direction.y = 0
                        # stop moving the player down (no need for gravity)
                        self.num_jumps = 1 + (1 * self.can_double_jump)
                        # reset jump (add double jump if allowed)    
                        self.on_floor = True 

                    elif (self.direction.y < 0) and (self.rect.top > t.rect.top):
                        self.rect.top = t.rect.bottom
                        self.direction.y = 0
            
            if self.direction.y > self.fall_speed: self.on_floor = False
            
            if self.on_floor and not self.prev_on_floor:
                self.num_jumps -= 1

        horizontal_movement()
        # move horizontally (and collisions)
        
        if not self.in_dash:
            vertical_movement()
        # move vertically (and collisions)

        return self.rect.colliderect(tiles["completed"][0])
        # check for collision between completion flag
        
    def state_machine(self):
        self.previous_image_state = self.image_state
        
        if not self.on_floor != 0:
            if self.direction.y < 0:
                self.image_state = "jump"
            else:
                self.image_state = "fall"
        elif self.direction.x != 0:
            self.image_state = "run"
        else:
            self.image_state = "idle"
    
    def animate(self):
        if self.image_state != self.previous_image_state:
            self.frame_number = 0
        
        if self.animation_timer.time_check():
            self.frame_number += 1
            
            if self.frame_number >= len(self.sprites[self.image_state]):
                self.frame_number = 0
        
            self.image = self.sprites[self.image_state][self.frame_number]
            
            if self.look_dir == "left":
                self.image = pygame.transform.flip(self.image, True, False)           
        
    def draw(self, display: pygame.Surface):
        self.state_machine()
        self.animate()
        
        display.blit(self.image, self.rect.topleft)
        # draw player onto display
