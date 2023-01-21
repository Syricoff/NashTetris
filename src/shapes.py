import pygame
import random
from itertools import product
from constants import (HEIGHT, FIELD_HEIGHT, FIELD_WIDTH,
                       BLOCK, BORDER_W, CELL_COLORS, BLOCK_SHAPES)
from texts import Text


class Cell:
    def __init__(self, y, x, state=False, color=None):
        self.coords = (y, x)
        # state - наличие кубика в клетке
        self.state = state
        self.color = color if self.state else 0

    def get_state(self):
        return self.state

    def get_coords(self):
        return self.coords

    def get_color(self):
        return self.color

    # Поставить в клетку квадрат
    def fill(self, color):
        self.state = True
        self.color = color

    # Удалить квадрат из клетки
    def erase(self):
        self.state = False
        self.color = None

    def move(self, y, x):
        self.coords = (y, x)

    def __bool__(self):
        return self.get_state()

    def __eq__(self, other) -> bool:
        return bool(self) == bool(other)

    def __repr__(self) -> str:
        return f'Cell({self.coords}, {self.state}, {self.color}'


class Block:
    def __init__(self, shape=None, color=None,
                 start_y=FIELD_HEIGHT - 2,
                 start_x=FIELD_WIDTH // 2 - 2):
        # Задаем позицию левого нижнего угла нового блока
        self.pos = (start_y, start_x)
        # Генерируем случайный цвет, выбираем случайную форму
        self.color = color
        if not color:
            self.color = random.randint(1, len(CELL_COLORS) - 1)
        self.shape = shape
        if not shape:
            shape = random.choice(BLOCK_SHAPES)
        self.rect = pygame.Rect(0, 0, BLOCK.w * len(shape[0]),
                                BLOCK.h * len(shape))
        # Заполняем поле данными, если они не были даны в конструкторе
        # (Для корректной работы collide)
        self.field = [[Cell(y, x, shape[y][x], self.color)
                       for x in range(len(shape))]
                      for y in range(len(shape))]

    # Запрос длины стороны поля блока
    def size(self):
        return len(self.field)

    # Запрос цвета блока
    def get_color(self):
        return self.color

    # Перемещение вправо
    def right(self):
        self.pos = (self.pos[0], self.pos[1] + 1)

    # Перемещение влево
    def left(self):
        self.pos = (self.pos[0], self.pos[1] - 1)

    # Перемещение вверх
    def down(self):
        self.pos = (self.pos[0] - 1, self.pos[1])

    # Перемещение вниз (в случае когда коллайд сработал будем вызывать)
    def up(self):
        self.pos = (self.pos[0] + 1, self.pos[1])

    # поворачиваем блок по часовой стрелке
    def flip(self):
        temporary_field = Block([[cell.get_state()for cell in row]
                                 for row in self.field], self.get_color())
        for y in range(self.size()):
            for x in range(self.size()):
                self[y][x] = temporary_field[x][self.size() - y - 1]
        self.update_coords()

    # Поворачиваем блок против часовой стрелки
    # (в случае когда коллайд сработал будем вызывать)
    def unflip(self):
        temporary_field = Block([[cell.get_state() for cell in row]
                                 for row in self.field], self.get_color())
        for y in range(self.size()):
            for x in range(self.size()):
                self.field[x][self.size() - y - 1] = temporary_field[y][x]
        self.update_coords()

    # Проверка на пересечение с фрагментом поля стакана
    def collide(self, other):
        for y in range(self.size()):
            for x in range(self.size()):
                if self[y][x] == other[y][x] and self[y][x]:
                    return True
        return False

    # Обновляем координаты всех клеток внутри поля
    def update_coords(self):
        for i, j in product(range(self.size()), range(self.size())):
            self[i][j].move(i, j)

    # Реализовал методы для удобной работы с классом как со списком
    def __getitem__(self, key):
        return self.field[key]

    def __setitem__(self, key, value):
        self.field[key] = value

    def __delitem__(self, key):
        del self.field[key]

    def __iter__(self):
        return iter(self.field)


class Field:
    def __init__(self, row, column) -> None:
        self.rect = pygame.Rect(20,
                                HEIGHT - (row * BLOCK.h +
                                          BORDER_W * 2) - 20,
                                column * BLOCK.w + BORDER_W * 2,
                                row * BLOCK.h + BORDER_W * 2)
        # Заполняем поле пыстыми клетками
        self.field = [[Cell(i, j) for i in range(column)] for j in range(row)]
        # Создаем два блока - текущий и следующий
        self.new_block = Block()
        self.create_block()

    # Реализовал методы для работы с классом как со списком
    def __len__(self):
        return len(self.field)

    def __getitem__(self, key):
        return self.field[key]

    def __setitem__(self, key, value):
        self.field[key] = value

    def __delitem__(self, key):
        del self.field[key]

    def __iter__(self):
        return iter(self.field)

    def __repr__(self):
        return str(self.field)

    # Создание нового блока
    def create_block(self):
        self.block = self.new_block
        self.new_block = Block()

    # Выводим текст 'Next Shape' и отрисовываем следующую фигуру
    def next_shape(self, surface, rect):
        text_rect = rect.copy()
        text_rect.y = text_rect.y - 55
        image = pygame.Surface(self.new_block.rect.size)
        for row, line in enumerate(self.new_block[::-1]):
            for column, cell in enumerate(line):
                if cell:
                    pos = pygame.Rect(((column * BLOCK.w),
                                       (row * BLOCK.w)),
                                      BLOCK.size)
                    pygame.draw.rect(
                        image, CELL_COLORS[cell.get_color()], pos, 0)
        image_rect = image.get_rect()
        image_rect.midtop = rect.topleft
        surface.blit(image, image_rect)
        Text('Next Shape', 45,
             text_rect,
             True).draw(surface)

    # "Запекаем" блок на поле, после вызова он станет его частью
    def bake(self):
        b_y, b_x = self.block.pos
        for y in range(b_y, b_y + self.block.size()):
            for x in range(b_x, b_x + self.block.size()):
                if (0 <= y < FIELD_HEIGHT and 0 <= x < FIELD_WIDTH and
                   self.block[y - b_y][x - b_x]):
                    self[y][x] = self.block[y - b_y][x - b_x]
        self.update_coords()

    # Говорим, пересекает ли в текущем положении блок какую-либо клетку поля
    def collide(self):
        colliding_part = [
            [True for _ in range(self.block.size())]
            for _ in range(self.block.size())
        ]
        b_y, b_x = self.block.pos
        # Делаем матрицу пересечения
        for y in range(b_y, b_y + self.block.size()):
            for x in range(b_x, b_x + self.block.size()):
                if y >= FIELD_HEIGHT:
                    colliding_part[y - b_y][x - b_x] = False
                elif y < 0 or x < 0 or x >= FIELD_WIDTH or self[y][x]:
                    colliding_part[y - b_y][x - b_x] = True
                else:
                    colliding_part[y - b_y][x - b_x] = False

        # Используем матрицу для создания временного блока
        temporary_block = Block(colliding_part)
        # Пересекаем временный блок с основным
        return temporary_block.collide(self.block)

    # Движение блока вправо с коллайдом
    def move_right(self):
        self.block.right()
        if self.collide():
            self.block.left()

    # Движение блока влево с коллайдом
    def move_left(self):
        self.block.left()
        if self.collide():
            self.block.right()

    def flip(self):
        self.block.flip()
        if self.collide():
            self.block.left()
        if self.collide():
            self.block.left()
        if self.collide():
            for _ in range(3):
                self.block.right()
        if self.collide():
            self.block.right()
        if self.collide():
            self.block.left()
            self.block.left()
            self.block.unflip()

    # Движение блока вниз с коллайдом и переходом к новому блоку
    def move_down(self):
        self.block.down()
        if self.collide():
            self.block.up()
            self.bake()
            self.create_block()

    def draw(self, surface):
        # Создаём пустой холст размером поля
        image = pygame.Surface(self.rect.size)
        # Рисуем границы стакана
        pygame.draw.rect(image, 'white', image.get_rect(), BORDER_W)
        # Проходим в цикле по перевёрнутой матрице поля
        for row, line in enumerate(self[::-1]):
            for column, cell in enumerate(line):
                if cell:
                    # Определяем позицию клетки
                    pos = pygame.Rect((BLOCK.w * column + BORDER_W,
                                       BLOCK.h * row + BORDER_W),
                                      BLOCK.size)
                    # Рисуем клетку
                    pygame.draw.rect(
                        image, CELL_COLORS[cell.get_color()], pos, 0)
        block_y, block_x = self.block.pos
        for line in self.block[::-1]:
            for cell in line:
                x_pos = block_x + cell.get_coords()[1]
                y_pos = block_y + cell.get_coords()[0]
                if cell and 0 <= x_pos < FIELD_WIDTH and \
                        0 <= y_pos < FIELD_HEIGHT:
                    # Определяем позицию клетки
                    pos = pygame.Rect((BLOCK.w * x_pos + BORDER_W,
                                       BLOCK.h * (FIELD_HEIGHT - y_pos - 1)
                                       + BORDER_W),
                                      BLOCK.size)
                    pygame.draw.rect(
                        image, CELL_COLORS[cell.get_color()], pos, 0)
        # Переноим изображение на основной холст
        surface.blit(image, self.rect)

    def clean_lines(self, score):
        self.field = list(filter(lambda x: not all(x), self))
        score.update(FIELD_HEIGHT - len(self))
        self.field.extend([Cell(i, j) for i in range(FIELD_WIDTH)]
                          for j in range(FIELD_HEIGHT - len(self)))
        self.update_coords()

    def update_coords(self):
        for i, j in product(range(FIELD_HEIGHT), range(FIELD_WIDTH)):
            self[i][j].move(i, j)
