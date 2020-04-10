import time
import arcade

from utils.Event import Event
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


class Explosive(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.detonation_time = const.CHARACTER_EXPLOSIVES_FUSE
        self.current_texture = 0
        self.textures = TEXTURES
        self.textures.insert(0, FIRST_TEXTURE)
        self.set_texture(self.current_texture)
        self.start_time = None
        self.alive = False
        self.position_in_grid = None

    def plant(self, position: Position):
        self.set_position(position.center_in_pix_x, position.center_in_pix_y-10)
        self.position_in_grid = position
        self.start_time = time.time()
        self.alive = True

    def update(self):
        if self.alive:
            if time.time() - self.start_time > self.detonation_time:
                self.current_texture += 1
                if self.current_texture < len(self.textures):
                    self.set_texture(self.current_texture)
                else:
                    self.explode()
                    self.alive = False
                    self.current_texture = 0
                    self.set_texture(self.current_texture)

    def draw(self):
        if self.alive:
            super().draw()

    def is_alive(self):
        return self.alive

    def explode(self):
        Event("Explosion", self)
        print("Esta area debería morir")
        # for pos in self.position_in_grid.get_neighbours(const.EXPLOSIVES_AOE):
        #     print(pos)