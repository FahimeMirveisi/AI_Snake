
import arcade
import pandas as pd

from snake import Snake
from apple import Apple


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Super Snake for generate dataset"

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(arcade.color.KHAKI)
        self.game_background = arcade.load_texture("assets/game_background.png")
        self.dataset = []
        self.old_direction = 1
        self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                        SCREEN_HEIGHT, self.game_background)

        self.snake.draw()
        self.apple.draw()

        arcade.draw_text(f"SCORE : {self.snake.score}", SCREEN_WIDTH - 300,
                            SCREEN_HEIGHT - 30, arcade.color.YELLOW_ROSE, font_size=20)

        arcade.finish_render()

    def on_update(self, delta_time: float):

        data = {"wu": None,
                "wr": None,
                "wd": None,
                "wl": None,
                "au": None,
                "ar": None,
                "ad": None,
                "al": None,
                "apple visible": None,
                "direction": None}

        self.snake.move()

        if self.snake.center_y < self.apple.center_y:
            data["au"] = 1
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 0
            if self.snake.center_x == self.apple.center_x:
                data["apple visible"] = 1
            else:
                data["apple visible"] = 0

        elif self.snake.center_y > self.apple.center_y:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 1
            data["al"] = 0
            if self.snake.center_x == self.apple.center_x:
                data["apple visible"] = 1
            else:
                data["apple visible"] = 0

        elif self.snake.center_x < self.apple.center_x:
            data["au"] = 0
            data["ar"] = 1
            data["ad"] = 0
            data["al"] = 0
            if self.snake.center_y == self.apple.center_y:
                data["apple visible"] = 1
            else:
                data["apple visible"] = 0

        elif self.snake.center_x > self.apple.center_x:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 1
            if self.snake.center_y == self.apple.center_y:
                data["apple visible"] = 1
            else:
                data["apple visible"] = 0


        # جمع آوری دیتای فاصله مار تا دیوار
        data["wu"] = SCREEN_HEIGHT - self.snake.center_y
        data["wr"] = SCREEN_WIDTH - self.snake.center_x
        data["wd"] = self.snake.center_y
        data["wl"] = self.snake.center_x


        if self.snake.center_y > self.apple.center_y or data['wu'] < 8:
            self.snake.change_x = 0
            self.snake.change_y = -1
            data["direction"] = 2

        elif self.snake.center_y < self.apple.center_y or data['wd'] < 8:
            self.snake.change_x = 0
            self.snake.change_y = 1
            data["direction"] = 0

        elif self.snake.center_x > self.apple.center_x or data['wr'] < 8:
            self.snake.change_x = -1
            self.snake.change_y = 0
            data["direction"] = 3

        elif self.snake.center_x < self.apple.center_x or data['wl'] < 8:
            self.snake.change_x = 1
            self.snake.change_y = 0
            data["direction"] = 1

        # append data to dataset
        self.dataset.append(data)

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat(self.apple)
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)


    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Q:
            df = pd.DataFrame(self.dataset)
            df.to_csv('dataset/dataset.csv', index=False)
            arcade.close_window()
            exit(0)


if __name__ == "__main__":
    game = Game()
    arcade.run()
