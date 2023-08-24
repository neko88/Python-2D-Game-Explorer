import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Python Game Explorer")

WIDTH, HEIGHT = 800, 500
FPS = 60
PLAYER_VEL = 5

## 1. Create a window for our game, specify size
window = pygame.display.set_mode((WIDTH, HEIGHT))

## 10. Function to flip the image of the sprite
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

## 11. Function to load a sprite sheet file and split into images.
## width and height are the size for the entire sheet that needs to be split
def load_sprite_sheet(dir1, dir2, width, height, direction = False):
    path = join("assets", dir1, dir2)
    ## 11a. first load all files into a list of images
    img_files = [f for f in listdir(path) if isfile(join(path, f))]     ## a for-loop in a list

    all_sprites = {}        ## dictionary for key:anim.style with val:imgs in anim

    ## 11b. for each image, load it as an image
    for image in img_files:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() ## convert alpha loads transparent img

        ## A sprite sheet turned to List of sprites RETURNED.
        ## Access by indices for a specific sprite animation img.
        sprites = []

        ## loop through the sprite sheet with index as an individual sprite img
        for loc in range(sprite_sheet.get_width() // width ):     ## gets the width of each sprite in a sprite sheet
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

            ## where in the image to take 1 individual and blit it to the window
            rect = pygame.Rect(loc * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)  ## refers back to sprite_sheet to blit the current sprite location
            sprites.append(pygame.transform.scale2x(surface))   ## append that individual sprite to the list

        ## Adding for multi-direction characters (renaming the file)
        ## So two keys are needed for each animation for L and R
        ## ".png" for file, + "_right" or "_left" is appended to the file name
        ## all_sprites[ key ] = value
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


## 16. Create a function to load block
## return the blitted image on the specified location (0,0)
def load_block(sprite_x, sprite_y, width, height):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    rect = pygame.Rect(sprite_x, sprite_y, width, height)       ## starts at pixel p
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


## 7. Create a draft block for our player
class Player(pygame.sprite.Sprite):
    COLOUR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheet("MainCharacters","PinkMan",32, 32, True)
    ANIMATION_DELAY = 2

    def __init__(self, x, y, width, height):  ## rather than indiv. values, place them all in the rect for easy access
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0  ## how fast the player moves each frame
        self.y_vel = 0
        self.mask = None
        self.direction = "left" ## to be used for ref. img direction and appending to img name
        self.animation_count = 0
        self.fall_count = 0 ## how long in the air for
        self.jump_count = 0

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

## 13b. Create function for jump
    def jump(self):
        self.y_vel = -self.GRAVITY * 8      ## negative for jumping up (0,0)TLC so negative subtracts "closer" to y=0
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

## 13a. Create function for fall
    def fall(self, fps):
        self.y_vel += min(1, (self.fall_count/fps) * self.GRAVITY)
        self.fall_count += 1

## 12. Create a function that updates its animation
    def update_sprite(self):
        sprite_sheet = "idle"   ## the individual anims of each sprite sheet has an 'action
        if self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction ## anim + dir it is facing
        sprites = self.SPRITES[sprite_sheet_name]
        ## sprite index to draw the anim in the sheet
        ## animation_count increments dynamically update the sprite anim to mimic movement %mod to get same index as it goes on
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def update(self):
        self.rect = self.sprite.get_rect(topLeft=(self.rect.x, self.rect.y))

    ## called 1/frame to MOVE player with anim updates.
    def loop(self, fps):
       ## self.fall(fps)
        self.move(self.x_vel, self.y_vel)
        self.update_sprite()

    ## visual for the player movement
    def draw(self, window):
        ## self.sprite = self.SPRITES["idle_" + self.direction][0] // example
        window.blit(self.sprite, (self.rect.x, self.rect.y))


## 14. Create a class Object
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


## 15. Create a class Block which inherits from Object
## Blocks will be size x size
class Block(Object):
    def __init__(self, x, y, sprite_x, sprite_y, width, height):
        super().__init__(x, y, width, height)  ## from Object
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        block = load_block(sprite_x, sprite_y, width, height)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


## 5. Creating method for background
def get_background(bg_name):
    image = pygame.image.load(join("assets", "Background", bg_name)).convert_alpha()  ## creates the path to the images
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
def draw(window, background, bg_img, player, objects):
    for tile in background:
        ## blit() displays tile on screen -> screen.blit(image, (100, 100))
        window.blit(bg_img, tuple(tile))
        ## 8a. execute the drawing of the player in the window
        player.draw(window)

        for obj in objects:
            obj.draw(window)

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
    block_size = 96

    ## 8. Create a player after defining its class and some movement functions.
    player = Player( 100, 100, 50, 50)
    blocks = [Block(0, HEIGHT - block_size, 96, 0, block_size, block_size)]

    ## 4. Setup for running &stopping the program
    while run:
        ## 4a. set up the clock
        clock.tick(FPS)  ## regulate frame rate accross different devices
        for event in pygame.event.get():  ## turn off game if quit
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        handle_move(player)
        ## 6. write the execution for draw method
        draw(window, background, bg_img, player, blocks)

    pygame.quit()
    quit()


if __name__ == "__main__":  ## only run the file with this name
    main(window)
