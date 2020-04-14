import arcade

from objects.explosives import Explosive
from objects.explosives.ExplosivesList import ExplosivesList
from utils.Observer import Observer
from GameConstants import GameConstants as const


class ExplosivesHandler(Observer):

    def __init__(self, player_list: arcade.SpriteList, npc_list: arcade.SpriteList, explosives_list: ExplosivesList):
        Observer.__init__(self)
        self.player_list = player_list
        self.npc_list = npc_list
        self.observe("Explosion", self.explotion)

    def explotion(self, explosive: Explosive):
        for player in self.player_list:
            if(player.get_position_in_grid() in
                    explosive
                            .position_in_grid
                            .get_neighbours(const.EXPLOSIVES_AOE)):
                player.kill()

        for npc in self.npc_list:
            if(npc.get_position_in_grid() in
                    explosive
                            .position_in_grid
                            .get_neighbours(const.EXPLOSIVES_AOE)):
                npc.kill()