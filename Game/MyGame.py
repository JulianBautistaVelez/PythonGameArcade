import arcade
from GameConstants import GameConstants as const
from character.Character import Character
from character.NpcCharacter import NpcCharacter
from objects.explosives.Explosives import Explosives
from utils.Position import Position
from utils.Path import PathFinder
from utils.MyDecorators import run_async, log_timer
from map.Map import Map
import os

# TODO's * = opcionales

# TODO aprender a prefabricar objetos, activarlos y desactivarlos para hacer mas eficiente el programa
# TODO *Crear una clase ENEMY o NPC que extieda de Character y simplificar Character
# TODO implementar el daño o la muerte de los personajes
# TODO implementar que los explosivos maten lo que esta en su area de efecto
# TODO añadir más mecanicas al juego (que el npc ataque, que cambie la velocidad, etc)


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        # Attributes related to game window
        # arcade.set_background_color(arcade.color.BLACK)
        self.background = None
        self.view_left = 0
        self.view_bottom = 0

        # Attributes related to physics
        self.physics_engine = None
        self.npc_physics_engine = None

        # Attributes related to map and path finding
        self.map = Map()
        self.movements_grid = None
        self.wall_list = self.map.get_sprite_list()
        # self.grass_list = self.map.get_grass_sprite_list()
        # self.steps_list = arcade.SpriteList()

        # Attributes related to characters
        self.player_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()
        self.player = Character(const.CHARACTER_PLAYER, Position(10, 25))
        self.enemy = NpcCharacter(const.CHARACTER_NPC, Position(2, 2))
        self.explosions_list = arcade.SpriteList()

    def setup(self):
        self.background = arcade.load_texture("./resources/images/map_objects/grass_texture.png")
        print(self.background)

        self.player_list.append(self.player)
        self.npc_list.append(self.enemy)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.npc_physics_engine = arcade.PhysicsEngineSimple(self.enemy, self.wall_list)
        self.enemy_to_chase()

    @run_async
    def enemy_to_chase(self):
        npc_steps = PathFinder.find_path_only_two_directions(
            self.enemy.get_position_in_grid(),
            self.player.get_position_in_grid(),
            self.map.grid
        )
        if len(npc_steps) > 0:
            try:
                self.enemy.set_path(npc_steps)
                self.enemy.set_destiny(npc_steps[-1])
            except IndexError:
                print("No hay camino decidido para npc")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(const.MAP_BACKGROUND_SIZE // 2, const.MAP_BACKGROUND_SIZE // 2,
                                      const.MAP_BACKGROUND_SIZE, const.MAP_BACKGROUND_SIZE, self.background)
        self.wall_list.draw()
        # self.grass_list.draw()
        self.player_list.draw()
        self.npc_list.draw()
        self.explosions_list.draw()
        # self.steps_list.draw()

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
            if not self.player.are_explosives_in_cooldown():
                explosion = Explosives(self.player.center_x, self.player.center_y)
                self.explosions_list.append(explosion)

    def on_update(self, delta_time: float):
        if self.enemy.reached_go_to:
            self.enemy_to_chase()
        self.enemy.go_to_destiny()
        ###################################################################
        self.player_list.update_animation()
        self.npc_list.update_animation()
        self.explosions_list.update()
        self.physics_engine.update()
        self.npc_physics_engine.update()
        ####################################################################

        # --- Manage Scrolling ---

        # Keep track of if we changed the boundary. We don't want to call the
        # set_viewport command if we didn't change the view port.
        changed = False

        # Scroll left
        left_boundary = self.view_left + const.GAME_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + const.GAME_SCREEN_WIDTH - const.GAME_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + const.GAME_SCREEN_HEIGHT - const.GAME_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + const.GAME_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                const.GAME_SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                const.GAME_SCREEN_HEIGHT + self.view_bottom - 1)


def main():
    game = MyGame(const.GAME_SCREEN_WIDTH, const.GAME_SCREEN_HEIGHT, const.GAME_SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()