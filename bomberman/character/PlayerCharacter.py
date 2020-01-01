import arcade
from GameConstants import GameConstants as const
from utils.Position import Position


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename, scale=const.CHARACTER_SPRITE_SCALING),
        arcade.load_texture(filename, scale=const.CHARACTER_SPRITE_SCALING),
        arcade.load_texture(filename, scale=const.CHARACTER_SPRITE_SCALING),
        arcade.load_texture(filename, scale=const.CHARACTER_SPRITE_SCALING)
    ]


def load_walking_textures(filename):
    textures_list = []
    for i in range(const.CHARACTER_UPDATES_PER_FRAME):
        frame = [
            arcade.load_texture(filename + f"_walk_{i}.png", scale=const.CHARACTER_SPRITE_SCALING, mirrored=True),
            arcade.load_texture(filename + f"_walk_{i}.png", scale=const.CHARACTER_SPRITE_SCALING),
            arcade.load_texture(filename + f"_walk_up_{i}.png", scale=const.CHARACTER_SPRITE_SCALING),
            arcade.load_texture(filename + f"_walk_down_{i}.png", scale=const.CHARACTER_SPRITE_SCALING)
        ]
        textures_list.append(frame)
    # print("TAMAÑO DE LA LISTA DE TEXTURAS")
    # print("--X-- " + str(len(textures_list)))
    # print("--Y-- " + str(len(textures_list[0])))
    return textures_list


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = const.CHARACTER_RIGHT_FACING

        self.current_texture = 0

        # steps to reach destiny
        self.steps = None
        self.actual_step = None

        # state of the character
        self.reached_go_to = True
        self.moving = False

        # collision box
        # self.points = [[-11, -32], [11, -32], [11, 14], [-11, 14]]
        self.points = [[-10, -15], [10, -15], [-10, 9], [10, 9]]

        main_path = "./resources/images/animated_characters/barbarian/barbarian"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        self.walk_textures = load_walking_textures(main_path)

    def update_animation(self, delta_time: float = 1/60):

        if self.change_x < 0 and self.character_face_direction != const.CHARACTER_LEFT_FACING:
            self.character_face_direction = const.CHARACTER_LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction != const.CHARACTER_RIGHT_FACING:
            self.character_face_direction = const.CHARACTER_RIGHT_FACING
        elif self.change_y > 0:
            self.character_face_direction = const.CHARACTER_UP_FACING
        elif self.change_y < 0:
            self.character_face_direction = const.CHARACTER_DOWN_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        self.current_texture += 1
        if self.current_texture > 8 * const.CHARACTER_UPDATES_PER_FRAME:
            self.current_texture = 0

        # print("TEXTURA A UTILIZAR")
        # print("--X-- " + str(self.current_texture // pC.UPDATES_PER_FRAME))
        # print("--Y-- " + str(self.character_face_direction))
        self.texture = \
            self.walk_textures[self.current_texture // const.CHARACTER_UPDATES_PER_FRAME][self.character_face_direction]

    def get_position_in_grid(self, size_x: int, size_y: int):
        return Position(
            int(self.center_x // (const.GAME_SCREEN_WIDTH / size_x)),
            int(self.center_y // (const.GAME_SCREEN_HEIGHT / size_y))
        )

    def get_center(self):
        return [self.center_x, self.center_y]

    def set_path(self, steps):
        self.steps = steps
        self.actual_step = self.steps.pop(0)

    def go_to(self, position: Position):
        # print("ESTOY EN:")
        # # print(self.get_position_in_grid(31,21))
        # print("X: " + str(self.center_x) + " Y:" + str(self.center_y))
        print("QUIERO IR A:")
        print(position)
        # print("HE LLEGADO?:")
        # print(self.reached_go_to)

        # if self.center_x == position.center_in_pix_x and self.center_y == position.center_in_pix_y:
        # if self.center_x != position.center_in_pix_x or self.center_y != position.center_in_pix_y:
        self.reached_go_to = False
        if self.center_x < position.center_in_pix_x:
            self.change_x = const.CHARACTER_MOVEMENT_SPEED
            self.change_y = 0
        elif self.center_x > position.center_in_pix_x:
            self.change_x = -const.CHARACTER_MOVEMENT_SPEED
            self.change_y = 0
        elif self.center_y < position.center_in_pix_y:
            self.change_y = const.CHARACTER_MOVEMENT_SPEED
            self.change_x = 0
        elif self.center_y > position.center_in_pix_y:
            self.change_y = -const.CHARACTER_MOVEMENT_SPEED
            self.change_x = 0
        # else:
        #     print("HE LLEGADO!!")
        #     self.change_x = 0
        #     self.change_y = 0
        #     self.reached_go_to = True
        #     self.moving = False

    def go_to_destiny(self):
        if self.center_x != self.steps[len(self.steps) - 1].center_in_pix_x or \
                self.center_y != self.steps[len(self.steps) - 1].center_in_pix_y:
            print("comparacion X: " + str(self.center_x) + ", " + str(self.actual_step.center_in_pix_x))
            print("comparacion Y: " + str(self.center_y) + ", " + str(self.actual_step.center_in_pix_y))
            if self.center_x == self.actual_step.center_in_pix_x and self.center_y == self.actual_step.center_in_pix_y:
                print("SEGUNDA COMPROBACION PASADA")

                self.change_x = 0
                self.change_y = 0
                self.reached_go_to = True
                self.actual_step = self.steps.pop(0)
                self.go_to(self.actual_step)
























