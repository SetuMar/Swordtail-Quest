import pygame
    
class Powerup:
    def __init__(self, image:str, position:pygame.Vector2, type:str) -> None:
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.type = type
    
    def draw(self, display):
        # if self.image is none, the powerup has been deleted
        # if you try to blit a deleted image the code crashes
        if self.image != None:
        # if image does not exist, then do not draw
            display.blit(self.image,self.rect.topleft)
            # blit the image
            
    def collide(self, player):
        if self.rect is not None and self.rect.colliderect(player.rect):
            # If the player is colliding with the powerup
                # Delete the sprite
                #check powerup types and assign appropriate flags
                if self.type == "double_jump": player.has_double_jump = True
                if self.type == "dash":
                     player.has_dash = True
                     player.can_dash = True
                self.image = None
                # and the hitbox
                self.rect = None

