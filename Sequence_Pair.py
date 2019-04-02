from Technomax.Placement_Routing import Figure, Coordinate, Area
import random
import math
import copy

# TODO Файлик для теста разных SP, протестированы с телеги и Вонговский

class SeqPair:

    def __init__(self, X, Y, wid_hei_dict):
        self.X = X
        self.Y = Y
        self.wid_hei_dict = wid_hei_dict


    def find_SP_coordinates(self):
        """
                 LCS of              LCS of
        block | (X1; Y1) | x_coor | (XR2 ; Y1) | y_coor

        """
        '''Block position array P[b]; b = 1...n is used to record the x or
        y coordinate of block b depending on the weight w(b) equals
        to the width or height of block b respectively.'''
        P = [0 for _ in range(len(self.X))]

        '''
        To record the indices in both X and Y for each block b, the array match[b]; 
        b = 1...n is constructed to be:
            if b = X[i] = Y [j]: 
                match[b].x = i and match[b].y = j
        '''

        # Далее пусть будет статическим методом

        class ForMatching:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        match = ForMatching({}, {})

        for i in range(len(self.X)):
            for j in range(len(self.X)):
                if self.X[i] == self.Y[j]:
                    # ключ - Название фигуры, значение - индекс в последовательности
                    # в match попадают когда сошлись фигуры в одном списке и другом
                    match.x.update({self.X[i]: i})
                    match.y.update({self.Y[j]: j})

        '''
        The length array L[1...n] is used to record the length of candidates of the 
        longest common subsequence.
        '''
        L = [0 for _ in range(len(self.X))]

        # ALGORITHM for x coordinate:
        for i in range(len(self.X)):
            b = self.X[i]
            p = match.y[b]
            P[b - 1] = L[p]
            tmp = P[b - 1] + self.wid_hei_dict[b][0]
            for j in range(p, len(self.X)):
                if tmp > L[j]:
                    L[j] = tmp
                else:
                    break
        x_SP_coordinates = P
        #print(x_SP_coordinates)

        # ALGORITHM for y coordinate:
        P = [0 for _ in range(len(self.X))]
        match = ForMatching({}, {})

        XR = self.X[:]
        XR.reverse()
        for i in range(len(self.X)):
            for j in range(len(self.X)):
                if XR[i] == self.Y[j]:
                    match.x.update({XR[i]: i})
                    match.y.update({self.Y[j]: j})
        L = [0 for _ in range(len(self.X))]
        for i in range(len(self.X)):
            b = XR[i]
            p = match.y[b]
            P[b - 1] = L[p]
            tmp = P[b - 1] + self.wid_hei_dict[b][1]
            for j in range(p, len(self.X)):
                if tmp > L[j]:
                    L[j] = tmp
                else:
                    break

        y_SP_coordinates = P
        #print(y_SP_coordinates)

        return [x_SP_coordinates, y_SP_coordinates]

    def find_SP_coordinates_nlogn(self):
        pass


X = [4, 3, 1, 6, 2, 5]
Y = [6, 3, 5, 4, 1, 2]
XR = X[:]
XR.reverse()

wid_hei_dict = {
    1: (4, 6),
    2: (3, 7),
    3: (3, 3),
    4: (2, 3),
    5: (4, 3),
    6: (6, 4),
}

test_seq_pair = SeqPair(X, Y, wid_hei_dict)


print(test_seq_pair.find_SP_coordinates()[0])
print()
print("Координаты стартовых точек: ",
    list(
        zip(
            test_seq_pair.find_SP_coordinates()[0],
            test_seq_pair.find_SP_coordinates()[1]
        )
    )
)

'''
# На четырехстаx тыс. операций думает 25 секунд
for _ in range(400000):
    a = test_seq_pair.find_SP_coordinates()[0]
    # list(zip(test_seq_pair.find_SP_coordinates()[0], test_seq_pair.find_SP_coordinates()[1]))
'''

'''
# На четырехстаx миллионах операций думает 30 секунд
for _ in range(400000000):
    a = 8
'''
