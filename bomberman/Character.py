import arcade
import random
import os

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7

CHARACTER_SCALING =1

RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        