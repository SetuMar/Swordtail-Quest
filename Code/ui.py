import pygame
import powerups
from settings import *
from os import walk

class PowerupHolder:
    def __init__(self, position:pygame.Vector2) -> None:
        sprites_location = r"Graphics/Powerup Sprites"
        # location of the powerup sprites folder
        
        self.powerup_sprites = {}
        # powerup sprites held in a dictionary
        
        for (root,dirs,files) in walk(sprites_location):
            for file in files:
                self.powerup_sprites.update({file.split(".")[0]:pygame.image.load(sprites_location + "/" + file)})
                # get each sprite and add it to the dictionary
        
        self.powerup_gap_space = 10
        # gap between each powerup
        
        self.image_dimensions = (len(powerups.Powerup.powerup_layer_names) * BLOCK_SIZE + (2 * self.powerup_gap_space) + ((len(powerups.Powerup.powerup_layer_names) - 1) * self.powerup_gap_space), BLOCK_SIZE + (2 * self.powerup_gap_space))
        # dimensions of each image
        self.image = pygame.Surface(self.image_dimensions)
        # create image surface
        
        self.rect = self.image.get_rect()
        # get rectangle from image
        self.rect.topleft = position
        # move the rectangle to the designated position
        
        self.held_powerups = []
        # powerups in current use
        self.prev_held_powerups_length = 0
        # length of the powerups list last frame (for updates)
        
    def draw(self, display:pygame.Surface):
        if len(self.held_powerups) != self.prev_held_powerups_length:
        # if the number of powerups is different than what was calculated last frame
            self.image = pygame.Surface(self.image_dimensions)
            # redraw the image
            
            x_pos = self.powerup_gap_space
            y_pos = self.powerup_gap_space
            # x and y positions for each powerup
            
            for p in self.held_powerups:
                self.image.blit(self.powerup_sprites[p], (x_pos, y_pos))
                x_pos += self.powerup_gap_space + BLOCK_SIZE
            # place powerup at specified position
        
        display.blit(self.image, self.rect.topleft)
        # draw powerup sprite
        
        self.prev_held_powerups_length = len(self.held_powerups)
        # set previous held powerups length equal to length of current held powerups