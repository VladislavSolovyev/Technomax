from Technomax.Placement_Routing import *


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
                Coordinate(self.coordinate.x + 1, self.coordinate.y),
                Coordinate(self.coordinate.x - 1, self.coordinate.y),
                Coordinate(self.coordinate.x, self.coordinate.y + 1),
                Coordinate(self.coordinate.x, self.coordinate.y - 1),

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

