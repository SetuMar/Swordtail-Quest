import pygame
pygame.init()
#Init pygame sound mixer
pygame.mixer.init()
#Sfx
jumpSound = pygame.mixer.Sound("sfx/jump.wav")
loseLifeSound = pygame.mixer.Sound("sfx/loseLife.wav")
hurtSound = pygame.mixer.Sound("sfx/hurt.wav")
hitSound = pygame.mixer.Sound("sfx/hit.wav")
powerUpSound = pygame.mixer.Sound("sfx/powerUp.wav")
dashSound = pygame.mixer.Sound("sfx/dash.wav")