
import sys
import pygame
from copy import deepcopy
from abc import ABC, abstractmethod
from TetrisFactory import TetrisFactory


ROW, COL = 20, 10
SIZE = 40
RES = COL * SIZE, ROW * SIZE
DISPLAY = 750,850
FPS = 60


animation_count, animation_speed, animation_limit = 0, 60, 2000

pygame.init()
pygame.display.set_caption("Tetris")
display = pygame.display.set_mode(DISPLAY)
screen = pygame.Surface(RES)
clock = pygame.time.Clock() 

piece,next_piece = TetrisFactory().getPiece(), TetrisFactory().getPiece()

piece_rect = pygame.Rect(0, 0, SIZE-2, SIZE-2)

board = [[0 for i in range(COL)] for j in range(ROW)]

bg = pygame.image.load("score.jpg").convert()

game_bc = pygame.image.load("bg.jpg").convert()

bg = pygame.transform.smoothscale(bg, display.get_size())
game_bc = pygame.transform.smoothscale(game_bc, screen.get_size())

font = pygame.font.SysFont("Arial", 65)
font1 = pygame.font.SysFont("Arial", 45)

title_tetris = font.render("TETRIS", True, (255, 255, 255))

score, lines = 0, 0
scores = {0:0, 1:100, 2:300, 3:700, 4:1500}

def draw_grid():
    for y in range(ROW):
        for x in range(COL):
            rect = pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE)
            pygame.draw.rect(screen, (20,20,20), rect, 1)


def draw_figure():
    for i in range(4):
        piece_rect.x = piece.getRect()[i].x * SIZE
        piece_rect.y = piece.getRect()[i].y * SIZE
        pygame.draw.rect(screen, piece.color, piece_rect)

def draw_board():
    for y in range(ROW):
        for x in range(COL):
            if board[y][x]:
                piece_rect.x = x * SIZE
                piece_rect.y = y * SIZE
                pygame.draw.rect(screen, board[y][x], piece_rect)



def check_collision():
    for i in range(4):
        if piece.getRect()[i].x < 0 or piece.getRect()[i].x >= COL or piece.getRect()[i].y >= ROW:
            return True
        elif board[piece.getRect()[i].y][piece.getRect()[i].x]:
            return True
    return False



def quit():
    pygame.quit()
    sys.exit()
    

""" Proxy de loggeo para manejar el record"""
class Proxy:

    @classmethod
    def get_record(cls):
        """ Obtiene el record del archivo record.txt"""
        try:
            with open("record.txt", "r") as f:
                return f.readline()
        except FileNotFoundError:
            with open("record.txt", "w") as f:
                f.write("0")

    @classmethod
    def set_record(cls,record,score):
        """ Setea el record en el archivo record.txt"""
        r = max(int(record), score)
        with open("record.txt", "w") as f:
            f.write(str(r))



while True:

    
   
    record = Proxy.get_record()


    rotate = False
    dx,dy = 0,0

    display.blit(bg, (0,0))
    display.blit(screen, (20,20))
    screen.blit(game_bc, (0,0)) 

    

    for i in range(lines):
        pygame.time.wait(200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_DOWN:
                animation_limit = 100
            if event.key == pygame.K_UP:
                rotate = True

    #movement x
    figure_old = deepcopy(piece)
    piece.move(dx,dy)
    if check_collision():
        piece = figure_old
    
    #movement y
    animation_count += animation_speed
    if animation_count > animation_limit:
        animation_count = 0
        figure_old = deepcopy(piece)
        piece.move(0,1)
        if check_collision():
            for i in range(4):
                board[figure_old.getRect()[i].y][figure_old.getRect()[i].x] = figure_old.color
            piece = next_piece
            next_piece = TetrisFactory().getPiece()
            animation_limit = 2000
            
    #rotate
    figure_old = deepcopy(piece)
    if rotate:
        piece.rotate()
        if check_collision():
            piece = figure_old

    #check lines
    line,lines = ROW - 1, 0
    for row in range(ROW-1, -1, -1):
        count = 0
        for col in range(COL):
            if board[row][col]:
                count += 1
            board[line][col] = board[row][col]
        if count < COL:
            line -= 1
        else:
            lines += 1
            animation_limit +=1
    
    score += scores[lines]



    draw_grid()
    draw_figure()
    for i in range(4):
        piece_rect.x = next_piece.getRect()[i].x * SIZE + 380
        piece_rect.y = next_piece.getRect()[i].y * SIZE + 185
        pygame.draw.rect(display, next_piece.color, piece_rect)
    draw_board()    
   

    display.blit( title_tetris, (485,10))
    score_text = font1.render("SCORE", True, (255, 255, 255))
    display.blit( score_text, (450,740))
    display.blit(font.render(str(score), True, (255, 255, 255)), (450, 780))
    display.blit(font1.render("RECORD", True, (255, 255, 255)), (450, 580))
    display.blit(font.render(record, True, (255, 255, 255)), (450, 620))

    #game over
    for col in range(COL):
        if board[0][col]:
            Proxy.set_record(record, score)
            screen.fill(pygame.Color('black'))
            board = [[0 for i in range(COL)] for j in range(ROW)]
            animation_count, animation_limit,animation_speed = 0, 2000, 60
            score = 0
          

    pygame.display.flip()
    clock.tick(FPS)
 









