import arcade
import time
from GameConstants import GameConstants as const
from utils.Position import Position


# print("La lista de texturas del nuevo personaje tiene {} elementos".format(len(TEXTURES)))


class Character(arcade.Sprite):
    def __init__(self, character_type: int, position: Position):
        super().__init__(center_x=position.center_in_pix_x, center_y=position.center_in_pix_y)

        self.character_face_direction = const.CHARACTER_RIGHT_FACING

        self.current_texture = 0
        self.frames_animation = 0

        if character_type == const.CHARACTER_PLAYER:
            self.textures = arcade.load_spritesheet(
                "./resources/images/animated_characters/barbarian/barbarian_running_sheet_scaled.png", 42, 45, 14, 80)
            self.frames_animation = const.CHARACTER_FRAMES_ON_ANIMATION
        else:
            self.textures = arcade.load_spritesheet(
                "./resources/images/animated_characters/automaton/automaton_walking_sheet_scaled.png", 52, 54, 12, 108)
            self.frames_animation = const.NPC_FRAMES_ON_ANIMATION

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

        # Slowing factor makes the game use the same sprite during 4 frames making the animation look smoother
        slowing_factor = 4
        self.current_texture += 1
        if self.current_texture > (self.frames_animation - 3) * slowing_factor:
            self.current_texture = 0

        current_texture_number = (self.frames_animation*self.character_face_direction) + \
                                 (self.current_texture // slowing_factor)
        # print("triying to acces the sprite number {}".format(current_texture_number))
        self.set_texture(current_texture_number)

    def get_position_in_grid(self):
        return Position(
            int(self.center_x // const.MAP_SPRITE_SIZE),
            int(self.center_y // const.MAP_SPRITE_SIZE)
        )

    def get_center(self):
        return [self.center_x, self.center_y]

    def are_explosives_in_cooldown(self):
        if (time.time() - self.explosives_time) > 5.0:
            self.explosives_time = time.time()
            return False
        else:
            return True

























