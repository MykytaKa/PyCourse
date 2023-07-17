# Вариант 10
# Элемент матрицы называется локальным минимумом, если он строго меньше всех имеющихся у него соседей.
# Подсчитать количество локальных минимумов заданной матрицы размером 10 х 10.
# Найти сумму модулей элементов, расположенных выше главной диагонали.ї
# change
import random

LENGTH = 5
HEIGHT = 5

MINVALUE = 0
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


def calc_sum(matrix):
    sum_of_modules = 0
    for i in range(LENGTH):
        for j in range(HEIGHT):
            if i < j:
                sum_of_modules += matrix[i][j]
    print(f'Sum: {sum_of_modules}')


def calc_local_minimum(matrix):
    amount_of_minimums = 0
    for i in range(LENGTH):
        for j in range(HEIGHT):
            row_start = i - 1 if i != 0 else i
            col_start = j - 1 if j != 0 else j
            minimum = matrix[i][j]
            is_number_minimum = True
            for k in range(row_start, row_start + 3):
                if k == HEIGHT:
                    break
                for m in range(col_start, col_start + 3):
                    if m == LENGTH:
                        break
                    if minimum > matrix[k][m]:
                        is_number_minimum = False
            if is_number_minimum:
                print(f'Local mimimum = {minimum} ({i}) ({j})')
                amount_of_minimums += 1
    print(f'Amount of local minimums: {amount_of_minimums}')


matrix = create_array()
matrix = fill_array(matrix)
print_array(matrix)
calc_sum(matrix)
calc_local_minimum(matrix)
