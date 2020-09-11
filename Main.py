from GUI import *
from Visualise import visualise
from Problem_set import select_question
from PIL import Image
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 650, 500
board_SIZE = 450
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Sudoku')

Icon = Image.open("Images\\sudoku.PNG")
Icon_img = pygame.image.fromstring(Icon.tobytes(), Icon.size, Icon.mode)

def main():
    run = True
    question = select_question()
    bo = Board(WIN, 9, 9, board_SIZE, board_SIZE, WIDTH, question)
    solved = False
    key = None
    wrong = None
    finished = False
    start = time.time()
    NEW_GAME = Button((0,25,51), 9, 15, 160, 36)
    HOW_TO_PLAY = Button((0,25,51), 9, 61, 160, 36)
    SUDOKU_SOLVER = Button((0,25,51), 9, 107, 160, 36)
    GET_SOLUTION = Button((0,25,51), 9, HEIGHT-132, 160, 36)
    VISUALISE = Button((0,25,51), 9, HEIGHT-86, 160, 36)

    def redraw_window():
        WIN.fill((255, 255, 255))
        pygame.draw.rect(WIN, (224, 224, 224), (0, 0, 180, 500))
        WIN.blit(Icon_img, (26, 190))
        bo.draw()
        fnt = pygame.font.SysFont("comicsans", 30)
        text = fnt.render("Time: " + get_time(play_time), 1, (0, 0, 0))
        WIN.blit(text, (WIDTH - text.get_width() - 25, board_SIZE + 15))

        VISUALISE.draw(WIN, 'Visualise Solution', 22, (0,0,0))
        NEW_GAME.draw(WIN, 'New Game', 22, (0,0,0))
        HOW_TO_PLAY.draw(WIN, 'How to play?', 22, (0, 0, 0))
        GET_SOLUTION.draw(WIN, 'Get Solution', 22, (0, 0, 0))
        SUDOKU_SOLVER.draw(WIN, 'Sudoku Solver', 22, (0, 0, 0))

        if solved:
            solved_board = Board(WIN, 9, 9, board_SIZE, board_SIZE, WIDTH, question)
            solved_board.draw()

        fnt1 = pygame.font.SysFont('comicsans', 30)
        if wrong == 0:
            text = fnt1.render('Incorrect!', 1, (255, 0, 0))
            WIN.blit(text, ((WIDTH - board_SIZE) + 15, board_SIZE + 15))
        elif wrong == 1:
            text = fnt1.render('Correct!', 1, (0, 255, 0))
            WIN.blit(text, ((WIDTH - board_SIZE) + 17, board_SIZE + 15))

        if finished:
            text = fnt1.render('You won!', 1, (0, 0, 255))
            WIN.blit(text, ((WIDTH - board_SIZE)+(board_SIZE/2) - text.get_width()/2 - 7, board_SIZE + 15))


    while run:
        play_time = round(time.time() - start)
        redraw_window()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_RETURN:
                    i,j = bo.selected
                    if bo.content[i][j].temp != 0 and bo.content[i][j].value == ' ':
                        if bo.place(bo.content[i][j].temp):
                            wrong = 1
                        else:
                            wrong = 0
                        key = None
                        if bo.isFinished():
                            finished = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = bo.click(pos)
                if clicked:
                    bo.select_cube(clicked[0], clicked[1])
                    key = None
                    wrong = None
                if VISUALISE.isOver(pos):
                    visualise(bo)
                if NEW_GAME.isOver(pos):
                    return True
                if GET_SOLUTION.isOver(pos):
                    solve(bo.question)
                    solved=True
                if SUDOKU_SOLVER.isOver(pos):
                    pass

            if event.type == pygame.MOUSEMOTION:
                if VISUALISE.isOver(pos):
                    VISUALISE.colour = (0,51,102)
                else:
                    VISUALISE.colour = (0,25,51)
                if NEW_GAME.isOver(pos):
                    NEW_GAME.colour = (0,51,102)
                else:
                    NEW_GAME.colour = (0,25,51)
                if HOW_TO_PLAY.isOver(pos):
                    HOW_TO_PLAY.colour = (0,51,102)
                else:
                    HOW_TO_PLAY.colour = (0,25,51)
                if GET_SOLUTION.isOver(pos):
                    GET_SOLUTION.colour = (0,51,102)
                else:
                    GET_SOLUTION.colour = (0,25,51)
                if SUDOKU_SOLVER.isOver(pos):
                    SUDOKU_SOLVER.colour = (0,51,102)
                else:
                    SUDOKU_SOLVER.colour = (0,25,51)


        if bo.selected and key != None:
            bo.set_temp(key)

        pygame.display.update()

if __name__ == '__main__':
    playing = True
    while playing:
        a = main()
        if not a:
            playing = False