from Solver import find_empty, isValid
import pygame
import time

def visualise(board):
    board.update_model()
    find = find_empty(board.model)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if isValid(board.model, i, (row, col)):
            board.model[row][col] = i
            board.content[row][col].value = i
            board.update_model()
            board.content[row][col].draw_solution(True)
            pygame.display.update()
            time.sleep(0.1)

            if visualise(board):
                return True

            board.model[row][col] = ' '
            board.content[row][col].value = ' '
            board.update_model()
            board.content[row][col].draw_solution(False)
            pygame.display.update()
            time.sleep(0.1)

    return False