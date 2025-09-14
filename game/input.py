#--------------------------IMPORTS--------------------------#


import pygame
import config
from game.entities.player import Player


#--------------------------CONTROLS--------------------------#

# MAIN
def handle_input(player: Player) -> None:
    _handle_keyboard_input(player)
    _handle_controller_input(player)

# KEYBOARD
def _handle_keyboard_input(player: Player):
    dx = 0
    dy = 0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_F3]:
        config.SHOW_OBJECT_COORDS = not config.SHOW_OBJECT_COORDS

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= 1

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += 1

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= 1

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += 1

    return (dx, dy)

# CONTROLLER
def _handle_controller_input(player: Player):
    if pygame.joystick.get_count() == 0:
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    axis_x = joystick.get_axis(0)
    axis_y = joystick.get_axis(1)

    threshold = 0.2

    if axis_x < -threshold:
        player.move(-1, 0)

    if axis_x > threshold:
        player.move(1, 0)

    if axis_y < -threshold:
        player.move(0, -1)

    if axis_y > threshold:
        player.move(0, 1)
