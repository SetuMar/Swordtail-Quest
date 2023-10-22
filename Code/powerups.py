import pygame
import particles

class Powerup:
    powerup_layer_names = ["double_jump", "dash"]
    # names for each layer of powerups
    
    def __init__(self, image:pygame.Surface, position:pygame.Vector2, type:str) -> None:
        self.image = image
        # powerup image
        self.rect = self.image.get_rect()
        # create rectangle from sprite
        self.rect.topleft = position
        # set position of powerup rect
        self.type = type
        # set type of powerup
        self.position = position
        
        self.particles = None
        self.generate_particles = False
    
    def draw(self, display):
        self.rect.topleft = self.position

        # if self.image is none, the powerup has been deleted
        # if you try to blit a deleted image the code crashes
        if self.image != None:
        # if image does not exist, then do not draw
            display.blit(self.image,self.rect.topleft)
            # blit the image
        else:
            if self.particles == None:
                if self.type == "double_jump": color = (46, 112, 219)
                if self.type == "dash": color = (230, 41, 60)
                
                self.particles = particles.Particle.generate_system(color, self.rect.center, 5, 5, 0.9, 10)
    
    def draw_particles(self, display):
        particles.Particle.simulate_system(self.particles, display)
            
    def collide(self, player, powerup_holder):
        if self.rect.colliderect(player.rect):
        # check for powerups collision
            if self.type == "double_jump":
                player.num_jumps = 2
                player.can_double_jump = True
            # if double jump, then player can double jump
                
            if self.type == "dash":
                 player.can_dash = True
            # if dash, then player can dash

            player.health += 1
            # increase the health of the player
            powerup_holder.held_powerups.append(self.type)
            # update the display of the held powerups
            self.image = None
            # get rid of powerup visual - not needed