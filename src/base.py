import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    """ Load image and return image object """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image.convert()
        else:
            image.convert_alpha()
    except pygame.error as e:
        print('Cannot load image:', fullname)
        raise SystemExit from e
    return image


def load_sound(name):

    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    return pygame.mixer.Sound(os.path.join('data', name))
