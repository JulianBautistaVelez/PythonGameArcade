import arcade
import time
from GameConstants import GameConstants as const
from utils.Position import Position


# print("La lista de texturas del nuevo personaje tiene {} elementos".format(len(TEXTURES)))


class CharacterAttempt(arcade.Sprite):
    def __init__(self, character_type: int, position: Position):
        super().__init__()

        self.character_face_direction = const.CHARACTER_RIGHT_FACING
        self.center_x = position.center_in_pix_x
        self.center_y = position.center_in_pix_y

        self.current_texture = 0
        self.textures = arcade.load_spritesheet(
            "./resources/images/animated_characters/barbarian/barbarian_sheet_scaled_2.png", 30, 30, 10, 44)

        # type of character (player character or npc)
        self.character_type = character_type

        # steps to reach destiny
        self.steps = []
        self.actual_step = None
        self.destiny = None

        # state of the character
        self.reached_go_to = False
        self.moving = False
        self.explosives_time = time.time() - 5.0

        # collision box
        self.points = [[-10, -15], [10, -15], [-10, 8], [10, 8]]

        main_path = "./resources/images/animated_characters/barbarian/barbarian"

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
            if self.character_face_direction == const.CHARACTER_UP_FACING:
                self.set_texture(40)
            elif self.character_face_direction == const.CHARACTER_RIGHT_FACING:
                self.set_texture(41)
            elif self.character_face_direction == const.CHARACTER_DOWN_FACING:
                self.set_texture(42)
            else:
                self.set_texture(43)
            return

        self.current_texture += 1
        if self.current_texture > 27:
            self.current_texture = 0

        current_texture_number = (10*self.character_face_direction) + (self.current_texture // 3)
        # print("triying to acces the sprite number {}".format(current_texture_number))
        self.set_texture(current_texture_number)

    def get_position_in_grid(self):
        return Position(
            int(self.center_x // const.MAP_SPRITE_SIZE),
            int(self.center_y // const.MAP_SPRITE_SIZE)
        )

    def get_center(self):
        return [self.center_x, self.center_y]

    def set_path(self, steps):
        # for step in steps:
        #     print(step)
        self.steps = steps
        if not len(self.steps) == 0:
            self.actual_step = self.steps.pop(0)

    def set_destiny(self, destiny:Position):
        self.destiny = destiny

    def go_to(self, position: Position):
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

    def go_to_destiny(self):
        if self.center_x == self.destiny.center_in_pix_x and self.center_y == self.destiny.center_in_pix_y:
            # print("CHARACTER REACHED GO_TO")
            self.reached_go_to = True
            self.change_x = 0
            self.change_y = 0
        else:
            self.reached_go_to = False
            if self.center_x == self.actual_step.center_in_pix_x and self.center_y == self.actual_step.center_in_pix_y:
                self.actual_step = self.steps.pop(0)
                self.go_to(self.actual_step)

    def are_explosives_in_cooldown(self):
        if (time.time() - self.explosives_time) > 5.0:
            self.explosives_time = time.time()
            return False
        else:
            return True

























