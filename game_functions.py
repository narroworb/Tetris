import random
import pygame

def create_grid(locked_position={}, rect_size=25, black=(0, 0, 0)):
    grid = [[black for _ in range(16)] for _ in range(28)]
    for y in range(29):
        for x in range(17):
            if (x * rect_size, y * rect_size + 50) in locked_position:
                grid[y-1][x] = locked_position[(x * rect_size, y * rect_size + 50)]
    return grid

def valid_moving(cur_fig, rect_size=25, locked_position={}):
    extreme_left, extreme_right, extreme_down = False, False, False
    for y in range(len(cur_fig.form)):
        for x in range(len(cur_fig.form[y])):
            if cur_fig.form[y][x] == 1:
                if x * rect_size + cur_fig.x == 0 or (x * rect_size + cur_fig.x - rect_size, (y - 2) * rect_size + (cur_fig.y // rect_size) * rect_size) in locked_position.keys():
                    extreme_left = True
                if x * rect_size + cur_fig.x == 375 or (x * rect_size + cur_fig.x + rect_size, (y - 2) * rect_size + (cur_fig.y // rect_size) * rect_size) in locked_position.keys():
                    extreme_right = True
                if y * rect_size + cur_fig.y >= 825:
                    extreme_down = True
                    cur_fig.y = 825 - y * rect_size
                if (x * rect_size + cur_fig.x, (y - 2) * rect_size + (cur_fig.y // rect_size) * rect_size) in locked_position.keys():
                    extreme_down = True
                    cur_fig.y = (cur_fig.y // rect_size) * rect_size - rect_size
    return (extreme_left, extreme_right, extreme_down)

def figure_move(event, validation, rect_size=25, fall_speed=5):
    if event.key == pygame.K_RIGHT and not validation[1]:
        return (rect_size, 0)
    if event.key == pygame.K_LEFT and not validation[0]:
        return (-rect_size, 0)
    if event.key == pygame.K_DOWN and not validation[2]:
        return (0, rect_size)
    if not validation[2]:
        return (0, fall_speed)
    return (0, 0)

def deleting_row(points_counter, locked_position={}, rect_size=25):
    locked_position_coordinates = []
    for (x, y) in locked_position.keys():
        locked_position_coordinates.append(y)
    for y in range(0, 751, rect_size):
        if locked_position_coordinates.count(y) == 16:
            points_counter += 10
            for x in range(0, 401, rect_size):
                if (x, y) in locked_position.keys():
                    del locked_position[(x, y)]
                for y_upper in range(y - rect_size, 150, -rect_size):
                    if (x, y_upper) in locked_position.keys():
                        locked_position[(x, y_upper + rect_size)] = locked_position[(x, y_upper)]
                        del locked_position[(x, y_upper)]
    return locked_position, points_counter

class Figure:
    def __init__(self, x, y, form, colors):
        self.x = x
        self.y = y
        self.form = [[0 for _ in range(4)] for _ in range(4)]
        for y in range(4):
            for x in range(4):
                self.form[y][x] = form[y][x]
        self.rotation = 0
        self.color = random.choice(list(colors.values()))

    def change_rotation(self, locked_position={}, rect_size=25):
        copy_form = []
        for row in self.form:
            copy_row = []
            for item in row:
                copy_row.append(item)
            copy_form.append(copy_row)
        max_right_prev, max_right_post = 0, 0
        for y in range(len(self.form)):
            if max_right_prev < max([i if self.form[y][i] == 1 else 0 for i in range(len(self.form[y]))]):
                max_right_prev = max([i if self.form[y][i] == 1 else 0 for i in range(len(self.form[y]))])
            if max_right_post < max([i if copy_form[3 - i][y] == 1 else 0 for i in range(len(copy_form[y]))]):
                max_right_post = max([i if copy_form[3 - i][y] == 1 else 0 for i in range(len(copy_form[y]))])
        if (375 - (self.x + rect_size * max_right_prev)) - (max_right_post - max_right_prev) * rect_size < 0:
            self.rotation = (self.rotation + 3) % 4
            return
        min_left_prev, min_left_post = 3, 3
        for y in range(len(self.form)):
            if min_left_prev > min([i if self.form[y][i] == 1 else 4 for i in range(len(self.form[y]))]):
                min_left_prev = min([i if self.form[y][i] == 1 else 4 for i in range(len(self.form[y]))])
            if min_left_post > min([i if copy_form[3 - i][y] == 1 else 4 for i in range(len(copy_form[y]))]):
                min_left_post = min([i if copy_form[3 - i][y] == 1 else 4 for i in range(len(copy_form[y]))])
        if (self.x + rect_size * min_left_prev) - (min_left_prev - min_left_post) * rect_size < 0:
            self.rotation = (self.rotation + 3) % 4
            return
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if copy_form[y][x] == 1:
                    if ((3 - x) * rect_size + self.x, y * rect_size + (self.y // rect_size) * rect_size) in locked_position.keys():
                        self.rotation = (self.rotation + 3) % 4
                        return
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                self.form[y][x] = copy_form[3 - x][y]
