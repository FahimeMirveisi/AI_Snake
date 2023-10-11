import random
import arcade


class Snake(arcade.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.width = 16
        self.height = 16
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.color = arcade.color.BLACK
        self.change_x = 1
        self.change_y = 0
        self.speed = 8
        self.score = 0
        self.body = []

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

        for part in self.body:
            arcade.draw_rectangle_filled(part['center_x'], part['center_y'], self.width, self.height, self.color)

    def move(self):
        self.body.append({'center_x': self.center_x, 'center_y': self.center_y})
        if len(self.body) > self.score +1:
            self.body.pop(0)
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

    def eat(self, apple):
        del apple
        self.score += 1
        print("Score:", self.score)


