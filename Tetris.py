import sys
import os
import pygame
from random import choice

figures = [[['ooo',
             '0xx',
             'xxo'],
            ['oxo',
             'oxx',
             'oox']],
           [['ooo',
             'xxo',
             'oxx'],
            ['oox',
             'oxx',
             'oxo']],
           [['ooo',
             'xxx',
             'xoo'],
            ['oxo',
             'oxo',
             'oxx'],
            ['oox',
             'xxx',
             'ooo'],
            ['xxo',
             'oxo',
             'oxo']],
           [['ooo',
             'xxx',
             'oox'],
            ['oxx',
             'oxo',
             'oxo'],
            ['xoo',
             'xxx'],
            ['oxo',
             'oxo',
             'xxo']],
           [['ooxo',
             'ooxo',
             'ooxo',
             'ooxo'],
            ['oooo',
             'xxxx',
             'oooo',
             'oooo']],
           [['oooo',
             'oxxo',
             'oxxo',
             'oooo']],
           [['ooo',
             'xxx',
             'oxo'],
            ['oxo',
             'oxx',
             'oxo'],
            ['oxo',
             'xxx'],
            ['oxo',
             'xxo',
             'oxo']]]

colors = [(255, 36, 0), (80, 200, 120), (139, 0, 255), (45, 100, 100), (8, 37, 103), (255, 153, 0), (66, 170, 255)]
figurs_from_color = {
    (255, 36, 0): 1,
    (80, 200, 120): 0,
    (139, 0, 255): 6,
    (45, 100, 100): 5,
    (8, 37, 103): 3,
    (255, 153, 0): 2,
    (66, 170, 255): 4,
    0: (80, 200, 120),
    1: (255, 36, 0),
    2: (255, 153, 0),
    3: (8, 37, 103),
    4: (66, 170, 255),
    5: (45, 100, 100),
    6: (139, 0, 255)
}
name_from_figur = {
    0: 'змея_вправо.png',
    1: 'змея_влево.png',
    2: 'рука_вправо.png',
    3: 'рука_влево.png',
    4: 'палка.png',
    5: 'квадрат.png',
    6: 'затычка.png'
}
speed_per_level = {
    0: 0.7,
    1: 0.5,
    2: 0.356,
    3: 0.1734,
    4: 0.1,
    5: 0.054
}
figure_list = [] # Список координат и цвета фигур, которые уже упал, НАДО СДЕЛАТЬ СЛОВАРЬ, типа: {(0, 0): '1' или '0'}, чтобы потом пройтись по нему через range и сжигать ряды
list_coords_figure = []
value_score = {
    0: 0,
    1: 100,
    2: 300,
    3: 700,
    4: 1500
}
fon_sprite = pygame.sprite.Group()
hold_sprite = pygame.sprite.Group()
next_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tetris:
    def __init__(self, width, height, size_square=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

    def render_cup(self, screen): # Рисуем стакан, в дальнейшем надо будет удалить внутр. квадраты, но пока не надо, т.к. так удобнее
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), (self.left, self.top, self.size_square * 10, self.size_square * 20), 2)
#        for j in range(self.height):
#            y1 = j * self.size_square + self.top
#            y2 = self.size_square
#            for i in range(self.width):
#                x1 = i * self.size_square + self.left
#                x2 = self.size_square
#                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (x1, y1, x2, y2), 1)

    def set_view(self, left, top, size_square):
        self.left = left
        self.top = top
        self.size_square = size_square

    def render_figures(self, list_coords, size, screen): # Отрисовка упавших фигур
        for i in list_coords:
            pygame.draw.rect(screen, i[-1], (self.left + i[0] * size, self.top + i[1] * size, size, size))

    def view_figure(self):
        a = choice(colors)
        return [figures[figurs_from_color[a]], a] # возвращает рандомную фигуру и цвет

    def render_figure_falling(self, data_figure, screen, pos_x, pos_y, size, figut_ver, flag=False): # отрисовка падающей фигуры
        count_y = 0
        for i in data_figure[0][figut_ver]:
            count_x = 0
            for j in i:
                if j == 'x':
                    pygame.draw.rect(screen, data_figure[1],
                                     (pos_x + count_x * size, pos_y + size * count_y, size, size))
                    if flag: # Если True, то значит фигура упала и записывается в figure_list,
                        xy = self.get_cell((pos_x + count_x * size + 20, pos_y + size * count_y + 20))
                        figure_list.append([xy[0], xy[1], data_figure[1]])
                        list_coords_figure.append(xy)
                count_x += 1
            count_y += 1

    def examination_bottom_coords(self, data_figure, pos_x, pos_y, size, figur_ver): # Ф-я проверяет, упал ли хотя бы 1  блок фигуры, на блоки другой фигуры
        count_y = 0
        list_coords_falling_figure = [] # Список координат падающей фигуры
        for i in data_figure[0][figur_ver]:
            count_x = 0
            for j in i:
                if j == 'x':
                    list_coords_falling_figure.append(self.get_cell((pos_x + count_x * size, pos_y + size * count_y)))
                count_x += 1
            count_y += 1

        for i in list_coords_falling_figure:
            if i in list_coords_figure or i == 0:
                return False
        return True

    def coords_bottom_square(self, figure, figur_ver): # Выводит  лдину фигуры от начала ее отрисовки до самого нижнего блока(нужна для расчета, упала ли фигура на стакан)
        max_y_x = 0
        for i in range(len(figure[0][figur_ver])):
            for j in figure[0][figur_ver][i]:
                if j == 'x' and (i + 1) * 30 > max_y_x:
                    max_y_x = (i + 1) * 30
