import pygame
import powerups
from settings import *
import pathlib as pl
from os import walk

# create the relative path of the Graphics folder
current_file = pl.Path(__file__)
parent_directory = current_file.parent.parent
graphics_path = pl.Path(parent_directory / 'Graphics')


class PowerupHolder:
    def __init__(self, position: pygame.Vector2) -> None:
        sprites_location = str(graphics_path / "Powerup Sprites")

        self.powerup_sprites = {}

        for (root, dirs, files) in walk(sprites_location):
            for file in files:
                self.powerup_sprites.update({file.split(".")[0]: pygame.image.load(sprites_location + "/" + file)})

        self.powerup_gap_space = 10
        self.image_dimensions = (
            len(powerups.Powerup.powerup_layer_names) * BLOCK_SIZE + (2 * self.powerup_gap_space) + (
                    (len(powerups.Powerup.powerup_layer_names) - 1) * self.powerup_gap_space),
            BLOCK_SIZE + (2 * self.powerup_gap_space))
        self.image = pygame.Surface(self.image_dimensions)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.held_powerups = []
        self.prev_held_powerups_length = 0

    def draw(self, display: pygame.Surface) -> None:
        if len(self.held_powerups) != self.prev_held_powerups_length:
            self.image = pygame.Surface(self.image_dimensions)

            x_pos = self.powerup_gap_space
            y_pos = self.powerup_gap_space

            for p in self.held_powerups:
                self.image.blit(self.powerup_sprites[p], (x_pos, y_pos))
                x_pos += self.powerup_gap_space + BLOCK_SIZE

        display.blit(self.image, self.rect.topleft)

        self.prev_held_powerups_length = len(self.held_powerups)
