class GameConstants:
    ################################# GAME CONSTANTS #######################################
    GAME_SCREEN_WIDTH = 992
    GAME_SCREEN_HEIGHT = 672
    GAME_SCREEN_TITLE = "Prueba juego"
    GAME_VIEWPORT_MARGIN = 100

    ################################## CHARACTER CONTSTANTS ################################
    CHARACTER_PLAYER = 0
    CHARACTER_NPC = 1
    CHARACTER_MOVEMENT_SPEED = 2
    CHARACTER_UPDATES_PER_FRAME = 9
    CHARACTER_SPRITE_SCALING = 0.5
    CHARACTER_RIGHT_FACING = 0
    CHARACTER_LEFT_FACING = 1
    CHARACTER_UP_FACING = 2
    CHARACTER_DOWN_FACING = 3

    ##################################### MAP CONSTANTS #####################################
    MAP_SPRITE_SCALING = 0.25
    MAP_WALL_SPRITE_SCALING = 1
    MAP_NATIVE_SPRITE_SIZE = 128
    MAP_SPRITE_SIZE = MAP_NATIVE_SPRITE_SIZE * MAP_SPRITE_SCALING
    MAP_TILE_EMPTY = 0
    MAP_TILE_CRATE = 1
    MAP_SIZE_X = GAME_SCREEN_WIDTH // (MAP_SPRITE_SIZE / MAP_SPRITE_SCALING)
    MAP_SIZE_Y = GAME_SCREEN_HEIGHT // (MAP_SPRITE_SIZE / MAP_SPRITE_SCALING)
    MAP_GRID_SIZE = 30


