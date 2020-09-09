import pygame
from Solve import isValid, solve
from Problem_set import random_question
import random
import time
pygame.init()

WIDTH, HEIGHT = 450, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Sudoku')


class board:
    question = random_question()

    def __init__(self, win, rows, cols, width, height):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.content = [[Contents(self.question[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None
        self.update_model()

    def update_model(self):
        self.model = [[self.content[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        gap = self.width/9

        for i in range(self.rows):
            for j in range(self.cols):
                self.content[i][j].contents_draw(self.win)

        for i in range(self.rows+1):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (gap*i, 0), (gap*i, self.height), thick)
            pygame.draw.line(self.win, (0,0,0), (0, gap*i), (self.width, gap*i), thick)


    def set_temp(self, value):
        row, col = self.selected
        self.content[row][col].temp = value


    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width/9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def select_cube(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.content[i][j].selected = False

        self.content[row][col].selected = True
        self.selected = (row,col)

    def place(self, val):
        row, col = self.selected
        if self.content[row][col].value == ' ' and val != 0:
            self.content[row][col].value = val
            self.update_model()

        if isValid(self.model, val, (row, col)) and solve(self.model):
            return True
        else:
            self.content[row][col].value = ' '
            self.content[row][col].temp = 0
            self.update_model()
            return False



class Contents:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.selected = False
        self.temp = 0

    def contents_draw(self, win):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == ' ':
            fnt = pygame.font.SysFont('comicsans', 35)
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, ((x+5), (y+5)))

        elif not self.value == ' ':
            fnt = pygame.font.SysFont('comicsans', 35)
            text = fnt.render(str(self.value), 1, (32,32,32))
            pygame.draw.rect(win, (224,224,224), (x, y, gap, gap))
            win.blit(text, ((x + (gap/2 - text.get_width()/2)), (y + (gap/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(win, (0,0,255), (x, y, gap, gap), 4)

def get_time(secs):
    sec = secs % 60
    min = secs // 60
    mat = str(min) + ":" + str(sec)
    return mat


def redraw(win, bo, playtime, solved=False, wrong=False):
    win.fill((255,255,255))
    bo.draw()
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Time: " + get_time(playtime), 1, (0, 0, 0))
    win.blit(text, (WIDTH - text.get_width() - 20, WIDTH + 15))

    if solved:
        solved_board = board(win, 9, 9, WIDTH, WIDTH)
        solved_board.draw()

    if wrong:
        fnt = pygame.font.SysFont('comicsans', 30)
        text = fnt.render('Incorrect!', 1, (255,0,0))
        WIN.blit(text, (10, WIDTH+15))

def main():
    run = True
    bo = board(WIN, 9, 9, WIDTH, WIDTH)
    solved = False
    key = None
    wrong = False
    start = time.time()

    while run:
        play_time = round(time.time() - start)
        redraw(WIN, bo, play_time, solved, wrong)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solve(bo.question)
                    solved = True
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
                    if bo.content[i][j].temp != 0:
                        if bo.place(bo.content[i][j].temp):
                            wrong = False
                        else:
                            wrong = True
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = bo.click(pos)
                if clicked:
                    bo.select_cube(clicked[0], clicked[1])
                    key = None
                    wrong = False

        if bo.selected and key != None:
            bo.set_temp(key)

        pygame.display.update()

main()