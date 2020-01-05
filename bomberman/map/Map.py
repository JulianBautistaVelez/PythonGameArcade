import arcade
from GameConstants import GameConstants as const
from utils.Position import Position


def create_grid_with_cells(size_x, size_y, grid):
    for row in range(size_x):
        grid.append([])
        for column in range(size_y):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(const.MAP_TILE_CRATE)
            elif column == 0 or row == 0 or column == size_y - 1 or row == size_x - 1:
                grid[row].append(const.MAP_TILE_CRATE)
            else:
                grid[row].append(const.MAP_TILE_EMPTY)
    # grid[2][6] = const.MAP_TILE_EMPTY
    # grid[26][6] = const.MAP_TILE_EMPTY


def texture_maze(grid, wall_list):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == 1:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", const.MAP_SPRITE_SCALING)
                wall.center_x = row * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                wall.center_y = column * const.MAP_SPRITE_SIZE + const.MAP_SPRITE_SIZE / 2
                wall_list.append(wall)


class Map:
    def __init__(self, width, height):
        super().__init__()

        # To make sure there are odd number of vertical and horizontal cells
        self.size_x = int((((width - const.MAP_SPRITE_SIZE /2) // const.MAP_SPRITE_SIZE) // 2) * 2 + 1)
        self.size_y = int(((height // const.MAP_SPRITE_SIZE) // 2) * 2 + 1)
        print("tamaño mapa x:" + str(self.size_x) + "tamaño mapa y:" + str(self.size_y))
        self.grid = []
        self.wall_list = arcade.SpriteList()

        create_grid_with_cells(self.size_x, self.size_y, self.grid)

        texture_maze(self.grid, self.wall_list)

    def get_sprite_list(self):
        return self.wall_list

    def get_position_in_grid(self, position):
        return Position(
            position.pos_x // (const.GAME_SCREEN_WIDTH / self.size_x),
            position.pos_y // (const.GAME_SCREEN_HEIGHT / self.size_y)
        )

    def get_center_of_position(self, position: Position):
        return [
            int((position.pos_x * (const.GAME_SCREEN_WIDTH / self.size_x)) - const.MAP_SPRITE_SIZE //2),
            int((position.pos_y * (const.GAME_SCREEN_HEIGHT / self.size_y)) - const.MAP_SPRITE_SIZE //2)
        ]
