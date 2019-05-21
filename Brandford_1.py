from Technomax.Routing_A_Star import Coordinate

# g_lambda = 350
g_lambda = 350
gr = g_lambda * 5
# АХПП
width1 = 31600//gr + 1
height1 = 1700//gr + 1
# 2_Печь
width2 = 21320//gr + 1
height2 = 8660//gr + 1
# 3_Печь
width3 = 24320//gr + 1
height3 = 4820//gr +1
# 4_Кабина
width4 = 5000 // gr + 1
height4 = 5000//gr + 1
# 5_Зона Загрузки/Выгрузки
width5 = 10000//gr + 1
height5 = 2

area = (700000//gr, 500000//gr)


wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(0, 0), Coordinate(height1 - 1, width1 + 1), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(0, 0), Coordinate(height2 - 1, width2 + 1), '3_Печь_2'],
    3: [height3, width3, '3_Печь_2', Coordinate(0, 0), Coordinate(height3 - 1, width3 + 1), '4_Кабина'],
    4: [height4, width4, '4_Кабина', Coordinate(0, 0), Coordinate(height4 - 1, width4 + 1), '5_Зона Загрузки/Выгрузки'],
    5: [height5, width5, '5_Зона Загрузки/Выгрузки', Coordinate(0, 0), Coordinate(0, width5 + 1), '6_Зона Загрузки/Выгрузки_2'],
    6: [height5, width5, '6_Зона Загрузки/Выгрузки_2',Coordinate(0, 0), Coordinate(0, width5 + 1), '1_АХПП'],
}
X = [1, 3, 4, 5, 2, 6]
Y = [3, 4, 1, 2, 5, 6]


'''
wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(0, 0), Coordinate(height1 - 1, width1 + 1), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(0, 0), Coordinate(height2 - 1, width2 + 1), '3_Печь_2'],
    3: [height3, width3, '3_Печь_2', Coordinate(0, 0), Coordinate(height3 - 1, width3 + 1), '4_Кабина'],
    4: [height4, width4, '4_Кабина', Coordinate(0, 0), Coordinate(height4 - 1, width4 + 1), '1_АХПП'],


}
X = [1, 3, 2, 4]
Y = [3, 1, 2, 4]

'''
'''
wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(0, 0), Coordinate(height1 - 1, width1 + 1), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(0, 0), Coordinate(height2 - 1, width2 + 1), '1_АХПП'],
}
X = [1, 2]
Y = [2, 1]
'''

'''
wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(0, 0), Coordinate(0, 0), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(0, 0), Coordinate(0, 0), '3_Печь_2'],
    3: [height3, width3, '3_Печь_2', Coordinate(0, 0), Coordinate(0, 0), '4_Кабина'],
    4: [height4, width4, '4_Кабина', Coordinate(0, 0), Coordinate(0, 0), '5_Зона Загрузки/Выгрузки'],
    5: [height5, width5, '5_Зона Загрузки/Выгрузки', Coordinate(0, 0), Coordinate(0, 0), '1_АХПП'],
}
X = [1, 3, 4, 5, 2]
Y = [3, 4, 1, 2, 5]
'''
'''
wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(1, 1), Coordinate(1, 1), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(1, 1), Coordinate(1, 1), '3_Печь_2'],
    3: [height3, width3, '3_Печь_2', Coordinate(1, 1), Coordinate(1, 1), '4_Кабина'],
    4: [height4, width4, '4_Кабина', Coordinate(1, 1), Coordinate(1, 1), '5_Зона Загрузки/Выгрузки'],
    5: [height5, width5, '5_Зона Загрузки/Выгрузки', Coordinate(1, 1), Coordinate(1, 1), '1_АХПП'],
}
'''
'''
wid_hei_dict = {
    1: [height1, width1, '1_АХПП', Coordinate(0, 0), Coordinate(1, 1), '2_Печь'],
    2: [height2, width2, '2_Печь', Coordinate(0, 0), Coordinate(height2 - 1, width2 + 1), '3_Печь_2'],
    3: [height3, width3, '3_Печь_2', Coordinate(0, 0), Coordinate(height3 - 1, width3 + 1), '4_Кабина'],
    4: [height4, width4, '4_Кабина', Coordinate(0, 0), Coordinate(1, 1), '5_Зона Загрузки/Выгрузки'],
    5: [height5, width5, '5_Зона Загрузки/Выгрузки', Coordinate(0, 0), Coordinate(1, 1), '1_АХПП'],
}
'''

def get_sequences():
    return X, Y

def get_area():
    return area

def get_wid_hei_dict():
    return wid_hei_dict
