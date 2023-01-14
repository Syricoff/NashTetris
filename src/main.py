import pygame
import os
import sys

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 1000
BLOCK_SIZE = pygame.Rect(0, 0, 50, 50)
BORDER_W = 5


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
    return pygame.mixer.Sound(os.path.join('data', name))


def show_centered_text(surface, text: tuple | list, color='white', title=False):
    font = pygame.font.Font('src/data/ChargeVectorBlack.ttf', 80) if title else pygame.font.Font(None, 60)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (int(WIDTH / 2), int(HEIGHT / 2))
    surface.blit(text, textRect)


def show_title(surface):
    font = pygame.font.Font('src/data/ChargeVectorBlack.ttf', 80)
    text = font.render('NashTetris', True, 'white')
    textRect = text.get_rect()
    textRect.center = (int(WIDTH / 2), textRect.h)
    surface.blit(text, textRect)


def blink_text(surface):
    press_key_font = pygame.font.Font(None, 35)
    color = 55
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return True
        if color == 255:
            flag = False
        elif color == 55:
            flag = True
        color += 1 if flag else -1
        pressKeySurf = press_key_font.render('press any key to countine', True, (color, color, color))
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.center = (WIDTH / 2, HEIGHT * 0.55)
        surface.blit(pressKeySurf, pressKeyRect)
        pygame.display.flip()


def start_screen(surface):
    show_centered_text(surface, 'NashTetris', title=True)
    return blink_text(surface)


def dim_screen(surface):
    screen = pygame.Surface(SIZE, pygame.SRCALPHA)
    screen.fill((0, 0, 0, 175))
    surface.blit(screen, (0, 0))


def pause_screen(surface):
    dim_screen(surface)
    show_centered_text(surface, 'Game Paused')
    return blink_text(surface)


def game_over(surface):
    dim_screen(surface)
    show_centered_text(surface, 'Game Over')
    return blink_text(surface)


class Field():
    def __init__(self, row, column) -> None:
        self.rect = pygame.Rect(20,
                                HEIGHT - (row * BLOCK_SIZE.h + BORDER_W * 2) - 20,
                                column * BLOCK_SIZE.w + BORDER_W * 2,
                                row * BLOCK_SIZE.h + BORDER_W * 2)
        self.field = [[None for _ in range(column)] for _ in range(row)]

    # Реализовал методы, для удобной работы с классом как со списком
    def __len__(self):
        return len(self.rect)

    def __getitem__(self, key):
        return self.field[key]

    def __setitem__(self, key, value):
        self.field[key] = value

    def __delitem__(self, key):
        del self.field[key]

    def __iter__(self):
        return iter(self.field)

    def draw(self, surface):
        # Создаём пустой холст размером поля
        image = pygame.Surface(self.rect.size)
        # Рисуем границы стакана
        pygame.draw.rect(image, 'white', image.get_rect(), BORDER_W)
        # Проходим в цикле по перевёрнутой матрице поля
        for row, line in enumerate(self[::-1]):
            for column, cell in enumerate(line):
                if cell:  # Если в ячейке есть блок
                    # Определяем позицию блока
                    pos = pygame.Rect((BLOCK_SIZE.w * column + BORDER_W,
                                       BLOCK_SIZE.h * row + BORDER_W),
                                      BLOCK_SIZE.size)
                    # Рисуем блок
                    # Пока рисует красным цветом, будут картинки
                    pygame.draw.rect(image, 'red', pos, 0)
        # Переноим изображение на соновной холст
        surface.blit(image, self.rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 200)
    # Создание объектов
    field = Field(16, 8)
    # Стартовый экран
    running = start_screen(screen)  # Возможно надо будет как то по другому это сделать
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_screen(screen)
        screen.fill('black')
        show_title(screen)
        field.draw(screen)
        pygame.display.flip()
    terminate()
