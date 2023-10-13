import pygame
    
class Powerup:
    powerup_layer_names = ["double_jump", "dash"]
    
    def __init__(self, image:pygame.Surface, position:pygame.Vector2, type:str) -> None:
        self.image = image
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
        if self.image is not None and self.rect.colliderect(player.rect):
            if self.type == "double_jump":
                player.num_jumps = 2
                player.can_double_jump = True
                
            if self.type == "dash":
                 player.can_dash = True

            self.image = None
            # get rid of powerup visual - not needed