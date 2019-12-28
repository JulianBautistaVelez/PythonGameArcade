import arcade

SPRITE_SCALING = 0.25
NATIVE_SPRITE_SIZE = 128
SPRITE_SIZE = NATIVE_SPRITE_SIZE * SPRITE_SCALING
TILE_EMPTY = 0
TILE_CRATE = 1


def create_grid_with_cells(size_x, size_y, grid):
    for row in range(size_y):
        grid.append([])
        for column in range(size_x):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(TILE_CRATE)
            elif column == 0 or row == 0 or column == size_x - 1 or row == size_y - 1:
                grid[row].append(TILE_CRATE)
            else:
                grid[row].append(TILE_EMPTY)


def texture_maze(grid, wall_list):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == 1:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                wall_list.append(wall)


class Map:
    def __init__(self, width, height):
        super().__init__()

        # To make sure there are odd number of vertical and horizontal cells
        self.size_x = int((((width - SPRITE_SIZE /2) // SPRITE_SIZE) // 2) * 2 + 1)
        self.size_y = int(((height // SPRITE_SIZE) // 2) * 2 + 1)
        self.grid = []
        self.wall_list = arcade.SpriteList()

        create_grid_with_cells(self.size_x, self.size_y, self.grid)

        texture_maze(self.grid, self.wall_list)

    def get_sprite_list(self):
        return self.wall_list
