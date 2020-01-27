import arcade
import math
import time

from utils.Position import Position
from objects.explosives.Explosives import Explosives
from GameConstants import GameConstants as const


class ExplosivesList(arcade.SpriteList):
    def __init__(self):
        super().__init__()

        self.stock = math.ceil(const.CHARACTER_EXPLOSIVES_FUSE / const.CHARACTER_EXPLSIVES_COOLDOWN) + 1
        self.index = 0
        for _ in range(self.stock):
            self.append(Explosives())

        print("El tamaño de la lista de explosivos es {} ".format(self.stock))

    def update(self):
        for explosive in self.sprite_list:
            if explosive.is_alive():
                explosive.update()

    def draw(self):
        for explosive in self.sprite_list:
            if explosive.is_alive():
                explosive.draw()

    def plant_explosive(self, position:Position):
        self.index %= self.stock
        self.sprite_list[self.index].plant(position)
        self.index += 1