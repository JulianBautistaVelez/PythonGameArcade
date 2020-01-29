import math
from GameConstants import GameConstants as const


class Position:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.center_in_pix_x = int((self.pos_x * const.MAP_SPRITE_SIZE) + const.MAP_SPRITE_SIZE // 2)
        self.center_in_pix_y = int((self.pos_y * const.MAP_SPRITE_SIZE) + const.MAP_SPRITE_SIZE // 2)

    def __str__(self):
        return "X:" + str(self.pos_x) + \
               " Y:" + str(self.pos_y) + \
               " PX_X:" + str(self.center_in_pix_x) + \
               " PX_Y:" + str(self.center_in_pix_y)

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y

    def __copy__(self):
        return Position(self.pos_x, self.pos_y)

    def distance_to(self, obj):
        return math.sqrt(math.pow((obj.pos_x - self.pos_x), 2) + math.pow((obj.pos_y - self.pos_y), 2))

    def get_neighbours(self, area: int):
        neighbours = []
        for i in range(self.pos_x - area, self.pos_x + area + 1):
            for j in range(self.pos_y - area, self.pos_y + area + 1):
                neighbours.append(Position(i, j))
        return neighbours