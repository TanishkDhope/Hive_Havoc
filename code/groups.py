import pygame
from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset=pygame.Vector2(0,0)

    def draw(self,display_surface, player_pos):
        self.offset.x=-(player_pos[0] - WINDOW_WIDTH/2)
        self.offset.y=-(player_pos[1] - WINDOW_HEIGHT/2)

        ground_sprite=[sprite for sprite in self if hasattr(sprite, "ground")]
        object_sprite=[sprite for sprite in self if not hasattr(sprite, "ground")]
        



        for layer in [ground_sprite, object_sprite]:
            for sprite in layer:
                display_surface.blit(sprite.image,sprite.rect.topleft+self.offset)
            

        