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


## 7. Create a draft block for our player
class Player(pygame.sprite.Sprite):
    COLOUR = (255, 0, 0)
    GRAVITY = 1

    def __init__(self, x, y, width, height):  ## rather than indiv. values, place them all in the rect for easy access
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0  ## how fast the player moves each frame
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0 ## how long in the air for

    ## Displacement of the player's rect changes its (x,y) values
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def fall(self, fps):
        self.y_vel += min( 1, (self.fall_count/fps) * self.GRAVITY)
        self.fall_count += 1

    ## called 1/frame to MOVE player with anim updates.
    def loop(self, fps):
        self.fall(fps)
        self.move(self.x_vel, self.y_vel)



    ## visual for the player movement
    def draw(self, window):
        pygame.draw.rect(window, self.COLOUR, self.rect)

## 5. Creating method for background
def get_background(bg_name):
    image = pygame.image.load(join("assets", "Background", bg_name))  ## creates the path to the images
    _, _, width, height = image.get_rect()  ## grab width and height of img
    tiles = []  ## how many tiles we need

    ## how many x and y tiles we need for the specific img relative to the WIDTH x HEIGHT
    ## +1 for any gaps
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width,
                   j * height)  ## the position of the TLC of the tile to the window tile, every width&height amt of img
            tiles.append(pos)  ## Store each tile with its position in the tuple

    return tiles, image


## 6. Define the draw method
def draw(window, background, bg_img, player):
    for tile in background:
        ## blit() displays tile on screen -> screen.blit(image, (100, 100))
        window.blit(bg_img, tuple(tile))

        ## 8a. execute the drawing of the player in the window
        player.draw(window)

        pygame.display.update()

# 9. Create method to handle movement from keypress
def handle_move(player):
    keys = pygame.key.get_pressed() ## gets keys being pressed

    player.x_vel = 0        ## movement for holding key
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

## 2. Define the main method and pass window
def main(window):
    ## 3. Create a clock and set up
    clock = pygame.time.Clock()
    run = True
    ## 5. Get our background with the method created
    background, bg_img = get_background("Gray.png")

    ## 8. Create a player after defining its class and some movement functions.
    player = Player( 100, 100, 50, 50)

    ## 4. Setup for running &stopping the program
    while run:
        ## 4a. set up the clock
        clock.tick(FPS)  ## regulate frame rate accross different devices
        for event in pygame.event.get():  ## turn off game if quit
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player)

        ## 6. write the execution for draw method
        draw(window, background, bg_img, player)
    pygame.quit()
    quit()


if __name__ == "__main__":  ## only run the file with this name
    main(window)
