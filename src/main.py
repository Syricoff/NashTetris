from itertools import product
import pygame
import random
import os
import sys

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 1000
FIELD_SIZE = FIELD_HEIGHT, FIELD_WIDTH = 16, 8
BLOCK = pygame.Rect(0, 0, 50, 50)
BORDER_W = 5

# Места хранения спрайтов для клеток разных цветов
CELL_COLORS = ("empty", "blue", "green", "yellow")
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
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False)
    )
)


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


def blink_text(surface,
               text='press any key to continue',
               rect=pygame.Rect(WIDTH * 0.5, HEIGHT * 0.55, 0, 0)):
    color = 55
    clock = pygame.time.Clock()
    line = Text(text, 35, rect, color=(color,) * 3)
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
        line.set_color((color,) * 3)
        line.draw(surface)
        pygame.display.flip()


def start_screen(surface):
    Text('NashTetris', 80,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.5, 0, 0),
         True).draw(surface)
    return blink_text(surface)


def pause_screen(surface):
    Text('Game Paused', 60,
         pygame.Rect(WIDTH * 0.5,
                     HEIGHT * 0.5, 0, 0)).draw(surface, True)
    return blink_text(surface)


def game_over(surface):
    # Дописать вывод итогов игры и кнопки для дальнейших действий
    Text('Game Over', 60,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.5, 0, 0),
         True).draw(surface, True)
    return blink_text(surface)


def exit_screen(surface):
    Text('Exit?', 60,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.5, 0, 0),
         title=True).draw(surface, True)
    Text('All progress will be clear', 30,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.55, 0, 0),
         color='red').draw(surface)
    # Задаём цвет и текст для мерцания
    color = 55
    line = Text('press ESCAPE for exit, SPACE for resume', 35,
                pygame.Rect(WIDTH * 0.5, HEIGHT * 0.58, 0, 0),
                color=(color,) * 3)
    # Цикл окна с запросом кнопок
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    terminate()
        if color == 255:
            flag = False
        elif color == 55:
            flag = True
        color += 1 if flag else -1
        line.set_color((color,) * 3)
        line.draw(surface)
        pygame.display.flip()


class Text:
    def __init__(self, text, size, rect, title=False, color='white'):
        self.size = size
        self.font = pygame.font.Font('src/data/ChargeVectorBlack.ttf',
                                     self.size) if title else pygame.font.Font(
                                         None, self.size)
        self.color = color
        self.text = text
        self.draweble = self.font.render(self.text, True, self.color)
        self.rect = self.draweble.get_rect()
        self.rect.center = rect.topleft

    def draw(self, surface, dim=False):
        if dim:
            self.dim_screen(surface)
        surface.blit(self.draweble, self.rect)

    def dim_screen(self, surface):
        screen = pygame.Surface(SIZE, pygame.SRCALPHA)
        screen.fill((0, 0, 0, 175))
        surface.blit(screen, (0, 0))

    def get_rect(self):
        return self.rect

    def set_color(self, color):
        self.color = color
        self.draweble = self.font.render(self.text, True, self.color)


class Cell:
    def __init__(self, y, x, state=False, color=None):
        self.coords = (y, x)
        # state - наличие кубика в клетке
        self.state = state
        self.color = color

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

    def __repr__(self) -> str:
        return f'Cell({self.coords}, {self.state}, {self.color}'


