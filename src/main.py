import pygame
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    """ Load image and return image object """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert() if image.get_alpha() is None else image.convert_alpha()
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

    fullname = os.path.join('data', name)
    return pygame.mixer.Sound(fullname)


def show_text(screen, text: tuple | list, color='white', title=False):
    press_key_font = pygame.font.Font(None, 30)
    # Сюда надо разные шрифты
    font = pygame.font.Font(None, 60) if title else pygame.font.Font(None, 60)
    titleSurf = font.render(text, True, color)
    titleRect = titleSurf.get_rect()
    titleRect.center = (int(WIDTH / 2), int(HEIGHT / 2))
    screen.blit(titleSurf, titleRect)
    # Надо прикрутить мерциющий текст
    pressKeySurf = press_key_font.render('press any key to countine', True, color)
    pressKeyRect = titleSurf.get_rect()
    pressKeyRect.center = (10 + pressKeyRect.w / 2, HEIGHT - pressKeyRect.h)
    screen.blit(pressKeySurf, pressKeyRect)


def start_screen():
    show_text(screen, 'Tetris game', title=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return True
        pygame.display.flip()
        clock.tick(FPS)


class Field():
    def __init__(self, row, column) -> None:
        self.rect = pygame.Rect(10, (HEIGHT - row * BLOCK_H + BORDER_W * 2) / 2, column * BLOCK_W + BORDER_W * 2, row * BLOCK_H + BORDER_W * 2)
        self.field = [[None for _ in range(column)] for _ in range(row)]
        
    def draw(self, surface):
        image = pygame.Surface(self.rect.size)
        pygame.draw.rect(image, 'white', image.get_rect(), BORDER_W)
        surface.blit(image, self.rect)

if __name__ == '__main__':
    FPS = 60
    WIDTH, HEIGHT = 600, 1000
    BLOCK_SIZE = BLOCK_W, BLOCK_H = (50, 50)
    BORDER_W = 10

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 200)
    
    field = Field(16, 8)

    running = start_screen() # Возможно надо будет как то по другому это сделать

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        field.draw(screen)
        pygame.display.flip()
    terminate()
