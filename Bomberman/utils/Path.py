from utils.Position import Position
from GameConstants import GameConstants as const
import arcade


class PathFinder:

    @staticmethod
    def find_path_only_two_directions(grid, starting_pos: Position, end_pos: Position):
        steps = []
        current_pos = starting_pos
        game_map = grid
        # print("TAMAÑO DEL GRID RECIBIDO POR PATHFINDER:")
        # print(len(grid))
        # print(len(grid[0]))
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                  for row in grid]))
        possible_steps = []
        distances = []
        # Append the actual position as first step
        steps.append(starting_pos)
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
                    print("NO SE HA ENCONTRADO CAMINO HASTA EL DESTINO")
                    break

            else:
                # print("Posible steps")
                # print(len(possible_steps))
                step_selected = possible_steps[distances.index(min(distances))]
                grid[step_selected.pos_x][step_selected.pos_y] = 2
                steps.append(step_selected)
                current_pos = step_selected
                # print("SIGUIENTE PASO")
                # print(possible_steps[distances.index(min(distances))])
                # print("ME FALTA:")
                # print(min(distances))
                possible_steps.clear()
                distances.clear()

        # print("MAPA SOLUCIONADO:")
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                  for row in grid]))
        # for i in range(len(steps)):
        #     print(steps[i])
        return game_map

    @staticmethod
    def texture_steps(grid, wall_list: arcade.SpriteList):
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 2:
                    wall = arcade.Sprite(":resources:images/tiles/grass_sprout.png", const.MAP_SPRITE_SCALING)
                    wall.center_x = row * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                    wall.center_y = column * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                    wall_list.append(wall)