import math
import pygame
# import pygame

from settings import *

class Tile:
    dimensions = {
        "left":math.inf,
        "top":math.inf,
        "right":-math.inf,
        "bottom":-math.inf
    }
    
    level_length = 0
    
    def __init__(self, image:pygame.Surface, position:pygame.Vector2) -> None:
        self.image = image
        # set sprite to image
        
        self.rect = self.image.get_rect()
        # get rect from image
        self.rect.topleft = position
        # set position of rectangle
        
        self.position = position
        
    def draw(self, display:pygame.Surface):
        if self.image != None:
            self.rect.topleft = self.position
            display.blit(self.image, self.rect.topleft)
        # draw rectangle to display
        
    @staticmethod
    def block_shift(tiles, player):
        shift_amt = 0
        for layer_tiles in tiles.values():
        # go through all tile layers and the tiles on the layer
            for t in layer_tiles:
                difference = t.rect.bottom - SCREEN_HEIGHT
                if difference > shift_amt: shift_amt = difference
                
        for layer_tiles in tiles.values():
        # go through all tile layers and the tiles on the layer
            for t in layer_tiles:
                t.position.y -= shift_amt
                
        player.rect.y -= shift_amt
        
    @classmethod
    def determine_level_length(cls, tiles):
        length = -math.inf
        for layer_tiles in tiles.values():
        # go through all tile layers and the tiles on the layer
            for t in layer_tiles:
                if t.rect.right > length:
                    length = t.rect.right
                
        cls.level_length = length
        
    @classmethod
    def determine_bounds(cls, tile):
        if tile.position.x < cls.dimensions["left"]: cls.dimensions["left"] = tile.position.x
        if tile.position.x + BLOCK_SIZE > cls.dimensions["right"]: cls.dimensions["right"] = tile.position.x + BLOCK_SIZE
        if tile.position.y < cls.dimensions["top"]: cls.dimensions["top"] = tile.position.y
        if tile.position.y + BLOCK_SIZE > cls.dimensions["bottom"]: cls.dimensions["bottom"] = tile.position.y + BLOCK_SIZE