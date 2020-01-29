from GameConstants import GameConstants as const
from utils.Position import Position
from character.Character import Character


class NpcCharacter(Character):
    def __init__(self, character_type: int, position: Position):
        super().__init__(character_type, position)
        # steps to reach destiny
        self.steps = []
        self.actual_step = None
        self.destiny = None
        self.reached_go_to = False

    def set_destiny(self, destiny: Position):
        self.destiny = destiny

    def set_path(self, steps):
        # for step in steps:
        #     print(step)
        self.steps = steps
        if not len(self.steps) == 0:
            self.actual_step = self.steps.pop(0)

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