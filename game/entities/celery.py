#--------------------------IMPORTS--------------------------#


import pygame
from game.entities.enemy import Enemy


#--------------------------CLASS--------------------------#


class Celery(Enemy):
    texture = None

    def __init__(self, x: int, y: int, width: int=32, height: int=64):
        super().__init__(x, y, width=width, height=height)
        self.image = self.get_texture()

    def get_texture(cls):
        if cls.texture is None:
            cls.texture = pygame.image.load("assets/images/celery-idle-000.png").convert_alpha()
        return cls.texture

    def update(self, player, collidables):
        # Calculate direction vector toward player
        dx = player.rect.centerx - self.rect.centerx
        #dy = player.rect.centery - self.rect.centery
        distance = (dx ** 2) ** 0.5

        if distance != 0:
            dx /= distance
            #dy /= distance

        # Move enemy toward player
        self.rect.x += dx * self.speed
        #self.rect.y += dy * self.speed

        for obj in collidables:
            if self != obj and self.rect.colliderect(obj.rect):
                if dx > 0:
                    self.rect.right = obj.rect.left
                elif dx < 0:
                    self.rect.left = obj.rect.right
                break
