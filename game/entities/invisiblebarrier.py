#--------------------------IMPORTS--------------------------#


import pygame
from game.entities.object import GameObject


#--------------------------CLASS--------------------------#


class InvisibleBarrier(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width=width, height=height)

    def draw(self, surface):
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, 1) # Debug line
        pass
