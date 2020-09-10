from Solver import *
import pygame

class Board:

    def __init__(self, win, rows, cols, width, height, WIDTH, question):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.WIDTH = WIDTH
        self.question = question
        self.content = [[Contents(self.question[i][j], i, j, width, height, win, WIDTH) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None
        self.update_model()

    def update_model(self):
        self.model = [[self.content[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        gap = self.width/9

        for i in range(self.rows):
            for j in range(self.cols):
                self.content[i][j].contents_draw()

        for i in range(self.rows+1):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (gap*i + (self.WIDTH - self.width - 10), 0), (gap*i + self.WIDTH - self.width - 10, self.height), thick)
            pygame.draw.line(self.win, (0,0,0), (self.WIDTH-self.width-10, gap*i), (self.WIDTH-10, gap*i), thick)


    def set_temp(self, value):
        row, col = self.selected
        self.content[row][col].temp = value


    def click(self, pos):
        if (self.WIDTH-self.width-10) < pos[0] < (self.WIDTH-10) and pos[1] < self.height:
            gap = self.width/9
            x = (pos[0] - (self.WIDTH-self.width-10)) // gap
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

    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.content[i][j].value == ' ':
                    return False
        return True


class Contents:

    def __init__(self, value, row, col, width, height, win, WIDTH):
        self.value = value
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.win = win
        self.WIDTH = WIDTH
        self.selected = False
        self.temp = 0

    def contents_draw(self):
        gap = self.width / 9
        x = self.col * gap + (self.WIDTH-self.width-10)
        y = self.row * gap

        if self.temp != 0 and self.value == ' ':
            fnt = pygame.font.SysFont('comicsans', 35)
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            self.win.blit(text, ((x+5), (y+5)))

        elif not self.value == ' ':
            fnt = pygame.font.SysFont('comicsans', 35)
            text = fnt.render(str(self.value), 1, (32,32,32))
            pygame.draw.rect(self.win, (224,224,224), (x, y, gap, gap))
            self.win.blit(text, ((x + (gap/2 - text.get_width()/2)), (y + (gap/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(self.win, (0,0,255), (x, y, gap, gap), 4)

    def draw_solution(self, correct):
        gap = self.width / 9
        x = self.col * gap + (self.WIDTH - self.width - 10)
        y = self.row * gap

        fnt = pygame.font.SysFont('comicsans', 35)
        text = fnt.render(str(self.value), 1, (32, 32, 32))
        pygame.draw.rect(self.win, (255, 255, 255), (x, y, gap, gap))
        self.win.blit(text, ((x + (gap / 2 - text.get_width() / 2)), (y + (gap / 2 - text.get_height() / 2))))

        if correct:
            pygame.draw.rect(self.win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(self.win, (255, 0, 0), (x, y, gap, gap), 3)

def get_time(secs):
    sec = secs % 60
    min = secs // 60
    mat = str(min) + ":" + str(sec)
    return mat


class Button:
    def __init__(self, colour, x, y, width, height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window, text, fontsize, outline=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont('comicsans', fontsize)
        text_label = font.render(text, 1, (250,250,250))
        window.blit(text_label, (self.x + (self.width/2 - text_label.get_width()/2), self.y + (self.height/2 - text_label.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x+ self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False