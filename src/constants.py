import pygame
import sys

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 1000
FIELD_SIZE = FIELD_HEIGHT, FIELD_WIDTH = 20, 10
BLOCK = pygame.Rect(0, 0, 40, 40)
BORDER_W = 5

# Событие падения блока
DOWNEVENT = pygame.USEREVENT + 1
# Места хранения спрайтов для клеток разных цветов
CELL_COLORS = ("black", "blue", "green", "yellow",
               "red", "orange", "purple", "brown")
# Формы падающих фигур для генерации
BLOCK_SHAPES = (
    (
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
        (False, False, False, False)
    ),
    (
        (False, False, False),
        (True, True, True),
        (False, True, False)
    ),
    (
        (False, False, False),
        (True, True, True),
        (True, False, False)
    ),
    (
        (False, False, False),
        (True, True, True),
        (False, False, True)
    ),
    (
        (False, False, True),
        (False, True, True),
        (False, True, False)
    ),
    (
        (True, False, False),
        (True, True, False),
        (False, True, False)
    ),
    (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False)
    )
)


def terminate():
    pygame.quit()
    sys.exit()
