from pytmx.util_pygame import load_pygame
import block
import pygame
from settings import *

def generate_level(location:str):
    tmx_data = load_pygame(location)
    
    tiles = []
    
    for layer in tmx_data.visible_layers:
        # go through all visible layers
        
        for tile_data in layer.tiles():
            tiles.append(block.Tile(tile_data[2], pygame.Vector2(tile_data[0] * BLOCK_SIZE, tile_data[1] * BLOCK_SIZE)))
            
    return tiles