import math
import pygame
# import pygame
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
        
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
        # draw rectangle to display
        
    @classmethod
    def determine_level_length(cls, tiles):
        length = -math.inf
        for layer, layer_tiles in tiles.items():
        # go through all tile layers and the tiles on the layer
            for t in layer_tiles:
                if t.rect.right > length:
                    length = t.rect.right
                
        cls.level_length = length
        
    @classmethod
    def determine_bounds(cls, tile):
        if tile.rect.left < cls.dimensions["left"]: cls.dimensions["left"] = tile.rect.left
        if tile.rect.right > cls.dimensions["right"]: cls.dimensions["right"] = tile.rect.right