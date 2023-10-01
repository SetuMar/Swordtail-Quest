from pytmx.util_pygame import load_pygame
import pygame
# import pygame and pytmx

import block
from settings import *
# import game files

def generate_level(location:str):
    tmx_data = load_pygame(location)
    # get the data for a specific level
    
    tiles = []
    # list of all tiles
    
    for layer in tmx_data.visible_layers:
        # go through all visible layers
        
        for tile_data in layer.tiles():
            tiles.append(block.Tile(tile_data[2], pygame.Vector2(tile_data[0] * BLOCK_SIZE, tile_data[1] * BLOCK_SIZE)))
        # add tile to list of tiles
            
    return tiles
    # return list of tiles