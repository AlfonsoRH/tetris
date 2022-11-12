import random
import pygame


class TetrisFactory:
    def __init__(self):
        self.pieces = [TetrisPiece1(), TetrisPiece2(), TetrisPiece3(), TetrisPiece4(), TetrisPiece5(), TetrisPiece6(), TetrisPiece7()]

    def getPiece(self):
        return random.choice(self.pieces)

class TetrisPiece:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape

    def getRect(self):
        rect = []
        for x, y in self.shape:
            rect.append(pygame.Rect(x + 10 // 2, y + 1, 1,1))
        return rect

    
    
    def rotate(self):
        for i in range(4):
            x = self.shape[i][0] - self.shape[1][0]
            y = self.shape[i][1] - self.shape[1][1]
            self.shape[i] = (self.shape[1][0] - y, self.shape[1][1] + x)



    def move(self, dx, dy):
        self.shape = [(x + dx, y + dy) for x, y in self.shape]


class TetrisPiece1(TetrisPiece):
    def __init__(self):
        super().__init__((255, 0, 0), [(-1, 0), (-2, 0), (0, 0), (1, 0)])

class TetrisPiece2(TetrisPiece):
    def __init__(self):
        super().__init__((0, 255, 0), [(0, -1), (-1, -1), (-1, 0), (0, 0)])

class TetrisPiece3(TetrisPiece):
    def __init__(self):
        super().__init__((0, 0, 255), [(-1, 0), (-1, 1), (0, 0), (0, -1)])

class TetrisPiece4(TetrisPiece):
    def __init__(self):
        super().__init__((255, 255, 0), [(0, 0), (-1, 0), (0, 1), (-1, -1)])

class TetrisPiece5(TetrisPiece):
    def __init__(self):
        super().__init__((255, 0, 255), [(0, 0), (0, -1), (0, 1), (-1, -1)])

class TetrisPiece6(TetrisPiece):
    def __init__(self):
        super().__init__((0, 255, 255), [(0, 0), (0, -1), (0, 1), (1, -1)])
    
class TetrisPiece7(TetrisPiece):
    def __init__(self):
        super().__init__((255, 255, 255), [(0, 0), (0, -1), (0, 1), (-1, 0)])


