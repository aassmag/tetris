import arcade
from pyglet.graphics import Batch


class StartView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()
        self.batch = Batch()
        arcade.draw_text("Тетрис",
                         self.window.width // 2, self.window.height // 2,
                         arcade.color.YELLOW, 50, anchor_x="center")

        arcade.draw_text("Press any key to start",
                         self.window.width // 2, self.window.height // 2 - 75,
                         arcade.color.RED, 20, anchor_x="center")

        self.batch.draw()

    def on_key_press(self, key, modifiers):
        from screens import Tetris
        game_view = Tetris()
        self.window.show_view(game_view)