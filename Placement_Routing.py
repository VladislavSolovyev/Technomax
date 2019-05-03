import pprint
import tempfile
import os
from Technomax.Routing_A_Star import *


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(x:{}, y:{})'.format(self.x, self.y)

    def get_length(self, other):  # Манхетоновское расстояние
        return abs(self.x - other.x) + abs(self.y - other.y)


class Figure:
    def __init__(self, start_point, finish_point, name):
        self.start_point = start_point
        self.finish_point = finish_point
        self.name = name
        self.figures_queue = []
        # Поля для связи конвейера с фигурами
        # TODO пока в ручном режиме задую I/O агрегатов, в placement pins заранее известны
        self.in_point = Coordinate(start_point.x + 0, start_point.y - 1)
        self.out_point = Coordinate(start_point.x + 0, start_point.y - 1)

    def create_figure_queue(self):
        delta_x = self.finish_point.x - self.start_point.x
        delta_y = self.finish_point.y - self.start_point.y
        '''
        u ----------- f ----- y 
        |             |
        |             |
        s ----------- b
        |
        |
        x
        '''
        s = self.start_point
        f = self.finish_point

        # TODO Далее начинаю создавать тьюплы. Зачем, если есть класс Coordinate? - чтобы сортировать

        iter_x = s.x
        for _ in range(delta_x):
            self.figures_queue.append((iter_x, s.y))
            self.figures_queue.append((iter_x, f.y))
            iter_x += 1

        iter_y = s.y
        for _ in range(delta_y + 1):
            self.figures_queue.append((s.x, iter_y))
            self.figures_queue.append((f.x, iter_y))
            iter_y += 1

        return sorted(self.figures_queue, reverse=True)


class Area:
    def __init__(self):
        self.passabilities = [
            [1,  1,  1],
            [1,  1,  1],
            [1,  1,  1],
        ]
        #self.width = len(self.passabilities[0])  # Длина списка (количество столбцов)
        #self.height = len(self.passabilities)  # Количество строчек на карте

    def draw_map(self, width, height):
        self.passabilities = [[1 for j in range(width)] for i in range(height)]  # Заполнение нулями матрицы-карты
        self.height = height
        self.width = width
        return self.passabilities

    def get_passability(self, coordinate):
        return self.passabilities[coordinate.x][coordinate.y]  # Возвращает координату (x,y) точки

    def figure_adding(self, new_figure):
        list_of_figs = new_figure.create_figure_queue()
        # print(list_of_walls)
        # Добавление происходит проходясь по списку тьюплов list_of_figs
        for _ in range(len(list_of_figs)):
            buf = list_of_figs.pop()
            self.passabilities[buf[0]][buf[1]] = -1
        # Добавляем вход/выход агрегатам
        # self.passabilities[new_figure.in_point.x][new_figure.in_point.y] = -3
        # self.passabilities[new_figure.out_point.x][new_figure.out_point.y] = -4

        return self.passabilities

    def conveyor_adding(self, coordinate_from, coordinate_to):
        path = Routing.get_path(self, coordinate_from, coordinate_to)
        print("Length of path =", len(path))
        print("Path coordinates:")
        for i in range(len(path)):
            print(path[i], end=' ')


        # Добавление происходит поэлементной проходкой по Area
        if path:
            for _ in range(len(path)):
                buf = path.pop()
                self.passabilities[buf.x][buf.y] = -2
        else:
            print('Path does not exist')


        # print(list_of_walls)
        return self.passabilities


def coordinates_checker(start_point, finish_point):
    if start_point.x <= finish_point.x and start_point.y <= finish_point.y:
        return True
    return False


from Technomax.canvas import *


def _main():
    from Technomax import Brandford_1
    area = Area()
    #area.draw_map(25, 40)
    ar = Brandford_1.get_area()
    area.draw_map(ar[0], ar[1])

    from Technomax.Sequence_Pair_Testing import Calculate
    figures = Calculate.figures_SP()

    '''
    # Запускаем фигуры на площадку
    with open('input.txt', 'r') as f:
        # TODO добавляю фигуры меня значение range()
        for _ in range(1):
            print('Enter start and finish point of figure: ')
            # coord = list(map(int, input().split()))
            coord = list(map(int, f.readline().split()))
            if coordinates_checker(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3])):
                figure = Figure(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3]))
                a = area.figure_adding(figure)
            else:
                print('Finish point cannot be upper than start point')
    '''


    #a = area.figure_adding(figures[1])
    #a = area.figure_adding(figures[2])
    #a = area.figure_adding(figures[3])
    # TODO Индекс здесь не совпадает с индексом словаря. Сделать keys стрингами
    #a = area.figure_adding(figures[6])
    #a = area.figure_adding(figures[7])
    for i in range(len(figures)):
        a = area.figure_adding(figures[i])

    #a = area.conveyor_adding(Coordinate(2, 3), Coordinate(14, 9))

    # TODO сделать костыль в виде проверки координаты to и from. Циклит при не той координате to
    a = area.conveyor_adding(Coordinate(27, 2), Coordinate(1, 2))
    a = area.conveyor_adding(Coordinate(0, 8), Coordinate(7, 8))
    #a = area.conveyor_adding(Coordinate(0, 3), Coordinate(17, 28))

    #a = area.conveyor_adding(Coordinate(4, 1), Coordinate(9, 5))

    # Запускаем конвейер. Количество конвейеров в функции range
    '''for _ in range(0):
        coord = list(map(int, f.readline().split()))
        if coordinates_checker(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3])):
            figure = Figure(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3]))
            # TODO Ущербность эвритики при 14 -> 15
            a = area.conveyor_adding(Coordinate(4, 1), Coordinate(21, 21))
        else:
            print('Finish point cannot be upper than start point')
    '''
    storage_path = os.path.join(tempfile.gettempdir(), 'map.txt')

    # TODO Reverse is needed to allocate global in left bottom corner because of Sequence Pair
    # a.reverse()

    open(storage_path, 'w').close()

    with open(storage_path, 'w') as f:
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j] == -1:
                    f.write(' *')
                    # f.write('{}'.format(a[i][j]))
                    # print('{}'.format(a[i][j]), end=' ')
                elif a[i][j] == -2:
                    f.write(' #')
                elif a[i][j] == -3:
                    f.write(' S')
                elif a[i][j] == -4:
                    f.write(' T')
                else:
                    f.write(' {}'.format(a[i][j]))
                    # print(' {}'.format(a[i][j]), end=' ')
            f.write('\n')

    print(end='\n')
    print(os.path.dirname(storage_path))
    Draw.window(ar, figures, a)


if __name__ == "__main__":
    _main()
