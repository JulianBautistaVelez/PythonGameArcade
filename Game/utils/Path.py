import arcade
import copy
from utils.Position import Position
from GameConstants import GameConstants as const


class PathFinder:

    @staticmethod
    def find_path_only_two_directions(starting_pos: Position, end_pos: Position, grid):
        steps = []
        current_pos = copy.deepcopy(starting_pos)
        game_map = copy.deepcopy(grid)
        possible_steps = []
        distances = []
        # Append the actual position as first step
        steps.append(current_pos)
        while current_pos != end_pos:
            if game_map[current_pos.pos_x + 1][current_pos.pos_y] == 0:
                possible_steps.append(Position(current_pos.pos_x + 1, current_pos.pos_y))
            if game_map[current_pos.pos_x - 1][current_pos.pos_y] == 0:
                possible_steps.append(Position(current_pos.pos_x - 1, current_pos.pos_y))
            if game_map[current_pos.pos_x][current_pos.pos_y + 1] == 0:
                possible_steps.append(Position(current_pos.pos_x, current_pos.pos_y + 1))
            if game_map[current_pos.pos_x][current_pos.pos_y - 1] == 0:
                possible_steps.append(Position(current_pos.pos_x, current_pos.pos_y - 1))
            for i in range(len(possible_steps)):
                distances.append(possible_steps[i].distance_to(end_pos))

            if len(possible_steps) == 0:
                if len(steps) > 0:
                    current_pos = steps.pop()
                else:
                    break
            else:
                step_selected = possible_steps[distances.index(min(distances))]
                steps.append(step_selected)
                game_map[step_selected.pos_x][step_selected.pos_y] = 2
                current_pos = step_selected
                possible_steps.clear()
                distances.clear()

        return steps

    @staticmethod
    def texture_steps(grid, wall_list: arcade.SpriteList):
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 2:
                    wall = arcade.Sprite(":resources:images/tiles/grass_sprout.png", const.MAP_SPRITE_SCALING)
                    wall.center_x = row * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                    wall.center_y = column * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                    wall_list.append(wall)

    @staticmethod
    def texture_final_path(steps, steps_list: arcade.SpriteList):
        for step in steps:
            image = arcade.Sprite(":resources:images/tiles/grass_sprout.png", const.MAP_SPRITE_SCALING)
            image.center_x = step.center_in_pix_y
            image.center_y = step.center_in_pix_y
            steps_list.append(image)