import arcade
import time

from utils.Position import Position
from GameConstants import GameConstants as const

SPRITE_WIDTH = 256
SPRITE_HEIGHT = 256
COLUMNS = 16
COUNT = 60
FIRST_SPRITE_SCALE = 0.3
FILE_NAME = "././resources/images/spritesheets/explosion.png"
# Preload of the textures
TEXTURES = arcade.load_spritesheet(FILE_NAME, SPRITE_WIDTH, SPRITE_HEIGHT, COLUMNS, COUNT)
FIRST_TEXTURE = arcade.load_texture("././resources/images/items/mine.png", scale=FIRST_SPRITE_SCALE)


class Explosives(arcade.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.detonation_time = const.CHARACTER_EXPLOSIVES_FUSE
        self.current_texture = 0
        self.textures = TEXTURES
        self.textures.insert(0, FIRST_TEXTURE)
        self.set_texture(self.current_texture)
        self.start_time = None
        self.alive = False

    def plant(self, position: Position):
        self.set_position(position.center_in_pix_x, position.center_in_pix_y-10)
        self.start_time = time.time()
        self.alive = True

    def update(self):
        if self.alive:
            if time.time() - self.start_time > self.detonation_time:
                self.current_texture += 1
                if self.current_texture < len(self.textures):
                    self.set_texture(self.current_texture)
                else:
                    self.alive = False
                    # self.remove_from_sprite_lists()

    def draw(self):
        if self.alive:
            super().draw()

    def is_alive(self):
        return self.alive