import pygame
import sys
import os

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 1000
FIELD_SIZE = FIELD_HEIGHT, FIELD_WIDTH = 20, 10
BLOCK = pygame.Rect(0, 0, 40, 40)
BORDER_W = 5

# Событие падения блока
DOWNEVENT = pygame.USEREVENT + 1
# Места хранения спрайтов для клеток разных цветов
CELL_SPRITES = ["empty-cell.bmp", "red-cell.bmp", "blue-cell.bmp",
                "green-cell.bmp", "yellow-cell.bmp", "orange-cell.bmp",
                "purple-cell.bmp"]
CELL_COLORS = [pygame.sprite.Sprite() for _ in range(len(CELL_SPRITES))]
for i, sprite in enumerate(CELL_COLORS):
    sprite.image = pygame.image.load(
        os.path.join('src/data', CELL_SPRITES[i]))
    sprite.rect = sprite.image.get_rect()

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
