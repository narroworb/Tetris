import random
import pygame

from game_functions import create_grid, valid_moving, figure_move, deleting_row, Figure, setting_figure
from utils import start, restart, get_information, is_game_over

pygame.font.init()
black = (0, 0, 0)
white = (255, 255, 255)
colors = {'red': (255, 0, 0),
        'orange': (255, 165, 0),
        'yellow': (255, 255, 0),
        'green': (0, 150, 0),
        'blue': (0, 0, 255),
        'indigo': (75, 0, 130),
        'violet': (238, 130, 238)
        }
game_over, is_quit = False, False
game_over_font = pygame.font.Font('C:/Users/79611/PycharmProjects/Tetris/fonts/Boncegro FF 4F.otf', 50)
start_font = pygame.font.Font('C:/Users/79611/PycharmProjects/Tetris/fonts/Boncegro FF 4F.otf', 45)
title_font = pygame.font.Font('C:/Users/79611/PycharmProjects/Tetris/fonts/Boncegro FF 4F.otf', 70)
display_height, display_width = 850, 400
rect_size = 25
locked_position = {}
busy_cells = 0
points_counter = 0
start_time = 0
fall_speed = 5
difficulty = 20
forms ={'I': [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        'J': [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0]],
        'L': [[0, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]],
        'O': [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]],
        'S': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0]],
        'T': [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0]],
        'Z': [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0]]
       }
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()

def main():
    global game_over, locked_position, busy_cells, points_counter, start_time
    (starting, start_time) = start(start_font, title_font, dis, clock, colors)
    while not starting:
        pass
    while not is_quit:
        cur_fig = Figure(150, 150, random.choice(list(forms.values())), colors)
        next_fig = Figure(150, 150, random.choice(list(forms.values())), colors)
        while not game_over:
            get_information(next_fig, dis, points_counter, start_time)
            dx, dy = 0, fall_speed
            validation_move = valid_moving(cur_fig, locked_position=locked_position)
            if validation_move[2]:
                dy = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    (dx, dy) = figure_move(event, validation_move)
                    if event.key == pygame.K_SPACE:
                        cur_fig.rotation = (cur_fig.rotation + 1) % 4
                        cur_fig.change_rotation(locked_position=locked_position)
            cur_grid = create_grid(locked_position=locked_position)
            for y in range(len(cur_grid)):
                for x in range(len(cur_grid[y])):
                    pygame.draw.rect(dis, cur_grid[y][x], (x * rect_size, 150 + y * rect_size, rect_size, rect_size))
            cur_fig.y += dy
            cur_fig.x += dx
            locked_position = setting_figure(dy, dx, cur_fig, locked_position=locked_position)
            if len(locked_position) > busy_cells:
                cur_fig = next_fig
                next_fig = Figure(150, 150, random.choice(list(forms.values())), colors)
                game_over = is_game_over(cur_grid)
            (locked_position, points_counter) = deleting_row(points_counter, locked_position=locked_position)
            for y in range(4):
                for x in range(4):
                    if cur_fig.form[y][x] == 1:
                        pygame.draw.rect(dis, cur_fig.color, (x * rect_size + cur_fig.x, y * rect_size + cur_fig.y, rect_size, rect_size))
            pygame.display.update()
            clock.tick(difficulty)
            busy_cells = len(locked_position)

        (game_over, locked_position, busy_cells, start_time, points_counter) = restart(game_over_font, dis, clock, colors, points_counter)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()