#--------------------------IMPORTS--------------------------#


import math, time
import pygame
import pymunk
import config
from game.loader import load_level

# Game entities imports
from game.entities.player import Player
from game.entities.celery import Celery
from game.entities.invisiblebarrier import InvisibleBarrier
from game.entities.movingsolidtile import MovingSolidTile


#--------------------------GAME CLASS--------------------------#


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Load background image
        bg_path = "assets/images/sunnyskybackgroud.png" # <-- haha look, we misspelled it
        self.background = pygame.image.load(bg_path).convert()

        # Initialize pymunk components
        self.pymunk_space = pymunk.Space()
        self.pymunk_space.gravity = (0, 15)
        self.platform_shapes = []
        self.moving_platforms = []

        # Initialize pygame components
        self.player = Player(0,0)
        self.camera_x = 0
        self.camera_y = 215
        self.level = None
        self.entities = []
        self.celery = []

    def run(self):
        # Main game loop
        while self.is_running:
            self.process_events()
            self.update_state()
            self.render_frame()
            self.clock.tick(60)  # Limit to 60 FPS

    def process_events(self):
        vx = 0

        # Handle all input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_F3]:
            config.SHOW_OBJECT_COORDS = not config.SHOW_OBJECT_COORDS

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx -= 100
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = 100
        #if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #    dy += 1
        #if keys[pygame.K_UP] or keys[pygame.K_w]:
        #    dy -= 1
        #self.player.move(dx, dy, self.entities)

        self.player.body.velocity = (vx, self.player.body.velocity.y)


    def update_state(self):
        self.pymunk_space.step(60/1000)

        # Sync pygame and pymunk - aka gravity
        self.player.rect.centerx = int(self.player.body.position.x)
        #self.player.rect.centery = int(self.player.body.position.y)

        # Update Player
        self.player.update()

        # Update Enemies
        for enemy in self.celery:
            enemy.update(self.player, self.entities)
        pass

    def render_frame(self):
        # Draw background
        self.screen.blit(self.background, (-self.camera_x, -self.camera_y))

        # Draw all "entities"
        for entity in self.entities:
            # Skip loading player twice
            if isinstance(entity, Player):
                continue
            # Don't draw invis barriers
            if isinstance(entity, InvisibleBarrier):
                continue
            # Let pymunk have its turn first
            if isinstance(entity, MovingSolidTile):
                continue
            entity.draw(self.screen, self.camera_x, self.camera_y)

        # Draw moving platforms
        for platform in self.moving_platforms:
            offset = platform["amplitude"] * math.sin(time.time() * platform["speed"] * 0.01)
            y = platform["origin_y"] + offset
            platform["body"].position = (platform["body"].position.x, y)

            # Sync sprite to body
            platform["obj"].rect.x = int(platform["body"].position.x)
            platform["obj"].rect.y = int(platform["body"].position.y)

            platform["obj"].draw(self.screen, self.camera_x, self.camera_y)


        # Update camera pos
        self.camera_x = max(0, min(self.player.rect.centerx - config.SCREEN_WIDTH // 2, config.LEVEL_WIDTH - config.SCREEN_WIDTH))
        self.camera_y = max(0, min(self.player.rect.centery - config.SCREEN_HEIGHT // 2, config.LEVEL_HEIGHT - config.SCREEN_HEIGHT))

        # Draw the player/camera
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Update the display
        pygame.display.flip()

    def load_scene(self, level: str):
        self.level = level

        # Clear physics platform shapes from previous level
        for shape in self.platform_shapes:
            self.pymunk_space.remove(shape)
        self.platform_shapes.clear()

        # Load objects from level
        instantiated_objects = load_level(level)

        for obj in instantiated_objects:
            # Place player in level
            if isinstance(obj, Player):
                self.player = Player(obj.x, obj.y)
                self.create_player_physics()
                continue # Skip appending

            # List of enemies
            if isinstance(obj, Celery):
                self.celery.append(obj)

            # Kinematic platforms - pymunk
            if isinstance(obj, MovingSolidTile):
                # Create a kinematic body
                body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                body.position = (obj.x + obj.width / 2, obj.y + obj.height / 2)
                shape = pymunk.Poly.create_box(body, (obj.width, obj.height))
                self.pymunk_space.add(body, shape)

                # Store references for updating position later
                self.moving_platforms.append({"body": body, "shape": shape, "obj": obj, "origin_y": body.position.y, "amplitude": 40, "speed": 50})

            # ─── ADD: If obj is a static platform, add a static shape to physics space ───
            # (You'll need to decide which obj types count as static platforms)
            # For example:
            # if isinstance(obj, Platform):
            #     shape = pymunk.Poly.create_box(self.space.static_body, (obj.width, obj.height))
            #     shape.body.position = (obj.x + obj.width / 2, obj.y + obj.height / 2)
            #     self.space.add(shape)
            #     self.platform_shapes.append(shape)

            # Add each entity to Game's entity list
            self.entities.append(obj)

    def create_player_physics(self):
        mass = 1
        width, height = self.player.rect.width, self.player.rect.height
        moment = pymunk.moment_for_box(mass, (width, height))
        body = pymunk.Body(mass, moment)
        body.position = self.player.rect.centerx, self.player.rect.centery

        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 1.0
        shape.elasticity = 0.0

        self.pymunk_space.add(body, shape)

        # Store references for syncing later
        self.player.body = body
        self.player.shape = shape

    #print(instantiated_objects) # Debug line
