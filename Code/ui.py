import pygame
import powerups
from settings import *
import pathlib as pl
from os import walk
import keys

# create the relative path of the Graphics folder
current_file = pl.Path(__file__)
parent_directory = current_file.parent.parent
graphics_path = pl.Path(parent_directory / 'Graphics')

class PowerupHolder:
    def __init__(self) -> None:
        sprites_location = str(graphics_path / "Powerup Sprites")
        # location of the powerup sprites folder

        self.powerup_sprites = {}
        # powerup sprites held in a dictionary

        for (root, dirs, files) in walk(sprites_location):
            for file in files:
                self.powerup_sprites.update({file.split(".")[0]:pygame.image.load(sprites_location + "/" + file)})
                # get each sprite and add it to the dictionary

        self.powerup_gap_space = 10
        # gap between each powerup

        self.image_dimensions = (len(powerups.Powerup.powerup_layer_names) * BLOCK_SIZE + (2 * self.powerup_gap_space) + 
                                 ((len(powerups.Powerup.powerup_layer_names) - 1) * self.powerup_gap_space), 
                                 BLOCK_SIZE)
        # dimensions of each image
        self.image = pygame.Surface(self.image_dimensions, pygame.SRCALPHA)
        # create image surface

        self.rect = self.image.get_rect()
        # get rectangle from image
        self.rect.topleft = pygame.Vector2(0, SCREEN_HEIGHT - self.image_dimensions[1])
        # move the rectangle to the designated position

        self.held_powerups = []
        # powerups in current use
        self.prev_held_powerups_length = 0
        # length of the powerups list last frame (for updates)
        
        self.image_opacity = 100
        self.image.fill((0, 0, 0, self.image_opacity))

    def draw(self, display:pygame.Surface):
        if len(self.held_powerups) != self.prev_held_powerups_length:
        # if the number of powerups is different than what was calculated last frame
            self.image = pygame.Surface(self.image_dimensions)
            # redraw the image
            
            self.image.set_alpha(self.image_opacity, pygame.SRCALPHA)

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
        
class BetweenLevelHolderMenu:
    def __init__(self) -> None:
        self.image = pygame.Surface(SCREEN_SIZE)
        self.rect = self.image.get_rect()
        
        self.opacity = 0
        self.opacity_increase_amt = 40
        
        self.font = pygame.font.Font(r"Graphics/PixelifySans-VariableFont_wght.ttf", 50)
        self.font_color = (255, 255, 255)
        
        self.continue_event_key = pygame.K_SPACE
        self.opacity_transition_completed = False
        
        self.keys = keys.KeyData()
        
        self.key_pressed = False
        
    def draw(self, text, display):
        self.text = self.font.render(text, False, self.font_color)
        
        self.image.blit(self.text, pygame.Vector2(SCREEN_WIDTH / 2 - self.text.get_width() / 2, SCREEN_HEIGHT / 2 - self.text.get_height() / 2))
        self.opacity = self.opacity + self.opacity_increase_amt if self.opacity < 255 else 255
        
        self.image.set_alpha(self.opacity)
        
        display.blit(self.image, (0, 0))
        
        if self.key_pressed == False: 
            self.key_pressed = self.keys.get_key_on_keydown(self.continue_event_key)
        else:
            self.opacity_transition_completed = True
        
        return self.opacity_transition_completed