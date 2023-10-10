
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
        self.game_over_background = arcade.load_texture("assets/game_over_background1.png")
        self.game_over = False
        self.dataset = []
        self.old_direction = 1
        self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()

        if not self.game_over:

            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.game_background)

            self.snake.draw()
            self.apple.draw()

            arcade.draw_text(f"SCORE : {self.snake.score}", SCREEN_WIDTH - 300,
                             SCREEN_HEIGHT - 30, arcade.color.YELLOW_ROSE, font_size=20)

        elif self.game_over:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.game_over_background)
            arcade.exit()

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
                "bu": None,
                "br": None,
                "bd": None,
                "bl": None,
                "direction": None}

        self.snake.move()

        if self.snake.center_y > self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
            data["direction"] = 2

        elif self.snake.center_y < self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
            data["direction"] = 0

        elif self.snake.center_x > self.apple.center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
            data["direction"] = 3

        elif self.snake.center_x < self.apple.center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0
            data["direction"] = 1


        self.new_direction = data["direction"]
        # جمع آوری دیتای فاصله مار تا سیب
        if self.snake.center_x == self.apple.center_x and self.snake.center_y < self.apple.center_y:
            data["au"] = 1
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 0

        elif self.snake.center_x == self.apple.center_x and self.snake.center_y > self.apple.center_y:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 1
            data["al"] = 0

        elif self.snake.center_x < self.apple.center_x and self.snake.center_y == self.apple.center_y:
            data["au"] = 0
            data["ar"] = 1
            data["ad"] = 0
            data["al"] = 0

        elif self.snake.center_x > self.apple.center_x and self.snake.center_y == self.apple.center_y:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 1

        else:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 0

        # جمع آوری دیتای فاصله مار تا دیوار
        data["wu"] = SCREEN_HEIGHT - self.snake.center_y
        data["wr"] = SCREEN_WIDTH - self.snake.center_x
        data["wd"] = self.snake.center_y
        data["wl"] = self.snake.center_x

        if self.snake.score != 0:
             # حمع آوری دیتای فاصله مار تا بدن خودش
            for part in self.snake.body:
                if self.snake.center_x == part['center_x'] and self.snake.center_y < part['center_y']:
                    data["bu"] = 1
                    data["br"] = 0
                    data["bd"] = 0
                    data["bl"] = 0

                elif self.snake.center_x == part['center_x'] and self.snake.center_y > part['center_y']:
                    data["bu"] = 0
                    data["br"] = 0
                    data["bd"] = 1
                    data["bl"] = 0

                elif self.snake.center_x < part['center_x'] and self.snake.center_y == part['center_y']:
                    data["bu"] = 0
                    data["br"] = 1
                    data["bd"] = 0
                    data["bl"] = 0

                elif self.snake.center_x > part['center_x'] and self.snake.center_y == part['center_y']:
                    data["bu"] = 0
                    data["br"] = 0
                    data["bd"] = 0
                    data["bl"] = 1

                else:
                    data["bu"] = 0
                    data["br"] = 0
                    data["bd"] = 0
                    data["bl"] = 0

            if self.old_direction != self.new_direction:
                self.dataset.append(data)
                self.old_direction = self.new_direction
            #self.snake.move()

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat(self.apple)
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        #self.game_over_checker()

    def game_over_checker(self):
        for part in self.snake.body:
            if self.snake.center_x == part["center_x"] and self.snake.center_y == part["center_y"]:
                print("Snake hit his self.")
                self.game_over = True
                self.on_draw()

        if self.snake.center_x <= 8 or self.snake.center_x >= (
                SCREEN_WIDTH - 8) or self.snake.center_y <= 8 or self.snake.center_y >= (SCREEN_HEIGHT - 8):
            print("Snake hit wall.")
            self.game_over = True
            self.on_draw()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Q:
            df = pd.DataFrame(self.dataset)
            df.to_csv('dataset/dataset.csv', index=False)
            arcade.close_window()
            exit(0)


if __name__ == "__main__":
    game = Game()
    arcade.run()
