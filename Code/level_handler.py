from pytmx.util_pygame import load_pygame
import pathlib as pl
import pygame
# import pygame and pytmx

import block
import enemy
from settings import *
# import game files

import powerups
from sounds import winSound

# create the relative path of the Graphics folder
current_file = pl.Path(__file__)
parent_directory = current_file.parent.parent
graphics_path = pl.Path(parent_directory / 'Graphics')

class GameOverHandler:
    def __init__(self) -> None:
        self.current_level_completed = False
        self.level_number = 1

        self.current_level = str(graphics_path / 'Levels' / 'l1.tmx')

    def complete_level(self, tiles, player):
        self.level_number += 1
        self.current_level = str(graphics_path / 'Levels' / f'l{self.level_number}.tmx')
        tiles, player.rect.topleft = self.generate_level()
        player.health = 1
        block.Tile.determine_level_length(tiles)
        block.Tile.block_shift(tiles, player)
        pygame.mixer.Sound.play(winSound)

        self.current_level_completed = False

        return tiles

    def restart_level(self, tiles, player):
        self.current_level = str(graphics_path / 'Levels' / f'l{self.level_number}.tmx')
        tiles, player.rect.topleft = self.generate_level()
        
        block.Tile.determine_level_length(tiles)
        block.Tile.block_shift(tiles, player)

        player.health = 1
        player.direction = pygame.Vector2(0, 0)

        self.current_level_completed = False

        return tiles

    def generate_level(self):
        tmx_data = load_pygame(self.current_level)
        # get the data for a specific level

        tiles = {}
        # list of all tiles

        # # audio 
        # self.bg_music = pygame.mixer.Sound('music/Forest_Theme.mp3')
        # self.bg_music.play(loops = -1)

        player_position = None

        for layer in tmx_data.visible_layers:
            # go through all visible layers

            layer_tiles = []

            for tile_data in layer.tiles():
                image = tile_data[2]
                position = pygame.Vector2(tile_data[0] * BLOCK_SIZE, tile_data[1] * BLOCK_SIZE)
                if layer.name in powerups.Powerup.powerup_layer_names:
                    layer_tiles.append(powerups.Powerup(image, position, layer.name))
                
                elif layer.name == "player":
                    player_position = position
                
                elif layer.name == "walker_enemy":
                    layer_tiles.append(enemy.Walker(image, position))
                    
                elif layer.name == "deco_big":
                    b = block.Tile(image, position)
                    b.position.y -= (b.image.get_height() / 2) + (b.image.get_height() / 4)
                    b.rect.y -= (b.image.get_height() / 2) + (b.image.get_height() / 4)
                    layer_tiles.append(b)
                
                else:
                    layer_tiles.append(block.Tile(image, position))
            # add tile to list of tiles

            tiles.update({layer.name: layer_tiles})

        return tiles, player_position
        # return list of tiles and player position
