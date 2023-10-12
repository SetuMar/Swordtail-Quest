import pygame
class Enemy:#parent enemy class for all
    def __init__(self,image:pygame.surface,position):
        #define position, image and rect
        self.position = position
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    def draw(self, display):
        # if self.image is none, the enemy has been deleted
        # if you try to blit a deleted image the code crashes
        if self.image != None:
        # if image does not exist, then do not draw
            self.rect.topleft = self.position
            #change the bounds of the rect to the new enemy position
            display.blit(self.image,self.rect.topleft)
            # blit the image        
    def collide(self, player):
        if self.image is not None and self.rect.colliderect(player.rect):
            self.image = None
            #Currently, player kills enemy on contact. replace this later
class Walker(Enemy):
    def __init__(self,image:pygame.surface,position,left_boundary,right_boundary,move_speed:int = 2):
        #left and right boundaries should be integers representing the furthest left and furthest right x positions to walk to.
        super().__init__(image,position)
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.move_speed = move_speed
        self.direction = "right"
        #direction is just left or right as a string.
    def walk(self):
        #If the walker is walking right
        if self.direction == "right":
            #and moving right would not put the walker over its boundary
            if self.position.x < self.right_boundary - self.move_speed:
                #move the walker right by its move speed
                self.position.x += self.move_speed
            #if moving would make the walker cross its boundary, make it go left
            else: self.direction = "left"
        else:#if the walker is moving left. Same logic as for right just opposite
            if self.position.x > self.left_boundary + self.move_speed:
                self.position.x -= self.move_speed
            else:
                self.direction = "right"