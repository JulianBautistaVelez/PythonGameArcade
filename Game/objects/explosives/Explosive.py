import time
import arcade

from utils.Event import Event
from utils.Position import Position
from GameConstants import GameConstants as const


class Explosive(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # Preload of the textures
        self.textures = arcade.load_spritesheet(
            "././resources/images/spritesheets/explosion.png",
            const.EXPLOSIVES_SPRITE_WIDTH,
            const.EXPLOSIVES_SPRITE_HEIGHT,
            const.EXPLOSIVES_COLUMNS,
            const.EXPLOSIVES_COUNT)

        self.textures.insert(
            0,
            arcade.load_texture(
                 "././resources/images/items/mine.png",
                 scale=const.EXPLOSIVES_FIRST_SPRITE_SCALE
            )
        )

        self.detonation_time = const.CHARACTER_EXPLOSIVES_FUSE
        self.current_texture = 0

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