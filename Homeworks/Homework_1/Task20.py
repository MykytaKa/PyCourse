# Вариант 20
# Дана целочисленная прямоугольная матрица.
# Определить:
# 1)   количество отрицательных элементов в тех строках, которые содержат хотя бы один нулевой элемент;
# 2)   номера строк и столбцов всех седловых точек матрицы.Примечание.
# Матрица А имеет седловую точку Аij, если Аij является минимальным элементом в i-й строке и максимальным в j-м столбце
import random

length = 5
height = 8

minValue = -5
maxValue = 5


def create_array():
    tmpmatrix = [0] * length
    for i in range(length):
        tmpmatrix[i] = [0] * height
    return tmpmatrix


def fill_array(tmatrix):
    for row in range(length):
        for col in range(height):
            tmatrix[row][col] = random.randint(minValue, maxValue)
    return tmatrix


def print_array(matrix):
    for row in matrix:
        for col in row:
            print(col, end=' ')
        print()
    print()


def calc_negative_numbers(matrix):
    amount = 0
    is_contain_null = False
    for i in range(length):
        for j in range(height):
            if matrix[i][j] < 0:
                amount += 1
            if matrix[i][j] == 0:
                is_contain_null = True
        if is_contain_null:
            print("Row", i + 1, "has", amount, "negative elements")
        else:
            print("There are no null elements in row", i)
        is_contain_null = False
        amount = 0
    print()


def find_sadle_points(matrix):
    for i in range(length):
        for j in range(height):
            minimal_in_row = matrix[i][j]
            minimal_in_col = matrix[i][j]
            min_row_i = i
            min_row_j = j
            for k in range(height):
                if matrix[i][k] < minimal_in_row:
                    minimal_in_row = matrix[i][k]
                    min_row_j = k
            min_col_i = i
            min_col_j = j
            for m in range(length):
                if matrix[m][j] < minimal_in_col:
                    minimal_in_col = matrix[m][j]
                    min_col_i = m
            if (minimal_in_row == minimal_in_col) and (min_row_i == min_col_i) and (min_row_j == min_col_j):
                print("Element in", i + 1, "row and", j + 1, "column is sadle point")


matrix = create_array()
matrix = fill_array(matrix)
print_array(matrix)
calc_negative_numbers(matrix)
find_sadle_points(matrix)