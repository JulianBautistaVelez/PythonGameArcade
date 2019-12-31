import arcade
from character.PlayerConstats import PlayerConstants as pC


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename, scale=pC.CHARACTER_SCALING),
        arcade.load_texture(filename, scale=pC.CHARACTER_SCALING),
        arcade.load_texture(filename, scale=pC.CHARACTER_SCALING),
        arcade.load_texture(filename, scale=pC.CHARACTER_SCALING)
    ]


def load_walking_textures(filename):
    textures_list = []
    for i in range(pC.UPDATES_PER_FRAME):
        frame = [
            arcade.load_texture(filename + f"_walk_{i}.png", scale=pC.CHARACTER_SCALING, mirrored=True),
            arcade.load_texture(filename + f"_walk_{i}.png", scale=pC.CHARACTER_SCALING),
            arcade.load_texture(filename + f"_walk_up_{i}.png", scale=pC.CHARACTER_SCALING),
            arcade.load_texture(filename + f"_walk_down_{i}.png", scale=pC.CHARACTER_SCALING)
        ]
        textures_list.append(frame)
    # print("TAMAÑO DE LA LISTA DE TEXTURAS")
    # print("--X-- " + str(len(textures_list)))
    # print("--Y-- " + str(len(textures_list[0])))
    return textures_list


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = pC.RIGHT_FACING

        self.current_texture = 0

        # state of the character
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # collision box
        # self.points = [[-11, -32], [11, -32], [11, 14], [-11, 14]]
        self.points = [[-10, -15], [10, -15], [-10, 9], [10, 9]]

        main_path = "./resources/images/animated_characters/barbarian/barbarian"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        self.walk_textures = load_walking_textures(main_path)

    def update_animation(self, delta_time: float = 1/60):

        if self.change_x < 0 and self.character_face_direction != pC.LEFT_FACING:
            self.character_face_direction = pC.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction != pC.RIGHT_FACING:
            self.character_face_direction = pC.RIGHT_FACING
        elif self.change_y > 0:
            self.character_face_direction = pC.UP_FACING
        elif self.change_y < 0:
            self.character_face_direction = pC.DOWN_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        self.current_texture += 1
        if self.current_texture > 8 * pC.UPDATES_PER_FRAME:
            self.current_texture = 0

        # print("TEXTURA A UTILIZAR")
        # print("--X-- " + str(self.current_texture // pC.UPDATES_PER_FRAME))
        # print("--Y-- " + str(self.character_face_direction))
        self.texture = self.walk_textures[self.current_texture // pC.UPDATES_PER_FRAME][self.character_face_direction]

























