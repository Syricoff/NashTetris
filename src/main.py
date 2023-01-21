import pygame

from constants import (FPS, SIZE, WIDTH, HEIGHT,
                       FIELD_SIZE, DOWNEVENT)
from shapes import Field
from texts import Text, Score
from screens import (pause_screen, start_screen,
                     game_over, exit_screen)
from base import terminate


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('NashTetris')
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 100)
    pygame.time.set_timer(DOWNEVENT, 1000)
    # Создание объектов
    field = Field(*FIELD_SIZE)
    title = Text('NashTetris', 80,
                 pygame.Rect(WIDTH * 0.5,
                             HEIGHT * 0.08, 0, 0), True)
    score = Score((WIDTH * 0.77, HEIGHT * 0.55))
    current_speed = 0
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
                elif event.key == pygame.K_ESCAPE:
                    exit_screen(screen)
                elif event.key == pygame.K_LEFT:
                    field.move_left()
                elif event.key == pygame.K_RIGHT:
                    field.move_right()
                elif event.key == pygame.K_DOWN:
                    field.move_down()
                elif event.key == pygame.K_UP:
                    field.flip()
            if event.type == DOWNEVENT:
                field.move_down()
                current_speed = score.get_level() * 100
                pygame.time.set_timer(DOWNEVENT,
                                      max(100, 1000 - current_speed))
        if all(any(row) for row in field):
            if game_over(screen, score):
                field = Field(*FIELD_SIZE)
                score = Score((WIDTH * 0.77, HEIGHT * 0.55))
                current_speed = 0
        screen.fill('black')
        title.draw(screen)
        field.draw(screen)
        score.draw(screen)
        field.next_shape(screen, pygame.Rect(WIDTH * 0.77, HEIGHT * 0.3, 0, 0))
        field.clean_lines(score)
        pygame.display.flip()
    terminate()
