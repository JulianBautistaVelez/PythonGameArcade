import arcade
from character.PlayerCharacter import PlayerCharacter
from character.PlayerConstats import PlayerConstants as pC
from objects.explosives.Explosives import Explosives
from utils.Position import Position
from map.Map import Map
from utils.Position import Position
import os


SCREEN_WIDTH = 992
SCREEN_HEIGHT = 672
SCREEN_TITLE = "Prueba juego"


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

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.wall_list = Map(SCREEN_WIDTH, SCREEN_HEIGHT).get_sprite_list()
        self.player = PlayerCharacter()

        self.player.center_x = (SCREEN_WIDTH // 2) + 10
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 0.8

        self.player_list.append(self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_list[0], self.wall_list)

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.explosions_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = pC.MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -pC.MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -pC.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = pC.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.SPACE:
            explosion = Explosives(self.player.center_x, self.player.center_y)
            self.explosions_list.append(explosion)

    def on_update(self, delta_time: float):
        # self.player_list.update()
        self.player_list.update_animation()
        self.explosions_list.update()
        # Try to solve the problem with diagonal collisions
        self.physics_engine.update()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()