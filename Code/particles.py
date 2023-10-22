import math
import random
import pygame

class Particle:
    def __init__(self, color:[int, int, int], center_position:pygame.Vector2, rotate_amt:float, fade_out_amt:float, scale_keep_amt:float, fall_strength:int = 0) -> None:
        self.sprite = pygame.Surface((10, 10))
        self.sprite.fill(color)
        self.image = self.sprite
        self.save_pos = center_position
        
        self.rect = self.image.get_rect()
        self.rect.center = center_position
        
        self.angle = 0
        self.opacity = 255
        self.save_scale = pygame.Vector2(self.image.get_size())
        self.scale = self.save_scale
        
        self.rotate_amt = rotate_amt
        self.fade_out_amt = fade_out_amt
        self.scale_keep_amt = scale_keep_amt

        self.fall_strength = fall_strength
        move_angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.Vector2(math.cos(move_angle), -math.sin(move_angle)) * self.fall_strength
        self.gravity = 0.8
        
    def update(self) -> None:
        self.angle += self.rotate_amt
        save_pos = self.rect.center
        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = save_pos
        
        if self.opacity > 0:
            if self.opacity < 0: 
                self.opacity = 0
            else:
                self.opacity -= self.fade_out_amt
        
        if self.scale != pygame.Vector2(0, 0):
            self.scale  = self.scale * self.scale_keep_amt
        
        self.image.set_alpha(self.opacity)
        
        self.rect.topleft += self.direction
        self.direction.y += self.gravity

    def reset(self):
        self.angle = 0
        self.opacity = 255
        self.scale = self.save_scale
        self.rect.center = self.save_pos
        
        if self.is_falling:
            move_angle = random.uniform(0, 2 * math.pi)
            self.direction = pygame.Vector2(math.cos(move_angle), -math.sin(move_angle)) * self.fall_strength
        
    def draw(self, display:pygame.Surface):
        display.blit(self.image, self.rect.topleft)
    
    @staticmethod
    def generate_system(color:[255, 255, 255], center_pos:pygame.Vector2, rotate_amt:float, fade_out_amt:float, scale_amt:float, fall_strength:float):
        num_particles = 30
        
        particles = []
        
        for p in range(num_particles):
            particles.append(
                Particle(color, center_pos, rotate_amt, fade_out_amt, scale_amt, fall_strength)
            )
            
        return particles

    @staticmethod
    def simulate_system(particle_system:list, display:pygame.Surface):
        for p in particle_system:
            p.update()
            p.draw(display)
            
    @staticmethod
    def reset_system(particles:list):
        for p in particles:
            p.reset()