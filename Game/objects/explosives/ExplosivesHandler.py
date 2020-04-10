import arcade

from objects.explosives import Explosive
from objects.explosives.ExplosivesList import ExplosivesList
from utils.Observer import Observer
from GameConstants import GameConstants as const


class ExplosivesHandler(Observer):

    def __init__(self, player_list:arcade.SpriteList, npc_list:arcade.SpriteList, explosives_list:ExplosivesList):
        print("Explosives handler inicializado")
        Observer.__init__(self)
        self.player_list = player_list
        self.npc_list = npc_list
        self.set_explosives(explosives_list)

    def set_explosives(self, explosives_list:ExplosivesList):
        for explosive in explosives_list:
            self.observe("Explosion", self.explotion)

    def explotion(self, explosive:Explosive):
        print("Ha habido una explosion en %s" % explosive.position_in_grid)
        for player in self.player_list:
            if(player.get_position_in_grid() in
                    explosive
                            .position_in_grid
                            .get_neighbours(const.EXPLOSIVES_AOE)):
                player.kill()
                # print("ha muerto un jugador")

        for npc in self.npc_list:
            if(npc.get_position_in_grid() in
                    explosive
                            .position_in_grid
                            .get_neighbours(const.EXPLOSIVES_AOE)):
                npc.kill()
                # print("ha muerto un npc")