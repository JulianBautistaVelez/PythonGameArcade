import arcade
import time

TIME_TO_EXPLODE = 1
SPRITE_WIDTH = 256
SPRITE_HEIGHT = 256
COLUMNS = 16
COUNT = 60
FILE_NAME = "././resources/images/spritesheets/explosion.png"


class Explosives(arcade.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.detonation_time = TIME_TO_EXPLODE
        self.current_texture = 0
        self.textures = arcade.load_spritesheet(FILE_NAME, SPRITE_WIDTH, SPRITE_HEIGHT, COLUMNS, COUNT)
        self.center_x = pos_x
        self.center_y = pos_y
        self.start_time = time.time()

    def update(self):
        # if time.time() - self.start_time > 1.5:
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()
