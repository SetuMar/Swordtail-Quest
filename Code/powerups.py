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
                if self.type == "double_jump": player.has_double_jump = True
                
                self.image = None
                # and the hitbox
                self.rect = None
        
# class Dash():
#     def __init__(self) -> None:
#         #Load the Dash image
#         self.image = pygame.image.load("Graphics/dashplaceholder.png")   
#         #Make a rect based off the image
        
#         self.rect = self.image.get_rect()
#         # Place the x and y at 400 and 600
#         # These are values for testing and will probably be changed when implemented into levels
        
#         self.rect.x = 400
#         self.rect.y = 600
    
#     def draw(self,display):
#         #If self.image is none, the powerup has been deleted. If you try to blit a deleted image the code crashes.
#         if self.image != None:
#             #Blit the image
#             display.blit(self.image,self.rect.topleft)
#     #Collision detection with the player and powerup
    
#     def collide(self,Player):
#         #Only collide if the collision hasn't already occured(the powerup is deleted on collision)
#         if self.rect != None:
#             #If the player is colliding with the powerup
#             if self.rect.colliderect(Player.rect):
#                 #The player now has the ability to dash
#                 Player.has_dash = True
#                 #The player now can dash immediately
#                 Player.can_dash = True
#                 #delete the sprite
#                 self.image = None
#                 #and the hitbox
#                 self.rect = None
""" class Temp(Powerup):
    #just for testing
    def __init__(self) -> None:
        self.image = pygame.Surface((20,20))   
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 650
    def draw(self,display):
        display.blit(self.image,self.rect.topleft) """
