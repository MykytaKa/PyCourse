# Вариант 20
# Дана целочисленная прямоугольная матрица.
# Определить:
# 1)   количество отрицательных элементов в тех строках, которые содержат хотя бы один нулевой элемент;
# 2)   номера строк и столбцов всех седловых точек матрицы.Примечание.
# Матрица А имеет седловую точку Аij, если Аij является минимальным элементом в i-й строке и максимальным в j-м столбце
import random

LENGTH = 5
HEIGHT = 8

MINVALUE = -5
MAXVALUE = 5


def create_array():
    return [[element for element in range(HEIGHT)] for _ in range(LENGTH)]


def fill_array(t_matrix):
    for row in range(LENGTH):
        for col in range(HEIGHT):
            t_matrix[row][col] = random.randint(MINVALUE, MAXVALUE)
    return t_matrix


def print_array(matrix):
    matrix_text = ''
    for row in matrix:
        for col in row:
            matrix_text += str(col) + ' '
        matrix_text += '\n'
    print(matrix_text)


def calc_negative_numbers(matrix):
    amount = 0
    is_contain_null = False
    for i in range(LENGTH):
        for j in range(HEIGHT):
            amount += matrix[i][j] < 0
            is_contain_null = matrix[i][j] == 0
        if is_contain_null:
            print(f'Row {i + 1} has {amount} negative elements')
        else:
            print(f'There are no null elements in row {i + 1}')
        is_contain_null = False
        amount = 0
    print('')


def find_sadle_points(matrix):
    for i in range(LENGTH):
        for j in range(HEIGHT):
            minimal_in_row = matrix[i][j]
            minimal_in_col = matrix[i][j]

            min_row_i = i
            min_row_j = j

            for k in range(HEIGHT):
                if matrix[i][k] < minimal_in_row:
                    minimal_in_row = matrix[i][k]
                    min_row_j = k

            min_col_i = i
            min_col_j = j

            for m in range(LENGTH):
                if matrix[m][j] < minimal_in_col:
                    minimal_in_col = matrix[m][j]
                    min_col_i = m

            if (minimal_in_row == minimal_in_col) and (min_row_i == min_col_i) and (min_row_j == min_col_j):
                print(f'Element in {i + 1} row and {j + 1} column is sadle point')


matrix = create_array()
matrix = fill_array(matrix)
print_array(matrix)
calc_negative_numbers(matrix)
find_sadle_points(matrix)
