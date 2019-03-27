import pprint
import tempfile
import os


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return 'x: {}, y: {}'.format(self.x, self.y)

    def get_length(self, other):  # Манхетоновское расстояние
        return abs(self.x - other.x) + abs(self.y - other.y)


class Figure:
    def __init__(self, start_point, finish_point):
        self.start_point = start_point
        self.finish_point = finish_point
        # self.fig_name = fig_name -- для создания именнованных фигур
        self.figures_queue = []
        # Поля для связи конвейера с фигурами
        # TODO пока в ручном режиме задую I/O агрегатов, в placement pins заранее известны
        self.in_point = Coordinate(start_point.x + 0, start_point.y - 1)
        self.out_point = Coordinate(start_point.x + 0, start_point.y - 1)

    def create_figure_queue(self):
        delta_x = self.finish_point.x - self.start_point.x
        delta_y = self.finish_point.y - self.start_point.y
        '''
        
        x
        |
        |
        u ----------- f 
        |             |
        |             |
        s ----------- b ----- y
        
        '''
        s = self.start_point
        f = self.finish_point

        b = Coordinate(
            self.finish_point.x,
            self.start_point.y
        )
        u = Coordinate(
            self.start_point.x,
            self.finish_point.y
        )

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

    def get_coordinates(self):
        print(self.start_point)


class Routing:
    class Node:
        def __init__(self, parent, coordinate):  # У узла 2 параметра: имя родителя и координата родителя
            self.parent = parent
            self.coordinate = coordinate
            self.f = 0.0  # Оценочная функция
            self.g = 0.0  # Текущая оценка
            self.h = 0.0  # Эвристическая оценка

        def __eq__(self, other_node):   # Переопределяем встроенный метод "равенство"
            return self.coordinate == other_node.coordinate  # У coordinate уже два поля???

        def generate_children(self, area):  # Открываем потомков
            children = []

            # TODO Рскрытие потомков влияет на работу поиска на графе
            coordinates = [
                Coordinate(self.coordinate.x, self.coordinate.y + 1),
                Coordinate(self.coordinate.x, self.coordinate.y - 1),
                Coordinate(self.coordinate.x + 1, self.coordinate.y),
                Coordinate(self.coordinate.x - 1, self.coordinate.y),
            ]
            for coordinate in coordinates:
                child = self.generate_child(coordinate, area)
                if child:
                    children.append(child)  # Если потомок сущ., добавляем его в список children
            return children

        # Сначала обрабатываются исключения, потом создается объект - потомок
        def generate_child(self, coordinate, area):
            if coordinate.x < 0 or area.height <= coordinate.x:  # Неправильно введена координата
                return None
            if coordinate.y < 0 or area.width <= coordinate.y:
                return None
            if area.get_passability(coordinate) == -1:  # Если координата -- стена
                return None

            return Routing.Node(self, coordinate)  # Тут важный момент: потомок - это родитель и ????

    @staticmethod
    def get_path(area, coordinate_from, coordinate_to):     # Метод в routing

        root = Routing.Node(None, coordinate_from)          # Первый узел (корень)
        root.g = 0.0

        root.h = root.coordinate.get_length(coordinate_to)  # Эвристика -- манхет. расстояние от нуля до термин. ноды
        # TODO root.h = 0 - поиск в ширину
        root.f = root.g + root.h                            # Оценочная функция для корня
        # root.f = root.g
        open_set = list()                                   # OPEN список откуда берутся вершины для раскрытия
        open_set.append(root)
        closed_set = list()                                 # CLOSED - после того как верш. раскрыли она идет сюда

        while open_set:
            open_set.sort(key=lambda node: node.f)         # Сортируем от мен. к бол. по полю "оцен. ф-ия"
            best_node = open_set[0]                        # Первый(самый дешевый) и будет лучшим

            if best_node.coordinate == coordinate_to:      # Если лучшая оказалась терминальной, то возвр. путь
                path = []
                node = best_node
                while node:
                    path.insert(0, node.coordinate)
                    node = node.parent
                return path

            open_set.remove(best_node)
            closed_set.append(best_node)                   # Отправляем его в список закрытых

            children = best_node.generate_children(area)   # Если best оказался не термин., то открываем потомков дальше
            for child in children:
                if child in closed_set:                    # !!! Проверка не было ли такого состояния раньше !!!
                    continue
            # Для потомка находим тек. оценку, эврист. оценку и оценочную функцию
                child.g = best_node.g + area.get_passability(child.coordinate)
                child.h = child.coordinate.get_length(coordinate_to)
                child.f = child.g + child.h

                child_from_open_set = None                 # Инициализируем переменную
                for node_from_open_set in open_set:
                    if node_from_open_set == child:
                        child_from_open_set = node_from_open_set
                        break
                if child_from_open_set:
                    if child_from_open_set.g < child.g:
                        continue
                    open_set.remove(child_from_open_set)

                open_set.append(child)

        return []


class Area:
    def __init__(self):
        self.passabilities = [
            [1,  1,  1],
            [1,  1,  1],
            [1,  1,  1],
        ]
        self.width = len(self.passabilities[0])  # Длина списка (количество столбцов)
        self.height = len(self.passabilities)  # Количество строчек на карте

    def draw_map(self, height, width):
        self.passabilities = [[0 for j in range(width)] for i in range(height)]  # Заполнение нулями матрицы-карты
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

    # TODO Пока принимает начальную и конечную точку. Походу ругается на Routing.get_path, т.к. /
    # TODO это статический метод другого класса

    def conveyor_adding(self, coordinate_from, coordinate_to):
        path = Routing.get_path(area, coordinate_from, coordinate_to)
        print(len(path))

        # Добавление происходит поэлементной проходкой по Area
        for _ in range(len(path)):
            buf = path.pop()
            self.passabilities[buf.x][buf.y] = -2
        # print(list_of_walls)
        return self.passabilities

    '''
    def to_string_figure(self, coordinate_corner, dimension):
        result = ''
        coordinate = Coordinate(0, 0)
        for passabilities_row in self.passabilities:  # passability_row - это список-строчка
            if result:
                result += '\n'
            for passability in passabilities_row:
                if coordinate_corner == coordinate:
                    result += '  #'
    '''


def coordinates_checker(start_point, finish_point):
    if start_point.x <= finish_point.x and start_point.y <= finish_point.y:
        return True
    return False


area = Area()
area.draw_map(25, 40)
a = []

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


# Запускаем конвейер. Количество конвейеров в функции range
with open('input.txt', 'r') as f:
    for _ in range(1):
        coord = list(map(int, f.readline().split()))
        if coordinates_checker(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3])):
            figure = Figure(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3]))
            # TODO Ущербность эвритики при 14 -> 15
            a = area.conveyor_adding(Coordinate(4, 1), Coordinate(21, 21))
        else:
            print('Finish point cannot be upper than start point')

storage_path = os.path.join(tempfile.gettempdir(), 'map.txt')


a.reverse()
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
    

print(os.path.dirname(storage_path))
# Another try