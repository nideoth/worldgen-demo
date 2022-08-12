from enum import Enum, auto
from random import random, randint
from PIL import Image
import matplotlib.pyplot as plt

from noise import generate_noise, generate_island_gradient
from helpers import get_adjacent_xy


class Tile(Enum):
    water = (79, 143, 186)
    grass = (70, 130, 50)
    dirt = (173, 119, 87)
    sand = (231, 213, 179)
    snow = (235, 237, 233)
    rock = (87, 114, 119)
    #rock_dark = (57, 74, 80)
    tree = (25, 51, 45)


class WorldType(Enum):
    island = auto()
    archipelago = auto()


def generate_world(width: int, height: int, seed: int, type: WorldType) -> list[list[Tile]]:

    world = [[Tile.water for _ in range(height)] for _ in range(width)] 

    # Noise
    match type:
        case WorldType.island:
            noise = generate_noise(width, height, seed, octaves=3, period=128)
            island_gradient = generate_island_gradient(width, height)

            for x in range(width):
                for y in range(height):
                    # Island shape
                    noise[x][y] *= island_gradient[x][y]
                
                    # Terrains
                    value = noise[x][y]
                    if 0.40 < value <= 0.42:
                        world[x][y] = Tile.sand
                    if 0.42 < value <= 1.00:
                        world[x][y] = Tile.grass

        case WorldType.archipelago:
            noise = generate_noise(width, height, seed, octaves=1, period=64)

            for x in range(width):
                for y in range(height):
                
                    # Terrains
                    value = noise[x][y]
                    if 0.50 < value <= 0.55:
                        world[x][y] = Tile.sand
                    if 0.55 < value <= 1.00:
                        world[x][y] = Tile.grass

    # Forests
    forest_noise = generate_noise(width, height, seed-1, 1)

    for x in range(width):
        for y in range(height):

            if world[x][y] == Tile.grass and random() < 0.10 and forest_noise[x][y] > 0.5:
                no_adjacent = True
                for tile in get_adjacent_xy(x, y):
                    if world[tile[0]][tile[1]] in [Tile.tree, Tile.sand, Tile.water]:
                        no_adjacent = False
                        break
                if no_adjacent: 
                    world[x][y] = Tile.tree

    # Single trees
    for x in range(width):
        for y in range(height):
            if world[x][y] == Tile.grass and random() < 0.01:
                world[x][y] = Tile.tree

    return world


def world_to_image(world: list[list[Tile]]) -> Image:

    width = len(world)
    height = len(world[0])
    image = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            image.putpixel((x,y), world[x][y].value)

    return image


if __name__ == "__main__":

    seed = randint(0, 2**32)
    world = generate_world(256, 256, seed, WorldType.island)
    
    image = world_to_image(world)
    plt.imshow(image, cmap='gray')
    plt.show()
