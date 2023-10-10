import random
import arcade


class Apple(arcade.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__('assets/apple.png')
        self.width = 16
        self.height = 16
        self.center_x = (random.randint(8, SCREEN_WIDTH - 8)) // 8 * 8
        self.center_y = (random.randint(8, SCREEN_HEIGHT - 8)) // 8 * 8
        self.change_x = 0
        self.change_y = 0
