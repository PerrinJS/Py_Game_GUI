#!/usr/bin/python
import sys
import pygame
from gui_interface.button import Button

SCREEN_SIZE = (100, 100)
BUTTON_WIDTH = 40
BUTTON_HEIGHT = 30
BUTTON_X_CENTERING = SCREEN_SIZE[0]/2-(BUTTON_WIDTH/2)
BUTTON_Y_CENTERING = SCREEN_SIZE[1]/2-(BUTTON_HEIGHT/2)
BLACK = (0, 0, 0)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    button = Button(
            screen,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            BUTTON_X_CENTERING,
            BUTTON_Y_CENTERING,
            "Hello!",
            (lambda: print("Clicked")))

    while pygame.QUIT not in map((lambda event: event.type), pygame.event.get()):
        screen.fill(BLACK)
        button.draw()
        pygame.display.flip()
else:
    print("Buttons test file is ment to run as a stand alone test script",
          file=sys.stderr)
