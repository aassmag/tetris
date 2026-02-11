import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Classic Tetris"

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30

BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH * CELL_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT * CELL_SIZE) // 2
NEXT_X = BOARD_X + BOARD_WIDTH * CELL_SIZE + 100
NEXT_Y = BOARD_Y + BOARD_HEIGHT * CELL_SIZE - 100

START_SPEED = 1.0
SPEED_INCREMENT = 0.05

COLORS = {
    0: arcade.color.BLACK,
    1: arcade.color.CYAN,
    2: arcade.color.BLUE,
    3: arcade.color.ORANGE,
    4: arcade.color.YELLOW,
    5: arcade.color.GREEN,
    6: arcade.color.PURPLE,
    7: arcade.color.RED
}

SHAPE_COLORS = {
    'I': 1,
    'O': 2,
    'T': 3,
    'S': 4,
    'Z': 5,
    'L': 6,
    'J': 7
}

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'L': [[1, 0, 0],
          [1, 1, 1]],
    'J': [[0, 0, 1],
          [1, 1, 1]]
}


