#--------------------------IMPORTS--------------------------#


import pygame
import config


#--------------------------CLASS--------------------------#


# Debug font :p
pygame.font.init()
DEBUG_FONT = pygame.font.SysFont('Arial', 14)

class GameObject:
    def __init__(self, x: int, y: int, width: int = 32, height: int = 32):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None

    def update(self):
        """Override in subclasses for movement, behavior, etc."""
        pass

    def draw(self, surface: pygame.Surface, camera_offset_x, camera_offset_y):
        draw_x = self.rect.x - camera_offset_x
        draw_y = self.rect.y - camera_offset_y
        #surface.blit(self.image, (draw_x, draw_y))

        # Get image size
        tile_width, tile_height = self.image.get_size()

        # Loop over the object's rect and tile the image
        for x in range(0, self.rect.width, tile_width):
            for y in range(0, self.rect.height, tile_height):
                surface.blit(
                    self.image,
                    (draw_x + x, draw_y + y)
                )


        # Draw debug text (X, Y)
        if config.SHOW_OBJECT_COORDS:
            coord_text = f"{self.rect.x},{self.rect.y}"
            text_surface = DEBUG_FONT.render(coord_text, True, (255, 255, 255))  # white text
            surface.blit(text_surface, (draw_x + 2, draw_y + 2))  # small offset to avoid corner
