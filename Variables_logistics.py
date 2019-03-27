from Technomax.Placement_Routing import Figure, Coordinate, Area, coordinates_checker
from Technomax.Sequence_Pair_Testing import Calculate
import os
import tempfile


def start():
    area = Area()
    area.draw_map(25, 40)
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
    a = area.figure_adding(figures[0])
    a = area.figure_adding(figures[1])
    a = area.figure_adding(figures[2])
    a = area.figure_adding(figures[3])
    '''for figure in figures:
        print('Enter start and finish point of figure: ')
        # coord = list(map(int, input().split()))
        a = area.figure_adding(figure)'''

    # Запускаем конвейер. Количество конвейеров в функции range
    with open('input.txt', 'r') as f:
        for _ in range(0):
            coord = list(map(int, f.readline().split()))
            if coordinates_checker(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3])):
                figure = Figure(Coordinate(coord[0], coord[1]), Coordinate(coord[2], coord[3]))
                # TODO Ущербность эвритики при 14 -> 15
                a = area.conveyor_adding(Coordinate(4, 1), Coordinate(21, 21))
            else:
                print('Finish point cannot be upper than start point')

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

    print(os.path.dirname(storage_path))
