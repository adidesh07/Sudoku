import random

def solve(board):

    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if isValid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = ' '

    return False


def isValid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check col
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(board):

    for n in range(len(board)):
        if n % 3 == 0 and n != 0:
            print('- - - - - - - - - - - - -')

        for m in range(len(board[0])):
            if m % 3 == 0 and m != 0:
                print(' | ', end="")

            if m == 8:
                print(board[n][m])
            else:
                print(str(board[n][m]) + ' ', end="")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                return (i, j)  # row, col

    return None