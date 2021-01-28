import os
import arcade
from GameConstants import GameConstants as const
from character.Character import Character
from character.NpcCharacter import NpcCharacter
from objects.explosives.ExplosivesHandler import ExplosivesHandler
from objects.explosives.ExplosivesList import ExplosivesList
from utils.Position import Position
from utils.Path import PathFinder
from utils.MyDecorators import run_async
from map.Map import Map

# TODO añadir más mecanicas al juego (que el npc ataque, que cambie la velocidad, etc)
# TODO intentar crear mapas proceduralmente
# TODO separar las diferentes ventanas en diferentes archivos

class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        # Attributes related to game window
        self.background = arcade.load_texture("./resources/images/map_objects/grass_texture.png")
        self.view_left = 0
        self.view_bottom = 0

        # Attributes related to physics
        self.physics_engine = None
        self.npc_list_physics_engine = {}

        # Attributes related to map and path finding
        self.map = Map()
        self.wall_list = self.map.get_sprite_list()

        # Attributes related to characters
        self.player_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()
        self.player = Character(const.CHARACTER_PLAYER, Position(10, 25))
        self.enemy1 = NpcCharacter(const.CHARACTER_NPC, Position(2, 2))
        self.enemy2 = NpcCharacter(const.CHARACTER_NPC, Position(20, 2))
        self.explosives_list = ExplosivesList()
        self.explosives_handler = ExplosivesHandler(self.player_list, self.npc_list, self.explosives_list)

    def setup(self):
        print(self.background)

        self.player_list.append(self.player)
        self.npc_list.append(self.enemy1)
        self.npc_list.append(self.enemy2)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        for npc in self.npc_list:
            self.npc_list_physics_engine[npc.id] = arcade.PhysicsEngineSimple(npc, self.wall_list)
            self.enemy_to_chase(npc)

    @run_async
    def enemy_to_chase(self, npc: NpcCharacter):
        if self.player.get_position_in_grid() != npc.get_position_in_grid():
            npc_steps = PathFinder.find_path_only_two_directions(
                npc.get_position_in_grid(),
                self.player.get_position_in_grid(),
                self.map.grid
            )
            if len(npc_steps) > 0:
                try:
                    npc.set_path(npc_steps)
                    npc.set_destiny(npc_steps[-1])
                except IndexError:
                    print("No hay camino decidido para npc")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(const.MAP_BACKGROUND_SIZE // 2, const.MAP_BACKGROUND_SIZE // 2,
                                      const.MAP_BACKGROUND_SIZE, const.MAP_BACKGROUND_SIZE, self.background)
        self.wall_list.draw()
        self.player_list.draw()
        self.npc_list.draw()
        self.explosives_list.draw()

    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        # TODO decidir si la lista de explosivos se puede hacer un atributo del personaje
        if key == arcade.key.SPACE:
            if not self.player.are_explosives_in_cooldown():
                self.explosives_list.plant_explosive(self.player.get_position_in_grid())
        else:
            self.player.on_key_release(key, modifiers)

    def on_update(self, delta_time: float):
        game_over = False

        if len(self.player_list) == 0 \
                or self.reached_by_enemy():
            message = "You lose :)"
            game_over = True
        elif len(self.npc_list) == 0:
            message = "You win :("
            game_over = True

        if game_over:
            game_over_view = GameOverView(message)
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

        for npc in self.npc_list:
            if npc.reached_go_to:
                self.enemy_to_chase(npc)
            npc.go_to_destiny()
        ###################################################################
        self.player_list.update_animation()
        self.npc_list.update_animation()
        self.explosives_list.update()
        self.physics_engine.update()
        for npc_engine in self.npc_list_physics_engine.values():
            npc_engine.update()

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

    def reached_by_enemy(self):
        for npc in self.npc_list:
            if npc.get_position_in_grid() == self.player.get_position_in_grid():
                return True
        return False


class GameOverView(arcade.View):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(self.message, const.GAME_SCREEN_WIDTH / 3, 650, arcade.color.WHITE, 30)
        arcade.draw_text("Game Over", const.GAME_SCREEN_WIDTH/3, 550, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", const.GAME_SCREEN_WIDTH/3, 500, arcade.color.WHITE, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = MyGame()
        game.setup()
        self.window.show_view(game)


def main():
    window = arcade.Window(const.GAME_SCREEN_WIDTH, const.GAME_SCREEN_HEIGHT, const.GAME_SCREEN_TITLE)
    game = MyGame()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()