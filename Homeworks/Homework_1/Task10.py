# Вариант 10
# Элемент матрицы называется локальным минимумом, если он строго меньше всех имеющихся у него соседей.
# Подсчитать количество локальных минимумов заданной матрицы размером 10 х 10.
# Найти сумму модулей элементов, расположенных выше главной диагонали.ї
# change
import random

length = 5
height = 5

minValue = 0
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


def calc_sum(matrix):
    sum = 0
    for i in range(length):
        for j in range(height):
            if i < j:
                sum += matrix[i][j]
    print("Sum:", sum)


def calc_local_minimum(matrix):
    amount_of_minimums = 0
    for i in range(length):
        for j in range(height):
            row_start = i - 1 if i != 0 else i
            col_start = j - 1 if j != 0 else j
            minimum = matrix[i][j]
            is_number_minimum = True
            for k in range(row_start, row_start + 3):
                if k == height:
                    break
                for m in range(col_start, col_start + 3):
                    if m == length:
                        break
                    if minimum > matrix[k][m]:
                        is_number_minimum = False
            if is_number_minimum:
                print("Local mimimum =", minimum ,"(", i, ")", "(", j, ")")
                amount_of_minimums += 1
    print("Amount of local minimums:", amount_of_minimums)


matrix = create_array()
matrix = fill_array(matrix)
print_array(matrix)
calc_sum(matrix)
calc_local_minimum(matrix)
