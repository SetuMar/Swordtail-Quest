import pygame
import pathlib as pl

current_file = pl.Path(__file__)
parent_directory = current_file.parent.parent
sfx_path = pl.Path(parent_directory / 'sfx')

pygame.init()
# Init pygame sound mixer
pygame.mixer.init()
# Sfx
jumpSound = pygame.mixer.Sound(sfx_path / "jump.wav")
loseLifeSound = pygame.mixer.Sound(sfx_path / "loseLife.wav")
hurtSound = pygame.mixer.Sound(sfx_path / "hurt.wav")
hitSound = pygame.mixer.Sound(sfx_path / "hit.wav")
powerUpSound = pygame.mixer.Sound(sfx_path / "powerUp.wav")
dashSound = pygame.mixer.Sound(sfx_path / "dash.wav")
winSound = pygame.mixer.Sound(sfx_path / "win.wav")
