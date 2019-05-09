from Technomax.Routing_A_Star import Coordinate

g_lambda = 350
gr = g_lambda * 5
# АХПП
width1 = 31600//gr + 1
height1 = 1700//gr + 1
# 2_Печь
width2 = 21320//gr + 1
height2 = 8660//gr + 1
# 3_Печь
width3 = 4820//gr + 1
height3 = 24320//gr +1
# 4_Кабина
width4 = 5000 // gr + 1
height4 = 5000//gr + 1
# 5_Зона Загрузки
width5 = 15000//gr + 1
height5 = 2
# 6_Зона Выгрузки
width6 = 15000//gr + 1
height6 = 2
# 7_Курилка
width7 = 1000//gr + 1
height7 = 1000//gr + 1
# 8_Паркет
width8 = 1000//gr + 1
height8 = 1000//gr + 1

area = (700000//gr, 500000//gr)


wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(0, 0), Coordinate(height1 - 1, width1 + 1), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(0, 0), Coordinate(height2 - 1, width2 + 1), '3_Печь_2'],
    3: [height3, width3, '3_Печь_2', Coordinate(0, 0), Coordinate(0, 0), '4_Кабина'],
    4: [height4, width4, '4_Кабина', Coordinate(0, 0), Coordinate(0, 0), '5_Зона Загрузки'],
    5: [height5, width5, '5_Зона Загрузки', Coordinate(0, 0), Coordinate(0, 0), '6_Зона Выгрузки'],
    6: [height6, width6, '6_Зона Выгрузки', Coordinate(0, 0), Coordinate(0, 0), '7_Курилка'],
    7: [height7, width7, '7_Курилка', Coordinate(0, 0), Coordinate(0, 0), '8_Паркет'],
    8: [height8, width8, '8_Паркет', Coordinate(0, 0), Coordinate(0, 0), '1_АХПП'],
}

X = [1, 7, 4, 5, 2, 6, 3, 8]
Y = [8, 4, 7, 2, 5, 3, 6, 1]

def get_sequences():
    return X, Y

def get_area():
    return area

def get_wid_hei_dict():
    return wid_hei_dict
