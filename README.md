# **Игра Тетрис**
____
## *Описание*
Классическая игра тетрис, реализованная на Python с помощью библиотеки pygame. В коде реализована вся стандартная логика игры тетрис: 

1. Случайные фигурки падают сверху в прямоугольный стакан шириной 16 и высотой 28 клеток.
2. В полёте игрок может поворачивать фигурку на 90° и двигать её по горизонтали. Также можно «сбрасывать» фигурку, то есть ускорять её падение, когда уже решено, куда фигурка должна упасть.
3. Фигурка летит до тех пор, пока не наткнётся на другую фигурку, либо на дно стакана. Если при этом заполнился горизонтальный ряд из 16 клеток, он пропадает и всё, что выше него, опускается на одну клетку. 
4. Дополнительно показывается фигурка, которая будет следовать после текущей — это подсказка, которая позволяет игроку планировать действия.
5. Игра заканчивается, когда новая фигурка не может поместиться в стакан.
6. Игрок получает очки за каждый заполненный ряд, поэтому его задача — заполнять горизонтальные ряды, не заполняя сам стакан (предотвращая/не допуская его заполнение по вертикали) как можно дольше, чтобы таким образом получить как можно больше очков. 

____
## *Реализация*
Код программы разделён на три файла (`main.py`,`utils.py`, `game_functions.py`) для удобства последующего редактирования. 
### `main.py`
Файл `main.py` является головным и отвечает за подключение остальных файлов:
   ```python
from game_functions import create_grid, valid_moving, figure_move, deleting_row, Figure, setting_figure
from utils import start, restart, get_information, is_game_over
```
Также в этом файле прописаны все необходимые константы и инициализация нужных модулей бибилиотеки pygame.
  ```python
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
```
В единственной функции файла описан алгоритм функционирования игры:
```python
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

```
### `utils.py`
Файл `utils.py` отвечает за подключение за системные процессы в приложении, такие как запуск игры, определение поражения, перезапуск игры и вывод информации об игре:
   ```python
import random
import pygame

def start(start_font, title_font, dis, clock, colors, black=(0, 0, 0), display_width=400, display_height=850):
    start_message1 = start_font.render('ЧТОБЫ НАЧАТЬ ИГРУ,', True, random.choice(list(colors.values())))
    start_message2 = start_font.render('НАЖМИТЕ ПРОБЕЛ', True, random.choice(list(colors.values())))
    while 1:
        title = title_font.render('ТЕТРИС', True, random.choice(list(colors.values())))
        pygame.draw.rect(dis, black, (0, 0, display_width, display_height))
        dis.blit(title, (100, 200))
        dis.blit(start_message1, (22, 400))
        dis.blit(start_message2, (47, 450))
        pygame.display.flip()
        clock.tick(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_time = pygame.time.get_ticks()
                    return True, start_time

def get_information(next_fig, dis, points_counter, start_time, white=(255, 255, 255), black = (0, 0, 0), rect_size=25):
    pygame.draw.line(dis, white, [0, 149], [400, 149], 10)
    pygame.draw.line(dis, white, [133, 0], [133, 149], 5)
    pygame.draw.line(dis, white, [267, 0], [267, 149], 5)
    digits_font = pygame.font.Font('C:/Users/79611/PycharmProjects/Tetris/fonts/Eurofightersemital.ttf', 36)
    text_font = pygame.font.Font('C:/Users/79611/PycharmProjects/Tetris/fonts/SkrampCyr-Regular_0.ttf', 20)
    cur_time = (pygame.time.get_ticks() - start_time) // 1000
    cur_time_mins = cur_time // 60
    cur_time_secs = cur_time - cur_time_mins * 60
    if cur_time_secs <= 9:
        cur_time_secs = '0' + str(cur_time_secs)
    pygame.draw.rect(dis, black, (0, 0, 120, 140))
    pygame.draw.rect(dis, black, (140, 0, 120, 145))
    pygame.draw.rect(dis, black, (270, 0, 120, 140))
    timer_text = text_font.render('Время игры:', True, (255, 255, 255))
    points_text = text_font.render('Очки:', True, (255, 255, 255))
    next_figure_text1 = text_font.render('Следующая', True, (255, 255, 255))
    next_figure_text2 = text_font.render('фигура:', True, (255, 255, 255))
    timer = digits_font.render(f"{cur_time_mins}:{cur_time_secs}", True, (255, 255, 255))
    points = digits_font.render(f"{points_counter}", True, (255, 255, 255))
    dis.blit(timer, (5, 70))
    dis.blit(timer_text, (5, 40))
    dis.blit(points_text, (275, 40))
    dis.blit(points, (275, 70))
    dis.blit(next_figure_text1, (140, 2))
    dis.blit(next_figure_text2, (140, 22))
    for y in range(4):
        for x in range(4):
            if next_fig.form[y][x] == 1:
                pygame.draw.rect(dis, next_fig.color, (x * rect_size + 160, y * rect_size + 45, rect_size, rect_size))

def is_game_over(grid, black=(0, 0, 0)):
    for y in range(6):
        if grid[y].count(black) != 16:
            return True

def restart(game_over_font, dis, clock, colors, points_counter, black=(0, 0, 0), rect_size=25, display_width=400, display_height=850):
    game_over_message = game_over_font.render('ИГРА ЗАКОНЧЕНА', True, colors['red'])
    game_over_points = game_over_font.render(f'Ваш счёт: {points_counter}', True, (255, 255, 255))
    restart_font = pygame.font.Font('C:/Users/79611/PycharmProjects/Tetris/fonts/Domino Italic.otf', rect_size)
    restart_message = restart_font.render('Начать заново? Нажмите пробел!', True, random.choice(list(colors.values())))
    while 1:
        pygame.draw.rect(dis, black, (0, 0, display_width, display_height))
        dis.blit(game_over_message, (40, 300))
        dis.blit(game_over_points, (75, 370))
        dis.blit(restart_message, (55, 500))
        pygame.display.flip()
        clock.tick(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    locked_position = {}
                    busy_cells = 0
                    points_counter = 0
                    start_time = pygame.time.get_ticks()
                    return False, locked_position, busy_cells, start_time, points_counter
```
### `game_functions.py`
Файл `game_functions.py` содержит в себе функции, которые определяют логику движения фигур и создание сетки для игрового поля:
   ```python
                    locked_position = {}
                    busy_cells = 0
                    points_counter = 0
                    start_time = pygame.time.get_ticks()
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

def setting_figure(dy, dx, cur_fig, locked_position={}, rect_size=25,):
    if dy == 0 and dx == 0:
        for y in range(4):
            for x in range(4):
                if cur_fig.form[y][x] == 1:
                    locked_position[(cur_fig.x + x * rect_size, cur_fig.y - (3 - y) * rect_size)] = cur_fig.color

    min_y_by_x = [-1, -1, -1, -1]
    for y in range(4):
        for x in range(4):
            if cur_fig.form[y][x] == 1:
                min_y_by_x[x] = y

    for y in range(4):
        for x in range(4):
            if cur_fig.form[y][x] == 1:
                if (cur_fig.x + x * rect_size, ((cur_fig.y + rect_size * (min_y_by_x[x] - 2)) // rect_size) * rect_size) in locked_position.keys():
                    locked_position[(cur_fig.x + x * rect_size, (cur_fig.y // rect_size * rect_size) - (3 - min_y_by_x[x]) * rect_size)] = cur_fig.color
                    for j in range(4):
                        for i in range(4):
                            if cur_fig.form[j][i] == 1:
                                locked_position[(cur_fig.x + i * rect_size, (cur_fig.y // rect_size * rect_size) - (3 - j) * rect_size)] = cur_fig.color
                    break
    return locked_position
```
Кроме того, файл содержит в себе класс фигур. В нём задаются поля, определяющие координаты фигуры, форму фигуры, цвет фигуры и угол её поворота. Также реализован метод для поворота фигуры при нажатии соответствующей клавиши.
   ```python
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
```

____
## *Управление в игре*
В управлении используются 4 клавиши:
+ **ПРОБЕЛ** - поворот фигуры на 90 градусов
+ **СТРЕЛКА ВПРАВО** - движение фигуры вправо
+ **СТРЕЛКА ВЛЕВО** - движение фигуры влево
+ **СТРЕЛКА ВНИЗ** - ускорение падения фигуры

Остальное управление (например, в меню) указывается на экране.

____
## *Установка и запуск*
Запускать игру можно двумя способами:
+ Запуском файла `main.py`
+ С помощью файла `main.exe` (необходимо скачать архив Tetris.rar)

Исполняемый файл `main.exe` скомпилирован с помощью интерфейса пользователя ***auto-py-to-exe*** и библиотеки ***pyinstaller***.

____
## *Скриншоты из игры*

![screen1]()
![screen2]()
![screen3]()