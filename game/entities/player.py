#--------------------------IMPORTS--------------------------#


import pygame
import os


#--------------------------PLAYER CLASS--------------------------#


class Player:
    def __init__(self, x: int, y: int, width: int = 32, height: int = 64, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 4
        self.asset_folder = "assets/images/"
        self.on_ground = False

        # Load Jaden's sprite
        sprite_path = os.path.join(self.asset_folder, "jaden-idle-000.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy, collidables):
        print(self.on_ground)

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        on_ground_this_frame = False
        for obj in collidables:
            #print(obj)
            if self != obj and self.rect.colliderect(obj.rect):
                if dx > 0:
                    self.rect.right = obj.rect.left
                elif dx < 0:
                    self.rect.left = obj.rect.right
                elif dy > 0:
                    on_ground_this_frame = True
                    self.rect.bottom = obj.rect.top
                elif dy < 0:  # Head bump
                    self.rect.top = obj.rect.bottom
                self.on_ground = on_ground_this_frame
            #elif self != obj and not self.rect.colliderect(obj.rect):
                #self.on_ground = True
                #on_ground_this_frame = True
                break


        #for obj in collidables:
        #    if self != obj and self.rect.colliderect(obj.rect):
                # Check for ground contact with some vertical tolerance

        #        self.on_ground = on_ground_this_frame
        #        break


    def update(self):
        # Could include other logic later (e.g. animation, physics)
        pass

    def draw(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        draw_pos = (self.rect.x - camera_x, self.rect.y - camera_y)
        surface.blit(self.image, draw_pos)
