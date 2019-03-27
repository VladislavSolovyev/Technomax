from Technomax.Placement_Routing import Figure, Coordinate, Area


# TODO Файлик для теста разных SP, протестированы с телеги и Вонговский


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
XR = X[:]
XR.reverse()

wid_hei_dict = {
    1: (2, 4),
    2: (1, 3),
    3: (3, 3),
    4: (3, 5),
    5: (3, 2),
    6: (5, 3),
    7: (1, 2),
    8: (2, 4),
}

"""
         LCS of              LCS of
block | (X1; Y1) | x_coor | (XR2 ; Y1) | y_coor

"""
'''Block position array P[b]; b = 1...n is used to record the x or
y coordinate of block b depending on the weight w(b) equals
to the width or height of block b respectively.'''
P = [0 for _ in range(len(X))]

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

for i in range(len(X)):
    for j in range(len(X)):
        if X[i] == Y[j]:
            match.x.update({X[i]: i})
            match.y.update({Y[j]: j})

'''
The length array L[1...n] is used to record the length of candidates of the 
longest common subsequence.
'''
L = [0 for _ in range(len(X))]

# ALGORITHM for x coordinate:
for i in range(len(X)):
    b = X[i]
    p = match.y[b]
    P[b - 1] = L[p]
    tmp = P[b - 1] + wid_hei_dict[b][0]
    for j in range(p, len(X)):
        if tmp > L[j]:
            L[j] = tmp
        else:
            break
x_SP_coordinates = P
print(x_SP_coordinates)


# ALGORITHM for y coordinate:
P = [0 for _ in range(len(X))]
match = ForMatching({}, {})

for i in range(len(X)):
    for j in range(len(X)):
        if XR[i] == Y[j]:
            match.x.update({XR[i]: i})
            match.y.update({Y[j]: j})
L = [0 for _ in range(len(X))]
for i in range(len(X)):
    b = XR[i]
    p = match.y[b]
    P[b - 1] = L[p]
    tmp = P[b - 1] + wid_hei_dict[b][1]
    for j in range(p, len(X)):
        if tmp > L[j]:
            L[j] = tmp
        else:
            break

y_SP_coordinates = P
print(y_SP_coordinates)

coordinates_for_placement = [x_SP_coordinates, y_SP_coordinates]


area = Area()
area.draw_map(25, 40)
a = []

# TODO Уперся в то, что надо переделать инициализацию фигуры


class Calculate:
    @staticmethod
    def figures_SP():
        figures = []
        for i in range(8):
            figure = Figure(
                Coordinate(
                    x_SP_coordinates[i],
                    y_SP_coordinates[i]
                ),
                Coordinate(
                    x_SP_coordinates[i] + wid_hei_dict[i + 1][1],
                    y_SP_coordinates[i] + wid_hei_dict[i + 1][0]
                )
            )
            figures.append(figure)
        return figures

