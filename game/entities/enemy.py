#--------------------------IMPORTS--------------------------#


import pygame
from game.entities.object import GameObject


#--------------------------CLASS--------------------------#


class Enemy(GameObject):
    def __init__(self, x: int, y: int, width, height):
        super().__init__(x, y, width=width, height=height)
        self.speed = 1.5

    def update(self, player):
        """Override in subclasses."""
        pass
