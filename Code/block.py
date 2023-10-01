import pygame
# import pygame
class Tile:
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