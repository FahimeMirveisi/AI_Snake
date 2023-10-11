import tensorflow as tf
import numpy as np
import arcade
from snake import Snake
from apple import Apple


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Super Snake ML version"


# Class Game
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(arcade.color.KHAKI)
        self.game_background = arcade.load_texture("assets/game_background.png")
        self.game_over_background = arcade.load_texture("assets/game_over_background1.png")
        self.model = tf.keras.models.load_model('weights/my_snake_model.h5')
        self.game_over = False
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
                             SCREEN_HEIGHT - 30, arcade.color.YELLOW_ROSE, font_size= 20)

        elif self.game_over:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.game_over_background)
            arcade.exit()
        #arcade.finish_render()



    def game_over_func(self):
        for part in self.snake.body:
            if self.snake.center_x == part["center_x"] and self.snake.center_y == part["center_y"]:
                print("Snake hit his self")
                self.game_over = True
                self.on_draw()

        if self.snake.center_x <= 8 or self.snake.center_x >= SCREEN_WIDTH - 8 or self.snake.center_y <= 8 or self.snake.center_y >= SCREEN_HEIGHT - 8:
            print("Snake hit wall")
            self.game_over = True
            self.on_draw()

        if self.snake.score == -1:
            print("Snake score is -1")
            self.game_over = True
            self.on_draw()


    def on_update(self, delta_time: float):

        self.snake.move()

        data ={}

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

        elif self.snake.center_x == self.apple.center_x and self.snake.center_y > self.apple.center_y:
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

        # حمع آوری دیتای فاصله مار تا بدن خودش
        print("body", self.snake.body)
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


            elif self.snake.center_x > part['x'] and self.snake.center_y == part['y']:
                data['bu'] = 0
                data['bd'] = 0
                data['bl'] = 1
                data['br'] = 0

            elif self.snake.center_y < part['y']:
                data['bu'] = 1
                data['bd'] = 0
                data['bl'] = 0
                data['br'] = 0

            elif self.snake.center_y > part['y']:
                data['bu'] = 0
                data['bd'] = 1
                data['bl'] = 0
                data['br'] = 0

            elif self.snake.center_x < part['x']:
                data['bu'] = 0
                data['bd'] = 0
                data['bl'] = 0
                data['br'] = 1

            elif self.snake.center_x > part['x']:
                data['bu'] = 0
                data['bd'] = 0
                data['bl'] = 1
                data['br'] = 0


        print(data)
        data = list(data.values())
        data = np.array(data)
        print("Data is: ", data)


        output = self.model.predict(data)
        direction = output.argmax()
        if direction == 0:
            self.snake.change_x = 0
            self.snake.change_y = 1

        elif direction == 1:
            self.snake.change_x = 1
            self.snake.change_y = 0

        elif direction == 2:
            self.snake.change_x = 0
            self.snake.change_y = -1

        elif direction == 3:
            self.snake.change_x = -1
            self.snake.change_y = 0


        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat(self.apple)
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        #self.game_over_func()


    def on_key_release(self, symbol: int, modifiers: int):
        pass


if __name__ == "__main__":
    game = Game()
    arcade.run()