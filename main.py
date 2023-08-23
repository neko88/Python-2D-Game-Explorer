import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Python Game Explorer")

BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

## 1. Create a window for our game, specify size
window = pygame.display.set_mode((WIDTH, HEIGHT))

## 2. Define the main method and pass window
def main(window):
    pass


if __name__ == "__main__":      ## only run the file with this name
    main(window)