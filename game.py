import pygame
import random

from copy import deepcopy

from TetrisFactory import TetrisFactory

ROW, COL = 20, 10
SIZE = 40
RES = COL * SIZE, ROW * SIZE
FPS = 60

animation_count, animation_speed, animation_limit = 0, 60, 2000

pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

piece = TetrisFactory().getPiece()

piece_rect = pygame.Rect(0, 0, SIZE-2, SIZE-2)

board = [[0 for i in range(COL)] for j in range(ROW)]



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
    
while True:
    rotate = False
    dx,dy = 0,0
    screen.fill(pygame.Color('black'))
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
            piece = TetrisFactory().getPiece()
            animation_limit = 2000
            
    #rotate
    figure_old = deepcopy(piece)
    if rotate:
        piece.rotate()
        rotate = False
        if check_collision():
            piece = figure_old

    #check lines
    line = ROW - 1
    for row in range(ROW-1, -1, -1):
        count = 0
        for col in range(COL):
            if board[row][col]:
                count += 1
            board[line][col] = board[row][col]
        if count < COL:
            line -= 1
    
    #game over
    for col in range(COL):
        if board[0][col]:
            quit()


    draw_grid()
    draw_figure()
    draw_board()
    pygame.display.flip()
    clock.tick(FPS)



    

  




