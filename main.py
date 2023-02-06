import pygame
from random import choice
#МАКСИИИИИИМ, ТЕПЕРЬ СДЛЕлай поворт фигур и сжигание, поворт через клавишу вверх. Чтобы это реалезховать проще, сделай, если нажали на кнопку, то фигура меняется на следующую из списка


figures = [ [['ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo'],
                 ['ooooo',
                  'oxooo',
                  'oxxoo',
                  'ooxoo'
                  'ooooo']],
           [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo'],
                 ['ooooo',
                  'oooxo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo']],
           [['ooooo',
                  'oxooo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxxo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'oxxoo',
                  'ooooo']],
           [['ooooo',
                  'oooxo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'oxxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo']],
           [['ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'xxxxo',
                  'ooooo',
                  'ooooo']],
           [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'oxxoo',
                  'ooooo']],
           [['ooooo',
                  'ooxoo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'ooxoo',
                  'ooooo']]]

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),(0, 255, 255), (255, 0, 255), (255, 255, 0)]
figure_list = [] # Список координат и цвета фигур, которые уже упал, НАДО СДЕЛАТЬ СЛОВАРЬ, типа: {(0, 0): '1' или '0'}, чтобы потом пройтись по нему через range и сжигать ряды
list_coords_figure = []


class Tetris:
    def __init__(self, width, height, size_square=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

    def render_cup(self, screen): # Рисуем стакан, в дальнейшем надо будет удалить внутр. квадраты, но пока не надо, т.к. так удобнее
#        pygame.draw.rect(screen, pygame.Color(255, 255, 255), (self.left, self.top, self.size_square * 10, self.size_square * 20), 2)
        for j in range(self.height):
            y1 = j * self.size_square + self.top
            y2 = self.size_square
            for i in range(self.width):
                x1 = i * self.size_square + self.left
                x2 = self.size_square
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (x1, y1, x2, y2), 1)

    def set_view(self, left, top, size_square):
        self.left = left
        self.top = top
        self.size_square = size_square

    def render_figures(self, list_coords, size, screen): # Отрисовка упавших фигур
        for i in list_coords:
            pygame.draw.rect(screen, i[-1], (self.left + i[0] * size, self.top + i[1] * size, size, size))

    def view_figure(self):
        return [choice(figures)[0], choice(colors)] # возвращает рандомную фигуру и цвет

    def render_figure_falling(self, data_figure, screen, pos_x, pos_y, size, flag=False): # отрисовка падающей фигуры
        count_y = 0
        for i in data_figure[0]:
            count_x = 0
            for j in i:
                if j == 'x':
                    pygame.draw.rect(screen, data_figure[1],
                                     (pos_x + count_x * size, pos_y + size * count_y, size, size))
                    if flag: # Если True, то значит фигура упала и записывается в figure_list, PS: строка 122
                        xy = self.get_cell((pos_x + count_x * size + 20, pos_y + size * count_y + 20))
                        figure_list.append([xy[0], xy[1], data_figure[1]])
                        list_coords_figure.append(xy)
                count_x += 1
            count_y += 1

    def examination_bottom_coords(self, data_figure, pos_x, pos_y, size): # Ф-я проверяет, упал ли хотя бы 1  блок фигуры, на блоки другой фигуры
        count_y = 0
        list_coords_falling_figure = [] # Список координат падающей фигуры
        for i in data_figure[0]:
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

    def coords_bottom_square(self, figure): # Выводит  лдину фигуры от начала ее отрисовки до самого нижнего блока(нужна для расчета, упала ли фигура на стакан)
        max_y_x = 0
        for i in range(len(figure[0])):
            for j in figure[0][i]:
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


def main():
    pygame.init()
    size = 750, 850
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Тетрис')
    tetris = Tetris(10, 20)
    size_square = 30
    tetris.set_view(size[0] // 2 - 5 * size_square, size[1] - 20 * size_square, size_square)

    running = True
    speed = 150 # 150, 90
    fps = 15
    clock = pygame.time.Clock()

    # координаты началаотрисовки падающих фигур
    pos_x_figure = size[0] // 2 - 3 * size_square
    pos_y_figure = size[1] - 23 * size_square

    flag = False # тот самы флаг со строки 155
    figure = tetris.view_figure()
    next_figure = tetris.view_figure()
    max_y_falling_figure = tetris.coords_bottom_square(figure)

    while running:
        if flag: # Если True, значит фигура упала и надо зарегинировать новую и вернуть координаты в прежнее состояние
            tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, flag)
            pos_x_figure = size[0] // 2 - 3 * size_square
            pos_y_figure = size[1] - 23 * size_square
            figure = next_figure
            next_figure = tetris.view_figure()
            max_y_falling_figure = tetris.coords_bottom_square(figure)
            flag = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:  # движение фигуры влево и вправо
                if event.key == pygame.K_RIGHT and tetris.examination_bottom_coords(figure, pos_x_figure + size_square, # Проверяет, можно ли фигуре переметится впарво
                                                                                    pos_y_figure, size_square):
                    pos_x_figure += size_square

                elif event.key == pygame.K_LEFT and tetris.examination_bottom_coords(figure,
                                                                                     pos_x_figure - size_square,
                                                                                     pos_y_figure, size_square): # Проверяет, можно ли фигуре переметится
                    pos_x_figure -= size_square
                elif event.key == pygame.K_UP:  # Поворот фигуры
                    pass

        screen.fill((0, 0, 0))
        # отрисовка:
        tetris.render_cup(screen)
        tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, flag)
        tetris.render_figures(figure_list, size_square, screen)
        if pos_y_figure + speed / fps <= 850 - max_y_falling_figure and tetris.examination_bottom_coords(figure, # Проверяет упала ли фигура на блок или на стакан
                                                                                                         pos_x_figure,
                                                                                                         pos_y_figure + size_square,
                                                                                                         size_square):
            pos_y_figure += speed / fps
        else: # Фигура упала, значит записываем ее коодинаты в figure_list и регенирируем новую
            tetris.render_figure_falling(figure, screen, pos_x_figure, pos_y_figure, size_square, flag)
            flag = True

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()