#                elif j == 'o' and i * 30 > max_y_o:
#                    max_y_o = i * 30
        return max_y_x

    def get_cell(self, mouse_pos): # Выводит координаты падающей каждого блока, падающей фигуры
        cell_x = (mouse_pos[0] - self.left) // self.size_square
        cell_y = (mouse_pos[1] - self.top) // self.size_square
        if cell_x < 0 or cell_x > 9: # Чтобы за стакан не выходил
            return 0
        elif cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return int(cell_x), int(cell_y)

    def burn_line(self):
        burning_line = []
        for y in range(19, -1, -1):
            line_collection = []
            line_full = False
            for x in range(10):
                for i in figure_list:
                    if y == i[1] and x == i[0]:
                        line_collection.append(x)
            if len(line_collection) == 10:
                line_full = True
            if line_full:
                burning_line.append(y)
        kolv_burn_line = len(burning_line)
        need_remove = []
        if bool(burning_line):
            for line in burning_line:
                for i in figure_list:
                    if i[1] == line:
                        need_remove.append(i)
        if bool(need_remove):
            bottom_line = 0
            for i in need_remove:
                figure_list.remove(i)
                list_coords_figure.remove((i[0], i[1]))
                if i[1] > bottom_line:
                    bottom_line = i[1]
            for i in range(len(figure_list) - 1, -1, -1):
                a = figure_list.pop(i)
                if a[1] < bottom_line:
                    b = [a[0], a[1] + kolv_burn_line, a[2]]
                else:
                    b = [a[0], a[1], a[2]]
                figure_list.append(b)
                a = list_coords_figure.pop(i)
                if a[1] < bottom_line:
                    b = (a[0], a[1] + kolv_burn_line)
                else:
                    b = (a[0], a[1])
                list_coords_figure.append(b)
        return kolv_burn_line #возвращает кол-во сожжёных линий для подсчёта очков

    def draw_interface(self, screen, size_screen, size_square, inp_score, inp_timer, inp_level):
        color = (255, 255, 255)
        font = pygame.font.Font(None, 40)

        coords_score_xy = size_screen[0] // 2 - 10 * size_square, size_screen[1] - 14.5 * size_square
        coords_score_wh = size_screen[0] // 2 - 7 * size_square, size_screen[1] - 24 * size_square
        pygame.draw.rect(screen, color, (coords_score_xy, coords_score_wh), 1)
        text_score = font.render('Score', True, color)
        text_score_xy = size_screen[0] // 2 - 9 * size_square, size_screen[1] - 14.5 * size_square
        screen.blit(text_score, text_score_xy)
        score = font.render(str(inp_score), True, color)
        score_xy = size_screen[0] // 2 - 7.7 * size_square - score.get_width() // 2, size_screen[1] - 13.5 * size_square
        screen.blit(score, score_xy)

        coords_timer_xy = size_screen[0] // 2 - 10 * size_square, size_screen[1] - 11.5 * size_square
        coords_timer_wh = size_screen[0] // 2 - 7 * size_square, size_screen[1] - 24 * size_square
        pygame.draw.rect(screen, color, (coords_timer_xy, coords_timer_wh), 1)
        text_timer = font.render('Timer', True, color)
        text_timer_xy = size_screen[0] // 2 - 9 * size_square, size_screen[1] - 11.5 * size_square
        screen.blit(text_timer, text_timer_xy)
        timer = font.render(str(inp_timer), True, color)
        timer_xy = size_screen[0] // 2 - 7.7 * size_square - timer.get_width() // 2, size_screen[1] - 10.5 * size_square
        screen.blit(timer, timer_xy)

        coords_hold_xy = size_screen[0] // 2 - 10 * size_square, size_screen[1] - 20 * size_square
        coords_hold_wh = size_screen[0] // 2 - 7 * size_square, size_screen[1] - 22 * size_square
        pygame.draw.rect(screen, color, (coords_hold_xy, coords_hold_wh), 1)
        text_hold = font.render('Hold', True, color)
        text_hold_x = size_screen[0] // 2 - 8.7 * size_square
        text_hold_y = size_screen[1] - 20 * size_square
        screen.blit(text_hold, (text_hold_x, text_hold_y))

        coords_next_xy = size_screen[0] - 6.3 * size_square, size_screen[1] - 20 * size_square
        coords_next_wh = size_screen[0] - 18.7 * size_square, size_screen[1] - 22 * size_square
        pygame.draw.rect(screen, color, (coords_next_xy, coords_next_wh), 1)
        text_next = font.render('Next', True, color)
        text_next_x = size_screen[0] - 5 * size_square
        text_next_y = size_screen[1] - 20 * size_square
        screen.blit(text_next, (text_next_x, text_next_y))

        coords_level_xy = size_screen[0] - 6.3 * size_square, size_screen[1] - 14.5 * size_square
        coords_level_wh = size_screen[0] // 2 - 7 * size_square, size_screen[1] - 24 * size_square
        pygame.draw.rect(screen, color, (coords_level_xy, coords_level_wh), 1)
        text_level = font.render('Level', True, color)
        text_level_x = size_screen[0] - 5.2 * size_square
        text_level_y = size_screen[1] - 14.5 * size_square
        screen.blit(text_level, (text_level_x, text_level_y))
        level = font.render(str(inp_level), True, color)
        level_xy = size_screen[0] - 4.2 * size_square, size_screen[1] - 13.3 * size_square
        screen.blit(level, level_xy)

    def end_game(self, screen):
        pause = pygame.Surface((700, 800), pygame.SRCALPHA)
        pause.fill((70, 255, 255, 127))
        screen.blit(pause, (0, 0))