class Block():
    def __init__(self, field=None,
                 start_x=FIELD_HEIGHT - 2,
                 start_y=FIELD_WIDTH // 2 - 2):
        # Задаем позицию левого нижнего угла нового блока
        self.pos = (start_x, start_y)
        # Генерируем случайный цвет, выбираем случайную форму
        self.color = random.randint(1, len(CELL_COLORS))
        shape = random.choice(BLOCK_SHAPES)
        # Заполняем поле данными, если они не были даны в конструкторе(Для корректной работы collide)
        self.field = field
        if not self.field:
            self.field = [[Cell(y, x, shape[y][x], self.color)
                           for x in range(len(shape))]
                          for y in range(len(shape))]

    # Запрос длины стороны поля блока
    def size(self):
        return len(self.field)

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
        temporary_field = self.field
        for y in range(self.size()):
            for x in range(self.size()):
                self.field[y][x] = temporary_field[x][self.size() - y - 1]
                # Изменяя клетку, изменяем и ее координаты
                self.field[y][x].move(y, x)

    # поворачиваем блок против часовой стрелки(в случае когда коллайд сработал будем вызывать)
    def unflip(self):
        temporary_field = self.field
        for y in range(self.size()):
            for x in range(self.size()):
                self.field[x][self.size() - y - 1] = temporary_field[y][x]
                # Изменяя клетку, изменяем и ее координаты
                self.field[x][self.size() - y - 1].move(x,
                                                        self.size() - y - 1)

    # Проверка на пересечение с фрагментом поля стакана
    def collide(self, other):
        for y in range(self.size()):
            for x in range(self.size()):
                if self[y][x] == other[y][x] and self[y][x]:
                    return True
        return False

    # Реализовал методы, для удобной работы с классом как со списком
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

    # "Запекаем" блок на поле, после вызова он станет его частью
    def bake(self):
        b_x, b_y = self.block.pos()
        for y in range(b_y, b_y + self.block.size()):
            for x in range(b_x, b_x + self.block.size()):
                if y < 0 or x < 0 or x >= FIELD_WIDTH or y >= FIELD_HEIGHT:
                    pass
                else:
                    self[y][x] = self.block[y - b_y][x - b_x]
        self.update_coords()

    # Говорим, пересекает ли в текущем положении блок какую-либо клетку поля
    def collide(self):
        colliding_part = [
            [True for _ in range(self.block.size())]
            for _ in range(self.block.size())
        ]
        b_x, b_y = self.block.pos()
        # Делаем матрицу пересечения
        for y in range(b_y, b_y + self.block.size()):
            for x in range(b_x, b_x + self.block.size()):
                if y >= FIELD_HEIGHT:
                    colliding_part[y - b_y][x - b_x] = False
                elif y < 0 or x < 0 or x >= FIELD_WIDTH:
                    colliding_part[y - b_y][x - b_x] = True
                else:
                    colliding_part[y - b_y][x - b_x] = self[y][x]
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
                    pygame.draw.rect(image, cell.get_color(), pos, 0)
        block_y, block_x = self.block.pos
        for row, line in enumerate(self.block[::-1]):
            for column, cell in enumerate(line):
                x_pos = block_x + cell.get_coords()[1]
                y_pos = block_y + cell.get_coords()[0]
                if cell and 0 <= x_pos < FIELD_WIDTH and 0 <= y_pos < FIELD_HEIGHT:
                    # Определяем позицию клетки
                    pos = pygame.Rect((BLOCK.w * x_pos + BORDER_W,
                                       BLOCK.h * (15 - y_pos) + BORDER_W),
                                      BLOCK.size)
                    pygame.draw.rect(image, cell.get_color(), pos, 0)
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


class Score:
    def __init__(self, pos):
        self.score = 0
        self.level = 1
        self.lines = 0
        self.pos = pos
        self.text = [
            f"Lines: {self.lines}",
            f"Score: {self.score}",
            f"Level: {self.level}"
        ]

    def draw(self, surface):
        sep = 40
        x, y = self.pos
        for text in self.text:
            y += sep
            Text(text, 45, pygame.Rect((x, y), (0, 0))).draw(surface)

    def update(self, lines):
        self.lines += lines
        if lines == 4:
            self.score += 1500
        elif lines == 3:
            self.score += 700
        elif lines == 2:
            self.score += 300
        elif lines == 1:
            self.score += 100
        if self.score % (self.level * 10000) == 0:
            self.level += 1
        # Обновляю тексты
        self.text = [
            f"Lines: {self.lines}",
            f"Score: {self.score}",
            f"Level: {self.level}"
        ]


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('NashTetris')
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 200)
    # Создание объектов
    field = Field(*FIELD_SIZE)
    title = Text('NashTetris', 80,
                 pygame.Rect(WIDTH * 0.5,
                             HEIGHT * 0.08, 0, 0), True)
    score = Score((WIDTH * 0.75, HEIGHT * 0.7))
    field[0] = [Cell(i, 0, True, 'red') for i in range(FIELD_WIDTH)]
    field[1][5] = Cell(1, 5, True, 'red')
    field[2] = [Cell(i, 0, True, 'red') for i in range(FIELD_WIDTH)]
    field[3][2] = Cell(1, 5, True, 'red')
    field[4] = [Cell(i, 0, True, 'red') for i in range(FIELD_WIDTH)]
    field[5] = [Cell(i, 0, True, 'red') for i in range(FIELD_WIDTH)]
    # Стартовый экран
    running = start_screen(screen)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_screen(screen)
                if event.key == pygame.K_g:  # для тестов
                    field.clean_lines(score)
                if event.key == pygame.K_ESCAPE:
                    exit_screen(screen)
        screen.fill('black')
        title.draw(screen)
        field.draw(screen)
        score.draw(screen)
        pygame.display.flip()
    terminate()
