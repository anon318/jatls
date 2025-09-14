#--------------------------IMPORTS--------------------------#

import pygame
import config
from game.entities.player import Player
from game.entities.celery import Celery
from game.entities.invisiblebarrier import InvisibleBarrier
from game.loader import load_level

# ─── ADD THESE IMPORTS ──────────────────────────────────────────────────────────
import arcade                                # ADD: Arcade core
from arcade import Sprite, SpriteList        # ADD: Sprite types
from arcade.physics_engines import PhysicsEnginePlatformer  # ADD: physics engine


#--------------------------GAME CLASS--------------------------#

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen      = screen
        self.asset_folder= "assets/images/"
        self.clock       = pygame.time.Clock()
        self.is_running  = True
        self.camera_x    = 0
        self.camera_y    = 215

        # Load background image
        bg_path = self.asset_folder + "sunnyskybackgroud.png"
        self.background = pygame.image.load(bg_path).convert()

        # ─── ADD: Create an invisible Arcade window for physics internals ───────────
        # This must be before you instantiate any Arcade sprites/engines.
        arcade.Window(
            config.SCREEN_WIDTH,
            config.SCREEN_HEIGHT,
            title="(invisible) Arcade physics window",
            visible=False
        )

        # ─── ADD: Prepare Arcade‐side sprite containers ────────────────────────────
        self.arcade_player: Sprite      = None      # Will hold your player as an Arcade.Sprite
        self.barriers: SpriteList       = SpriteList()  # Walls + invisible barriers
        self.physics_engine: PhysicsEnginePlatformer = None

        # Pygame‐side wrappers
        self.player   = Player(0, 0)
        self.level    = None
        self.entities = []
        self.celery   = []

    def run(self):
        # Main game loop
        while self.is_running:
            self.process_events()
            self.update_state()
            self.render_frame()
            self.clock.tick(60)  # Limit to 60 FPS

    def process_events(self):
        dx = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        keys = pygame.key.get_pressed()

        # ─── REPLACE: your dx/dy → Arcade change_x / change_y calls ────────────────
        # Instead of self.player.move(dx, dy, ...), do:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.arcade_player.change_x = -self.player.speed   # Arcade expects change_x
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.arcade_player.change_x = +self.player.speed
        else:
            self.arcade_player.change_x = 0

        # Jump (UP arrow)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.arcade_player.change_y = config.JUMP_SPEED     # physics engine jump

    def update_state(self):
        # ─── ADD: Step Arcade physics each frame ───────────────────────────────────
        if self.physics_engine:
            self.physics_engine.update()  # PhysicsEnginePlatformer.update()

        # ─── ADD: Sync Arcade sprite position back into your Pygame rect ──────────
        # Arcade uses bottom-left origin, Pygame uses top-left.
        if self.arcade_player and self.player:
            # Compute top-left for Pygame
            px = self.arcade_player.center_x - (self.player.rect.width  / 2)
            py = (config.SCREEN_HEIGHT - self.arcade_player.center_y) - (self.player.rect.height / 2)
            self.player.rect.topleft = (px, py)

        # Keep your existing logic:
        # Update Pygame‐side Player and enemies
        self.player.update()
        for enemy in self.celery:
            enemy.update(self.player, self.entities)

    def render_frame(self):
        # Draw background
        self.screen.blit(self.background, (-self.camera_x, -self.camera_y))

        # Draw all entities (skip player & barriers as before)
        for entity in self.entities:
            if isinstance(entity, Player): continue
            if isinstance(entity, InvisibleBarrier): continue
            entity.draw(self.screen, self.camera_x, self.camera_y)

        # Update camera pos (unchanged)
        self.camera_x = max(
            0,
            min(self.player.rect.centerx - config.SCREEN_WIDTH // 2,
                config.LEVEL_WIDTH - config.SCREEN_WIDTH)
        )
        self.camera_y = max(
            0,
            min(self.player.rect.centery - config.SCREEN_HEIGHT // 2,
                config.LEVEL_HEIGHT - config.SCREEN_HEIGHT)
        )

        # Draw Pygame player
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Flip display
        pygame.display.flip()

    def load_scene(self, level: str):
        self.level = level
        instantiated_objects = load_level(level)

        # ─── ADD: Clear old Arcade sprites & barriers ──────────────────────────────
        self.entities.clear()
        self.celery.clear()
        self.barriers.clear()
        self.arcade_player = None

        for obj in instantiated_objects:
            # Place Pygame Player
            if isinstance(obj, Player):
                self.player = Player(obj.x, obj.y)

                # ─── ADD: Wrap in an Arcade.Sprite for physics ────────────────────
                # Use the same image as your Pygame player, and convert to bottom-left origin.
                self.arcade_player = arcade.Sprite(
                    filename=obj.image,
                    center_x=obj.x + obj.rect.width  / 2,
                    center_y=(config.SCREEN_HEIGHT - obj.y) - obj.rect.height / 2
                )
                continue

            # Enemies as barriers for now
            if isinstance(obj, Celery):
                self.celery.append(obj)
                barrier = arcade.SpriteSolidColor(
                    obj.rect.width, obj.rect.height, color=(0,0,0,0)
                )
                barrier.center_x = obj.rect.x + obj.rect.width  / 2
                barrier.center_y = (config.SCREEN_HEIGHT - obj.rect.y) - obj.rect.height / 2
                self.barriers.append(barrier)

            # Invisible barriers
            if isinstance(obj, InvisibleBarrier):
                barrier = arcade.SpriteSolidColor(
                    obj.rect.width, obj.rect.height, color=(0,0,0,0)
                )
                barrier.center_x = obj.rect.x + obj.rect.width  / 2
                barrier.center_y = (config.SCREEN_HEIGHT - obj.rect.y) - obj.rect.height / 2
                self.barriers.append(barrier)

            # All other entities stay in Pygame list
            self.entities.append(obj)

        # ─── ADD: Finally, instantiate the physics engine ──────────────────────────
        self.physics_engine = PhysicsEnginePlatformer(
            player_sprite    = self.arcade_player,
            gravity_constant = config.GRAVITY,
            walls            = self.barriers
        )
