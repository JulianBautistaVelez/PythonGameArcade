import arcade
from GameConstants import GameConstants as const
from character.PlayerCharacter import PlayerCharacter
from objects.explosives.Explosives import Explosives
from utils.Position import Position
from utils.Path import PathFinder
from map.Map import Map
import os


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        self.physics_engine = None
        self.player_list = None
        self.wall_list = None
        self.explosions_list = None
        self.player = None
        self.player_position = None
        self.map = None

    def setup(self):
        self.map = Map(const.GAME_SCREEN_WIDTH, const.GAME_SCREEN_HEIGHT)
        self.player_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.wall_list = self.map.get_sprite_list()
        self.player = PlayerCharacter()
        self.player_position = Position(29, 19)
        position = self.map.get_center_of_position(self.player_position)
        # self.player.center_x = (const.GAME_SCREEN_WIDTH // 2)
        self.player.center_x = position[0]
        self.player.center_y = position[1]

        self.player_list.append(self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        destiny = Position(4,4)
        path = PathFinder.find_path_only_two_directions(
            self.map.grid,
            self.player.get_position_in_grid(self.map.size_x, self.map.size_y),
            destiny
        )
        self.player.set_path(path)

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.explosions_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = const.CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -const.CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -const.CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = const.CHARACTER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.SPACE:
            explosion = Explosives(self.player.center_x, self.player.center_y)
            self.explosions_list.append(explosion)

    def on_update(self, delta_time: float):
        self.player.go_to_destiny()
        # print("ESTOY EN:")
        # print(self.get_position_in_grid(31,21))
        # print("X: " + str(self.player.center_x) + " Y:" + str(self.player.center_y))
        # self.player_list.update()
        self.player_list.update_animation()
        self.explosions_list.update()
        # Try to solve the problem with diagonal collisions
        self.physics_engine.update()
        # print("EL CHARACTER ESTA EN LA POSICION: ")
        # print(self.player.get_center())


def main():
    game = MyGame(const.GAME_SCREEN_WIDTH, const.GAME_SCREEN_HEIGHT, const.GAME_SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()