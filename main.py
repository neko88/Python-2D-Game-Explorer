import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Python Game Explorer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

## 1. Create a window for our game, specify size
window = pygame.display.set_mode((WIDTH, HEIGHT))

## 5. Creating method for background
def get_background(bg_name):
    image = pygame.image.load(join("assets", "Background", bg_name))        ## creates the path to the images
    _, _, width, height = image.get_rect()      ## grab width and height of img
    tiles = []          ## how many tiles we need

    ## how many x and y tiles we need for the specific img relative to the WIDTH x HEIGHT
    ## +1 for any gaps
    for i in range( WIDTH // width + 1):
        for j in range( HEIGHT // height + 1):
            pos = (i * width, j * height)   ## the position of the TLC of the tile to the window tile, every width&height amt of img
            tiles.append(pos) ## Store each tile with its position in the tuple

    return tiles, image

## 6. Define the draw method
def draw(window, background, bg_img):
    for tile in background:
        ## blit() displays tile on screen -> screen.blit(image, (100, 100))
        window.blit(bg_img, tuple(tile))

        pygame.display.update()

## 2. Define the main method and pass window
def main(window):
    ## 3. Create a clock and set up
    clock = pygame.time.Clock()
    run = True
    ## 5. Get our background with the method created
    background, bg_img = get_background("Gray.png")

    ## 4. Setup for running &stopping the program
    while run:
        ## 4a. set up the clock
        clock.tick(FPS)     ## regulate frame rate accross different devices
        for event in pygame.event.get():        ## turn off game if quit
            if event.type == pygame.QUIT:
                run = False
                break
        ## 6. write the execution for draw method
        draw(window, background, bg_img)
    pygame.quit()
    quit()

if __name__ == "__main__":      ## only run the file with this name
    main(window)