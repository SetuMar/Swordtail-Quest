import pygame

class Tile:
    def __init__(self, image:pygame.Surface, position:pygame.Vector2) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)