class Tetris_picture(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(fon_sprite)
        self.image = load_image('фон.jpg')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 0
        self.rect.y = 0


class Start_picture(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(fon_sprite)
        self.image = load_image('start.jpg')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Tetris_figur_on_hold(pygame.sprite.Sprite):
    def __init__(self, size_screen, size_square, name_figur):
        super().__init__(hold_sprite)
        self.image = load_image(name_figur, -1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = size_screen[0] // 2 - 9.4 * size_square
        self.rect.y = size_screen[1] // 2 - 5 * size_square


class Tetris_figur_next(pygame.sprite.Sprite):
    def __init__(self, size_screen, size_square, name_figur):
        super().__init__(next_sprite)
        self.image = load_image(name_figur, -1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = size_screen[0] - 5.6 * size_square
        self.rect.y = size_screen[1] // 2 - 5 * size_square


def main():
    pygame.init()
    size = 700, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Тетрис')
    tetris = Tetris(10, 20)
    size_square = 30
    tetris.set_view(size[0] // 2 - 5 * size_square, size[1] - 20 * size_square, size_square)


    running = True
    #speed = 900 # 150, 90
    #fps = 30
    clock = pygame.time.Clock()
    now_time = 0
    past_time = 0
    timer = '0'
    score = 0
    level = 0

    # координаты начала отрисовки падающих фигур
    pos_x_figure = size[0] // 2 - 2 * size_square
    pos_y_figure = size[1] - 20 * size_square

    flag_start = True
    flag_loss = True
    flag = False # тот самы флаг со строки 155
    figur_ver = 0 # выставляю начальное вариант фигуры

    figure = tetris.view_figure()
    next_figure = tetris.view_figure()
    next_figure_for_sprite = name_from_figur[figures.index(next_figure[0])]
    hold_figur = 0
    hold_figur_for_sprite = -1
    max_y_falling_figure = tetris.coords_bottom_square(figure, figur_ver)

    while running:
        if flag: # Если True, значит фигура упала и надо зарегинировать новую и вернуть координаты в прежнее состояние
            try:
                tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, figur_ver, flag)
            except:
                flag_loss = True

            pos_x_figure = size[0] // 2 - 3 * size_square
            pos_y_figure = size[1] - 23 * size_square
            figur_ver = 0
            figure = next_figure
            next_figure = tetris.view_figure()
            next_figure_for_sprite = name_from_figur[figures.index(next_figure[0])]
            max_y_falling_figure = tetris.coords_bottom_square(figure, figur_ver)
            flag = False

        if flag_loss:
            pos_x_figure = size[0] // 2 - 2 * size_square
            pos_y_figure = size[1] - 20 * size_square
            flag = False
            figur_ver = 0
            hold_figur = 0
            hold_figur_for_sprite = -1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:  # движение фигуры влево и вправо
                if not flag_loss and event.key == pygame.K_RIGHT and tetris.examination_bottom_coords(figure, pos_x_figure + size_square, # Проверяет, можно ли фигуре переметится впарво
                                                                                    pos_y_figure, size_square, figur_ver):
                    pos_x_figure += size_square

                elif not flag_loss and event.key == pygame.K_LEFT and tetris.examination_bottom_coords(figure,
                                                                                     pos_x_figure - size_square,
                                                                                     pos_y_figure, size_square, figur_ver): # Проверяет, можно ли фигуре переметится
                    pos_x_figure -= size_square

                elif not flag_loss and event.key == pygame.K_UP:  # Поворот фигуры
                    if figur_ver != len(figure[0]) - 1:
                        tm_figur_ver = figur_ver + 1
                    else:
                        tm_figur_ver = 0
                    if tetris.examination_bottom_coords(figure, pos_x_figure, pos_y_figure, size_square, tm_figur_ver):
                        if figur_ver != len(figure[0]) - 1:
                            figur_ver += 1
                        else:
                            figur_ver = 0
                        max_y_falling_figure = tetris.coords_bottom_square(figure, figur_ver)

                elif not flag_loss and event.key == pygame.K_DOWN and pos_y_figure + size_square <= size[1] - max_y_falling_figure\
                        and tetris.examination_bottom_coords(figure, pos_x_figure, pos_y_figure + size_square,
                                                             size_square, figur_ver):
                    past_time = now_time
                    pos_y_figure += size_square

                elif not flag_loss and event.key == pygame.K_RSHIFT:
                    ok = True
                    while ok:
                        if pos_y_figure + size_square <= size[1] - max_y_falling_figure and tetris.examination_bottom_coords(figure,
                                                                                                        # Проверяет упала ли фигура на блок или на стакан
                                                                                                        pos_x_figure,
                                                                                                        pos_y_figure + size_square,
                                                                                                        size_square,
                                                                                                        figur_ver):
                            pos_y_figure += size_square
                        else:
                            ok = False

                elif event.key == pygame.K_SPACE:
                    if hold_figur_for_sprite != -1 and not flag_loss:
                        tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, figur_ver,
                                                     flag)
                        pos_x_figure = size[0] // 2 - 3 * size_square
                        pos_y_figure = size[1] - 23 * size_square
                        figur_ver = 0
                        figure, hold_figur = hold_figur, figure
                        max_y_falling_figure = tetris.coords_bottom_square(figure, figur_ver)
                        hold_figur_for_sprite = name_from_figur[figures.index(hold_figur[0])]
                    elif not flag_loss:
                        tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, figur_ver,
                                                     flag)
                        pos_x_figure = size[0] // 2 - 3 * size_square
                        pos_y_figure = size[1] - 23 * size_square
                        figur_ver = 0
                        hold_figur = figure
                        figure = next_figure
                        next_figure = tetris.view_figure()
                        max_y_falling_figure = tetris.coords_bottom_square(figure, figur_ver)
                        hold_figur_for_sprite = name_from_figur[figures.index(hold_figur[0])]
                        next_figure_for_sprite = name_from_figur[figures.index(next_figure[0])]
                    flag_start = False

                    if flag_loss:
                        figure = tetris.view_figure()
                        next_figure = tetris.view_figure()
                        next_figure_for_sprite = name_from_figur[figures.index(next_figure[0])]
                        max_y_falling_figure = tetris.coords_bottom_square(figure, figur_ver)
                        for i in hold_sprite:
                            i.kill()
                        level = 0
                        score = 0
                        now_time = 0
                        past_time = 0
                        figure_list.clear()
                        list_coords_figure.clear()
                        flag_loss = False


        screen.fill((0, 0, 0))
        # отрисовка:
        if flag_start:
            Start_picture()

            fon_sprite.draw(screen)
        if flag_loss and not flag_start:
            font = pygame.font.Font(None, 90)
            font_1 = pygame.font.Font(None, 60)
            text_loss = font.render("Поражение!", True, (250, 25, 15))
            text_loss_2 = font_1.render("Играть занаво: Пробел", True, (250, 25, 15))
            x = size[0] // 2 - text_loss.get_width() // 2
            y, y2 = size[1] // 8 - text_loss.get_height() // 2, size[1] // 5 - text_loss.get_height() // 2
            screen.blit(text_loss_2, (x - 50, y2))
            screen.blit(text_loss, (x, y))

        if not flag_start:
            tetris.render_cup(screen)
            tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, figur_ver, flag)
            tetris.render_figures(figure_list, size_square, screen)
            q = tetris.burn_line()
            score += value_score[q] * level # начисление очков за сжжигание линий. Стоит не возле начисления очков за фигуры т.к. там q успевает измениться
            now_time += clock.tick() / 1000
            if not flag_loss:
                timer = str(now_time).split('.')[0]

            if hold_figur_for_sprite != -1:
                for o in hold_sprite:
                    o.kill()
                Tetris_figur_on_hold(size, size_square, hold_figur_for_sprite)
                for i in next_sprite:
                    i.kill()
                Tetris_figur_next(size, size_square, next_figure_for_sprite)
            else:
                for i in next_sprite:
                    i.kill()
                Tetris_figur_next(size, size_square, next_figure_for_sprite)
            hold_sprite.draw(screen)
            next_sprite.draw(screen)

            if now_time - past_time >= speed_per_level[level] and not flag_loss:
                past_time = now_time
                if pos_y_figure + size_square <= size[1] - max_y_falling_figure and tetris.examination_bottom_coords(figure,
                                                                                                            # Проверяет упала ли фигура на блок или на стакан
                                                                                                            pos_x_figure,
                                                                                                            pos_y_figure + size_square,
                                                                                                            size_square,
                                                                                                            figur_ver):
                    pos_y_figure += size_square
                else:  # Фигура упала, значит записываем ее коодинаты в figure_list и регенирируем новую
                    tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, figur_ver, flag)
                    flag = True
                    score += 5 * (pos_y_figure // 30 - 6)  # начисление очков за постановление фигуры. Начисляет слегка некоректно т.к. pos_y_figur стоит на центре фигур или я не знаю
            if level == 4 and score > 58000:
                level = 5
            if level == 3 and score > 26000:
                level = 4
            if level == 2 and score > 10000:
                level = 3
            elif level == 1 and score > 4000:
                level = 2
            elif level == 0 and score > 1500:
                level = 1
            tetris.draw_interface(screen, size, size_square, score, timer, level)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()