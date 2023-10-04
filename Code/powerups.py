import pygame
class Powerup:
    def __init__(self) -> None:
        pass
class Double_jump(Powerup):
    def __init__(self) -> None:
        self.image = pygame.image.load("Graphics\doublejumpplaceholder.png")   
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 650
    def draw(self,display):
        if self.image != None:
            display.blit(self.image,self.rect.topleft)
    def collide(self,Player):
        if self.rect != None:
            if self.rect.colliderect(Player.rect):
                Player.has_double_jump = True
                Player.can_double_jump = True
                self.image = None
                self.rect = None

""" class Temp(Powerup):
    #just for testing
    def __init__(self) -> None:
        self.image = pygame.Surface((20,20))   
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 650
    def draw(self,display):
        display.blit(self.image,self.rect.topleft) """
