from Technomax.Placement_Routing import Figure, Coordinate, Area
import random


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


class SimAnnealing:

    def __init__(self, init_temperature, frozen_temperature):
        self.temperature = init_temperature
        self.frozen = frozen_temperature

    # TODO Оказалось это должны быть методы класса, т.к. экземпляр класса для их ф-ала создавать не обязательно
    # TODO Методы при каждом вызове меняют seq_pair глобально
    def m1_perturb(self, seq_pair):
        rand_ind1 = random.randrange(0, len(seq_pair.X))
        rand_ind2 = random.randrange(0, len(seq_pair.X))

        while rand_ind1 == rand_ind2:
            rand_ind2 = random.randrange(0, len(seq_pair.X))
        seq_pair.X[rand_ind1], seq_pair.X[rand_ind2] = seq_pair.X[rand_ind2], seq_pair.X[rand_ind1]

        return seq_pair

    def m2_perturb(self, seq_pair):
        #rand_ind1 = random.randrange(0, len(seq_pair.X))
        rand_ind1 = 1
        #rand_ind2 = random.randrange(0, len(seq_pair.X))
        rand_ind2 = 6
        while rand_ind1 == rand_ind2:
            rand_ind2 = random.randrange(0, len(seq_pair.X))
        seq_pair.X[rand_ind1], seq_pair.X[rand_ind2] = seq_pair.X[rand_ind2], seq_pair.X[rand_ind1]

        ind1 = seq_pair.Y.index(seq_pair.X[rand_ind2])
        ind2 = seq_pair.Y.index(seq_pair.X[rand_ind1])
        seq_pair.Y[ind1], seq_pair.Y[ind2] = seq_pair.Y[ind2], seq_pair.Y[ind1]

        return seq_pair

    def m3_perturb(self, seq_pair):
        rand_ind = random.randrange(0, len(seq_pair.X))
        seq_pair.wid_hei_dict[rand_ind][0], seq_pair.wid_hei_dict[rand_ind][1] = \
            seq_pair.wid_hei_dict[rand_ind][1], seq_pair.wid_hei_dict[rand_ind][0]

        return seq_pair

    #def get_cost(self, ):

"""
### Rules ###
(<...xi..xj... > , < ...xi..xj...>)) x[i] is left to x[j]
(<...xj..xi... > , < ...xi..xj...>)) x[i] is below x[j]

1) if bi is after bj in X and before bj in Y , then bi is before
bj in XR and before bj in Y , and

2) if bi is before bj in XR and before bj in Y , then bi is
after bj in X and before bj in Y
"""


# seq_pair = [[1, 7, 4, 5, 2, 6, 3, 8], [8, 4, 7, 2, 5, 3, 6, 1]]


X = [1, 7, 4, 5, 2, 6, 3, 8]
Y = [8, 4, 7, 2, 5, 3, 6, 1]


wid_hei_dict = {
    1: [2, 4],
    2: [1, 3],
    3: [3, 3],
    4: [3, 5],
    5: [3, 2],
    6: [5, 3],
    7: [1, 2],
    8: [2, 4],
}

area = Area()
area.draw_map(25, 40)
a = []

init_seq_pair = SeqPair(X, Y, wid_hei_dict)

# Экземпляр создается ради perturb методов
sim_ann = SimAnnealing(1000, 2)

# m1_perturb глобально меняет seq_pair
new_p = sim_ann.m2_perturb(init_seq_pair)

x_SP_coordinates = init_seq_pair.find_SP_coordinates()[0]
y_SP_coordinates = init_seq_pair.find_SP_coordinates()[1]


class Calculate:
    @staticmethod
    def figures_SP():
        figures = []
        for i in range(len(init_seq_pair.X)):
            figure = Figure(
                Coordinate(
                    x_SP_coordinates[i],
                    y_SP_coordinates[i]
                ),
                Coordinate(
                    x_SP_coordinates[i] + wid_hei_dict[i + 1][0] - 1,
                    y_SP_coordinates[i] + wid_hei_dict[i + 1][1] - 1
                )
            )
            figures.append(figure)
        return figures
