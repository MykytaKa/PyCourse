# Вариант 15
# Дана целочисленная прямоугольная матрица.
# Определить номер первого из столбцов, содержащих хотя бы один нулевой элемент.
# Характеристикой  строки  целочисленной  матрицы  назовем  сумму  ее  отрицательных  четных элементов.
# Переставляя строки заданной матрицы, располагать их в соответствии с убыванием характеристик.
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


def find_first_zero_value(matrix):
    is_col_contain_zero_value = False
    for i in range(HEIGHT):
        for j in range(LENGTH):
            if matrix[j][i] == 0:
                is_col_contain_zero_value = True
                break
        if is_col_contain_zero_value:
            print(f'\nFirst column which contains zero value: {i + 1}')
            break
    if is_col_contain_zero_value:
        print('\nMatrix has no one zero value')


def move_rows(moved_row, matrix):
    for j in range(HEIGHT):
        matrix[moved_row][j], matrix[moved_row + 1][j] = matrix[moved_row + 1][j], matrix[moved_row][j]
    return matrix


def sort_matrix(negative_sum, matrix):
    for i in range(LENGTH - 1):
        for j in range(LENGTH - 1 - i):
            if negative_sum[j] < negative_sum[j + 1]:
                negative_sum[j], negative_sum[j + 1] = negative_sum[j + 1], negative_sum[j]
                matrix = move_rows(j, matrix)
    return matrix


def calc_sum_of_negative_elements(matrix):
    sum_of_negative_elements = [0] * LENGTH
    for i in range(LENGTH):
        for j in range(HEIGHT):
            if matrix[i][j] < 0 and matrix[i][j] % 2 == 0:
                sum_of_negative_elements[i] += matrix[i][j]
    matrix = sort_matrix(sum_of_negative_elements, matrix)
    print('\nChanged matrix')
    print_array(matrix)


matrix = create_array()
matrix = fill_array(matrix)
print('Default matrix:')
print_array(matrix)
find_first_zero_value(matrix)
calc_sum_of_negative_elements(matrix)
