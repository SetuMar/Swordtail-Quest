import pygame
class Powerup:
    #Base powerup class
    #It's empty for now but maybe we'll use it later
    #Who knows
    def __init__(self) -> None:
        pass
class Double_jump(Powerup):
    def __init__(self) -> None:
        #Load the doublejump image
        self.image = pygame.image.load("Graphics\doublejumpplaceholder.png")   
        #Make a rect based off the image
        self.rect = self.image.get_rect()
        #Place the x and y at 250 and 650. These are values for testing and will probably be changed when implemented into levels
        self.rect.x = 250
        self.rect.y = 650
    def draw(self,display):
        #If self.image is none, the powerup has been deleted. If you try to blit a deleted image the code crashes.
        if self.image != None:
            #Blit the image
            display.blit(self.image,self.rect.topleft)
    #Collision detection with the player and powerup
    def collide(self,Player):
        #Only collide if the collision hasn't already occured(the powerup is deleted on collision)
        if self.rect != None:
            #If the player is colliding with the powerup
            if self.rect.colliderect(Player.rect):
                #The player now has the ability to double jump
                Player.has_double_jump = True
                #delete the sprite
                self.image = None
                #and the hitbox
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
