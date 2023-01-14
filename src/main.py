import pygame
import random
import os
import sys

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 1000
FIELD_SIZE = FIELD_HEIGHT, FIELD_WIDTH = 16, 8
BLOCK_SIZE = pygame.Rect(0, 0, 50, 50)
BORDER_W = 5

CELL_COLORS = ["empty", "1st", "2nd", "3rd"]
BLOCK_SHAPES = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
]


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


def show_centered_text(surface, text: tuple | list, title=False):
    font = pygame.font.Font('src/data/ChargeVectorBlack.ttf', 80) if title else pygame.font.Font(None, 60)
    text = font.render(text, True, 'white')
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
        pressKeySurf = press_key_font.render('press any key to countine', True,
                                             (color, color, color), 'black')
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


class Cell():
    def __init__(self, y, x, state=False, color=None):
        self.coords = (y, x)
        self.state = state
        self.color = color

    def get_state(self):
        return self.state

    def get_coords(self):
        return self.coords

    def get_color(self):
        return self.color

    def fill(self, color):
        self.state = True
        self.color = color

    def erase(self):
        self.state = False
        self.color = None

    def __bool__(self):
        return self.get_state()


class Block():
    def __init__(self, start_x=FIELD_HEIGHT, start_y=FIELD_WIDTH):
        self.pos = (start_x, start_y)
        self.color = random.randint(1, len(CELL_COLORS))
        shape = random.choice(BLOCK_SHAPES)
        self.field = [[Cell(y, x, shape[y][x], self.color)
                       for x in range(4)] for y in range(4)]


class Field():
    def __init__(self, row, column) -> None:
        self.rect = pygame.Rect(20,
                                HEIGHT - (row * BLOCK_SIZE.h + BORDER_W * 2) - 20,
                                column * BLOCK_SIZE.w + BORDER_W * 2,
                                row * BLOCK_SIZE.h + BORDER_W * 2)
        self.field = [[Cell(i, j) for i in range(column)] for j in range(row)]

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
                if cell:
                    # Определяем позицию блока
                    pos = pygame.Rect((BLOCK_SIZE.w * column + BORDER_W,
                                       BLOCK_SIZE.h * row + BORDER_W),
                                      BLOCK_SIZE.size)
                    # Рисуем блок
                    # Пока рисует красным цветом, будут картинки
                    pygame.draw.rect(image, cell.get_color(), pos, 0)
        # Переноим изображение на соновной холст
        surface.blit(image, self.rect)

    def clean_lines(self):
        clean_lines = []
        for row, line in enumerate(self):
            if all(line):
                clean_lines.append(row)
            else:
                break
        self.field.extend([None for i in range(len(clean_lines))])
        for i in clean_lines:
            del self[i]


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 200)
    # Создание объектов
    field = Field(*FIELD_SIZE)
    field[0] = [Cell(i, 0, True, 'red') for i in range(FIELD_WIDTH)]
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
                if event.key == pygame.K_g:
                    field.clean_lines()
        screen.fill('black')
        show_title(screen)
        field.draw(screen)
        pygame.display.flip()
    terminate()
