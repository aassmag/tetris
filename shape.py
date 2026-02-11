import copy
from config import *


class Shape:
    def __init__(self, x, y, shape_name):
        self.x = x
        self.y = y
        self.shape_name = shape_name
        self.shape = copy.deepcopy(SHAPES[shape_name])
        self.color = SHAPE_COLORS.get(shape_name, 1)
        self.rotation = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation = (self.rotation + 1) % 4

    def rotate_counter_clockwise(self):
        for _ in range(3):
            self.rotate()

    def get_positions(self):
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions

    def get_width(self):
        return len(self.shape[0])

    def get_height(self):
        return len(self.shape)



