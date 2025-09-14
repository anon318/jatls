#--------------------------IMPORTS--------------------------#


import pygame
from game.entities.object import GameObject


#--------------------------CLASS--------------------------#


class MovingSolidTile(GameObject):
    texture = None

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width=width, height=height)
        self.image = self.get_texture()

    def get_texture(cls):
        if cls.texture is None:
            cls.texture = pygame.image.load("assets/images/movingsolidtile.png").convert_alpha()
        return cls.texture

