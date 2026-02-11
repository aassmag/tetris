import arcade
import random
from config import *
from shape import Shape


class Tetris(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

        self.current_piece = None
        self.next_piece = None

        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = START_SPEED
        self.last_fall_time = 0

        self.game_over = False
        self.paused = False

        self.spawn_new_piece()
        print("Game initialized!")

    def spawn_new_piece(self):
        if self.next_piece:
            self.current_piece = self.next_piece
            self.current_piece.x = BOARD_WIDTH // 2 - 1
            self.current_piece.y = 0
        else:
            shape_name = random.choice(list(SHAPES.keys()))
            self.current_piece = Shape(BOARD_WIDTH // 2 - 1, 0, shape_name)

        shape_name = random.choice(list(SHAPES.keys()))
        self.next_piece = Shape(0, 0, shape_name)

        if self.collision(self.current_piece):
            self.game_over = True
            print("Game Over!")

    def collision(self, piece):
        if not piece:
            return True

        positions = piece.get_positions()

        for x, y in positions:
            if x < 0 or x >= BOARD_WIDTH:
                return True
            if y >= BOARD_HEIGHT:
                return True
            if y >= 0 and self.board[y][x] != 0:
                return True
        return False

    def merge_piece(self):
        if not self.current_piece:
            self.spawn_new_piece()
            return

        positions = self.current_piece.get_positions()

        for x, y in positions:
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                self.board[y][x] = self.current_piece.color

        self.clear_lines()
        self.spawn_new_piece()

    def clear_lines(self):
        lines_cleared = 0
        y = BOARD_HEIGHT - 1

        while y >= 0:
            if all(self.board[y]):
                del self.board[y]
                self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1

        self.lines_cleared += lines_cleared
        self.level = self.lines_cleared // 5 + 1
        self.score += lines_cleared * 100 * self.level

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            arcade.color.DARK_BLUE
        )

        arcade.draw_rectangle_outline(
            BOARD_X + BOARD_WIDTH * CELL_SIZE // 2,
            BOARD_Y + BOARD_HEIGHT * CELL_SIZE // 2,
            BOARD_WIDTH * CELL_SIZE,
            BOARD_HEIGHT * CELL_SIZE,
            arcade.color.WHITE,
            2
        )

        for x in range(BOARD_WIDTH + 1):
            arcade.draw_line(
                BOARD_X + x * CELL_SIZE,
                BOARD_Y,
                BOARD_X + x * CELL_SIZE,
                BOARD_Y + BOARD_HEIGHT * CELL_SIZE,
                arcade.color.GRAY
            )

        for y in range(BOARD_HEIGHT + 1):
            arcade.draw_line(
                BOARD_X,
                BOARD_Y + y * CELL_SIZE,
                BOARD_X + BOARD_WIDTH * CELL_SIZE,
                BOARD_Y + y * CELL_SIZE,
                arcade.color.GRAY
            )

        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] != 0:
                    arcade.draw_rectangle_filled(
                        BOARD_X + x * CELL_SIZE + CELL_SIZE // 2,
                        BOARD_Y + (BOARD_HEIGHT - y - 1) * CELL_SIZE + CELL_SIZE // 2,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2,
                        COLORS[self.board[y][x]]
                    )

        if self.current_piece and not self.game_over:
            positions = self.current_piece.get_positions()
            for x, y in positions:
                if 0 <= y < BOARD_HEIGHT:
                    arcade.draw_rectangle_filled(
                        BOARD_X + x * CELL_SIZE + CELL_SIZE // 2,
                        BOARD_Y + (BOARD_HEIGHT - y - 1) * CELL_SIZE + CELL_SIZE // 2,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2,
                        COLORS[self.current_piece.color]
                    )

        arcade.draw_text(
            f"Score: {self.score}",
            NEXT_X,
            NEXT_Y,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Level: {self.level}",
            NEXT_X,
            NEXT_Y - 40,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "TETRIS",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            40,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_piece(-1, 0)
        elif key == arcade.key.RIGHT:
            self.move_piece(1, 0)
        elif key == arcade.key.DOWN:
            self.move_piece(0, 1)
        elif key == arcade.key.UP:
            self.rotate_piece()
        elif key == arcade.key.SPACE:
            self.drop_piece()
        elif key == arcade.key.R:
            self.reset_game()

    def move_piece(self, dx, dy):
        if self.game_over or not self.current_piece:
            return

        self.current_piece.x += dx
        self.current_piece.y += dy

        if self.collision(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:
                self.merge_piece()

    def rotate_piece(self):
        if self.game_over or not self.current_piece:
            return

        self.current_piece.rotate()
        if self.collision(self.current_piece):
            for _ in range(3):
                self.current_piece.rotate()

    def drop_piece(self):
        if self.game_over or not self.current_piece:
            return

        while not self.collision(self.current_piece):
            self.current_piece.y += 1

        self.current_piece.y -= 1
        self.merge_piece()

    def on_update(self, delta_time):
        if self.game_over or self.paused or not self.current_piece:
            return

        self.last_fall_time += delta_time
        if self.last_fall_time >= self.fall_speed:
            self.move_piece(0, 1)
            self.last_fall_time = 0

    def reset_game(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = START_SPEED
        self.game_over = False
        self.spawn_new_piece()


def main():
    print("Starting Tetris...")
    window = Tetris()
    arcade.run()


if __name__ == "__main__":
    main()