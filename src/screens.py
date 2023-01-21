import pygame

from constants import (FPS, WIDTH, HEIGHT, terminate)
from texts import Text, blink_text


def start_screen(surface):
    Text('NashTetris', 80,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.5, 0, 0),
         True).draw(surface)
    return blink_text(surface)


def pause_screen(surface):
    Text('Game Paused', 60,
         pygame.Rect(WIDTH * 0.5,
                     HEIGHT * 0.5, 0, 0), True).draw(surface, True)
    return blink_text(surface)


def game_over(surface, score):
    Text('Game Over', 60,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.25, 0, 0),
         True).draw(surface, True)
    Text(f'Total Score: {score.get_score()}', 45,
         pygame.Rect(WIDTH * 0.5, HEIGHT * 0.5, 0, 0),
         True).draw(surface)
    color = 55
    line = Text('press ESCAPE for exit, SPACE for new game', 35,
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
