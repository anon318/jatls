#--------------------------IMPORTS--------------------------#


import pygame
from game.engine import Game


#--------------------------MAIN FUNCTION--------------------------#


def main():
    # Initialize pygame and setup window
    pygame.init()
    screen = pygame.display.set_mode((854, 480)) # Supposed to be 700, 500 according to config, but this works so don't change ig?
    pygame.display.set_caption("Jaden and the Lost Starfruit")

    # Create game instance
    game = Game(screen)

    # Start game loop
    game.load_scene("level1")
    game.run()

    # Clean up on exit
    pygame.quit()


#--------------------------ENTRY POINT--------------------------#


if __name__ == "__main__":
    main()
