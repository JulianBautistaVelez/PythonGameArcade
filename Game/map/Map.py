import arcade
import random
from GameConstants import GameConstants as const
from utils.Position import Position


def create_grid_with_cells(grid):
    for row in range(const.MAP_GRID_SIZE):
        grid.append([])
        for column in range(const.MAP_GRID_SIZE):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(const.MAP_TILE_CRATE)
            elif column == 0 or row == 0 or column == const.MAP_GRID_SIZE - 1 or row == const.MAP_GRID_SIZE - 1\
                    or column == 6 or column == 18:
                grid[row].append(const.MAP_TILE_CRATE)
            else:
                grid[row].append(const.MAP_TILE_EMPTY)
    grid[2][18] = const.MAP_TILE_EMPTY
    grid[2][6] = const.MAP_TILE_EMPTY
    grid[26][18] = const.MAP_TILE_EMPTY
    grid[26][6] = const.MAP_TILE_EMPTY


def texture_maze(grid, wall_list):

    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == 1:
                wall_textures = [
                    arcade.Sprite("./resources/images/tiles/rock_wall0.png", const.MAP_SPRITE_SCALING),
                    arcade.Sprite("./resources/images/tiles/rock_wall1.png", const.MAP_SPRITE_SCALING)
                    # arcade.Sprite("./resources/images/tiles/skull_wall2.png", const.MAP_WALL_SPRITE_SCALING),
                    # arcade.Sprite("./resources/images/tiles/skull_wall3_R.png", 0.5),
                ]
                wall = wall_textures[random.randrange(0, 2)]
                wall.center_x = row * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                wall.center_y = column * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                wall_list.append(wall)


def texture_floor(grid, floor_list):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == 0:
                grass_textures = [
                    arcade.Sprite("./resources/images/high_grass/THX0_R.png", const.MAP_SPRITE_SCALING),
                    arcade.Sprite("./resources/images/high_grass/THX1_R.png", const.MAP_SPRITE_SCALING),
                    arcade.Sprite("./resources/images/high_grass/THX2_R.png", const.MAP_SPRITE_SCALING),
                    arcade.Sprite("./resources/images/high_grass/THX3_R.png", const.MAP_SPRITE_SCALING)
                ]
                grass = grass_textures[random.randrange(0, 3)]
                grass.center_x = row * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                grass.center_y = column * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                floor_list.append(grass)


class Map:
    def __init__(self):
        super().__init__()

        # To make sure there are odd number of vertical and horizontal cells
        self.size_x = const.MAP_GRID_SIZE
        self.size_y = const.MAP_GRID_SIZE
        # print("tamaño mapa en x:" + str(self.size_x) + " tamaño mapa en y:" + str(self.size_y))
        self.grid = []
        self.wall_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()

        create_grid_with_cells(self.grid)

        texture_maze(self.grid, self.wall_list)
        texture_floor(self.grid, self.grass_list)

    def get_sprite_list(self):
        return self.wall_list

    def get_grass_sprite_list(self):
        return self.grass_list

    def get_position_in_grid(self, position):
        return Position(
            position.pos_x // (const.GAME_SCREEN_WIDTH / self.size_x),
            position.pos_y // (const.GAME_SCREEN_HEIGHT / self.size_y)
        )

    def get_center_of_position(self, position: Position):
        return [
            int((position.pos_x * const.MAP_SPRITE_SIZE) + const.MAP_SPRITE_SIZE //2),
            int((position.pos_y * const.MAP_SPRITE_SIZE) + const.MAP_SPRITE_SIZE //2)
        ]
