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


def find_first_zero_value(matrix):
    is_col_contain_zero_value = False
    for i in range(height):
        for j in range(length):
            if matrix[j][i] == 0:
                is_col_contain_zero_value = True
                break
        if is_col_contain_zero_value == True:
            print("\nFirst column which contains zero value:", i + 1)
            break
    if is_col_contain_zero_value == False:
        print("\nMatrix has no one zero value")


def move_rows(moved_row, matrix):
    for j in range(height):
        temp = matrix[moved_row][j]
        matrix[moved_row][j] = matrix[moved_row + 1][j]
        matrix[moved_row + 1][j] = temp
    return matrix


def sort_matrix(sum, matrix):
    for i in range(length - 1):
        for j in range(length - 1 - i):
            if sum[j] < sum[j + 1]:
                temp = sum[j]
                sum[j] = sum[j + 1]
                sum[j + 1] = temp
                matrix = move_rows(j, matrix)
    return matrix


def calc_sum_of_negative_elements_and_sort_matrix(matrix):
    sum_of_negative_elements = [0] * length
    for i in range(length):
        for j in range(height):
            if (matrix[i][j] < 0) and (matrix[i][j] % 2 == 0):
                sum_of_negative_elements[i] += matrix[i][j]
    matrix = sort_matrix(sum_of_negative_elements, matrix)
    print("\nChanged matrix")
    print_array(matrix)


matrix = create_array()
matrix = fill_array(matrix)
print("Default matrix:")
print_array(matrix)
find_first_zero_value(matrix)
calc_sum_of_negative_elements_and_sort_matrix(matrix)
