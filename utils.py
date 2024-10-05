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