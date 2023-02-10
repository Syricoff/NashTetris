import pygame

from constants import (FPS, SIZE, WIDTH, HEIGHT, terminate)


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


class Score:
    def __init__(self, pos):
        self.score = 0
        self.level = 1
        self.lines = 0
        self.pos = pos
        self.max_score = int(open("src/data/max_score.txt", 'r').readline().strip())
        self.text = [
            f"Max Score: {self.max_score}",
            f"Lines: {self.lines}",
            f"Score: {self.score}",
            f"Level: {self.level}"
        ]

    def draw(self, surface):
        sep = 60
        x, y = self.pos
        for text in self.text:
            y += sep
            Text(text, 40, pygame.Rect((x, y), (0, 0)), True).draw(surface)

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
        if self.score != 0 and self.score / 1000 >= self.level:
            self.level += 1
        if self.score >= self.max_score:
            self.update_max_score()
        # Обновляю тексты
        self.text = [
            f"Max Score: {self.max_score}",
            f"Lines: {self.lines}",
            f"Score: {self.score}",
            f"Level: {self.level}"
        ]

    def update_max_score(self):
        print(f'{self.score}', file=open("src/data/max_score.txt", 'w'))
        self.max_score = int(open("src/data/max_score.txt", 'r').readline())

    def get_score(self):
        return self.score

    def get_level(self):
        return self.level
