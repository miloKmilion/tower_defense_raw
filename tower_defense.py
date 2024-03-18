"""
Tower defense game code after refactoring.
"""
import math
import random
from enum import Enum, auto
from tkinter import *

from PIL import Image, ImageDraw, ImageTk

from game import Game

# ! 1. Setting the global variables that will be used for setting the grid and map size.
grid_size = 30  # The height and width of the array of blocks
block_size = 20  # Pixels wide per block.
map_size = grid_size * block_size
block_grid = [[0 for y in range(grid_size)] for x in range(grid_size)]

block_array = ["NormalBlock",
               "PathBlock",
               "WaterBlock"]

monster_array = ["Monster1",
                 "Monster2",
                 "AlexMonster",
                 "LeonMonster",
                 "MonsterBig"]

tower_dictionary = {"Arrow Shooter": "ArrowShooterTower",
                    "Bullet Shooter": "BulletShooterTower",
                    "Tack Tower": "TackTower",
                    "Power Tower": "PowerTower",
                    }

tower_cost = {"Arrow Shooter": 150,
              "Bullet Shooter": 150,
              "Tack Tower": 150,
              "Power Tower": 200,
              }

tower_grid = [[None for y in range(grid_size)] for x in range(grid_size)]

path_list = []
spawn_x = 0
spawn_y = 0
monsters = []
monsters_by_health = []
monsters_by_health_reversed = []
monsters_by_distance = []
monsters_by_distance_reversed = []

monsters_list = [monsters_by_health, monsters_by_health_reversed, monsters_by_distance, monsters_by_distance_reversed]
projectiles = []
health = 100
money = 500000000
selected_tower = "<None>"
display_tower = None


# ! 2. Defining the state game by default params.
class TowerDefenseGameState(Enum):
    IDLE = auto()
    WAIT_FOR_SPAWN = auto()
    SPAWNING = auto()


# ! 3. Defining the main class for the game, where the constructor holds map variables and initial game status
class TowerDefense(Game):
    def __init__(self, title: str = "Tower Defense", width: int = map_size, height: int = map_size):
        super().__init__(title, width, height)
        self.state = TowerDefenseGameState.IDLE

    # 3.1 Defining the initial variables for the GUI
    def initialize(self):
        self.display_board = DisplayBoard(self)
        self.info_board = InfoBoard(self)
        self.tower_box = TowerBox(self)
        self.add_object(Map())
        self.add_object(Mouse(self))
        self.add_object(WaveGenerator(self))

    # 3.2 Defining the function to update values and params inside the game.
    def update(self):
        super().update()
        self.display_board.update()

        for p in projectiles:
            p.update()

        for y in range(grid_size):
            for x in range(grid_size):
                block_grid[x][y].update()

        for m in monsters:
            m.update()
        global monsters_by_health
        global monsters_by_health_reversed
        global monsters_by_distance
        global monsters_by_distance_reversed
        global monsters_list

        monsters_by_health = sorted(monsters, key=lambda x: x.health, reverse=True)
        monsters_by_distance = sorted(monsters, key=lambda x: x.distance_travelled, reverse=True)
        monsters_by_health_reversed = sorted(monsters, key=lambda x: x.health, reverse=False)
        monsters_by_distance_reversed = sorted(monsters, key=lambda x: x.distance_travelled, reverse=False)
        monsters_list = [monsters_by_health,
                         monsters_by_health_reversed,
                         monsters_by_distance,
                         monsters_by_distance_reversed]

        for y in range(grid_size):
            for x in range(grid_size):
                if tower_grid[x][y]:
                    tower_grid[x][y].update()

    def paint(self):
        super().paint()
        for y in range(grid_size):
            for x in range(grid_size):
                if tower_grid[x][y]:
                    tower_grid[x][y].paint(self.canvas)

        for i in range(len(monsters_by_distance_reversed)):
            monsters_by_distance_reversed[i].paint(self.canvas)

        for i in range(len(projectiles)):
            projectiles[i].paint(self.canvas)

        if display_tower:
            display_tower.paintSelect(self.canvas)
        self.display_board.paint()

    def set_state(self, state: TowerDefenseGameState):
        self.state = state


class Map:
    def __init__(self):
        self.image = None
        self.load_map("LeoMap")

    def load_map(self, mapName):
        self.drawn_map = Image.new("RGBA", (mapSize, mapSize), (255, 255, 255, 255))
        self.map_file = open("texts/mapTexts/" + mapName + ".txt", "r")
        self.grid_values = list(map(int, (self.map_file.read()).split()))
        for y in range(grid_size):
            for x in range(grid_size):
                global block_grid
                self.block_number = self.grid_values[grid_size * y + x]
                self.block_type = globals()[block_array[self.block_number]]
                block_grid[x][y] = self.block_type(
                    x * block_size + block_size / 2,
                    y * block_size + block_size / 2,
                    self.block_number,
                    x,
                    y,
                )  # creates a grid of Blocks
                block_grid[x][y].paint(self.drawn_map)
        self.drawn_map.save("images/mapImages/" + mapName + ".png")
        self.image = Image.open("images/mapImages/" + mapName + ".png")
        self.image = ImageTk.PhotoImage(self.image)

    def save_map(self):
        self.map_file = open("firstMap.txt", "w")
        for y in range(grid_size):
            for x in range(grid_size):
                self.map_file.write(block_grid[x][y].block_type + " ")
        self.map_file.close()

    def update(self):
        pass

    def paint(self, canvas):
        canvas.create_image(0, 0, image=self.image, anchor=NW)

class Game:

    def run(self):
        if not self.running:
            return
        self.update()  #
        self.paint()

        self.root.after(
            50, self.run
        )


def main():
    game = Game()  # IT starts the game application.


if main() == "__main__":
    main()
