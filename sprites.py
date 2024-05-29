# Import necessary modules
import pygame
from gameConstants import *
import numpy as np
from animation import Animator

# Constants for base tile width and height, and death animation identifier
BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5


# Spritesheet class for managing images from a spritesheet
class Spritesheet(object):
    def __init__(self):
        # Load spritesheet image
        self.sheet = pygame.image.load(
            "assets/pacman_spritesheet.png").convert()
        # Set transparent color
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        # Scale the spritesheet based on tile dimensions
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    # Method to get a specific image from the spritesheet
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


# PacmanSprites class for managing Pac-Man's sprites and animations
class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        # Initialize the superclass
        Spritesheet.__init__(self)
        self.entity = entity
        # Set Pac-Man's starting image
        self.entity.image = self.getStartImage()
        self.animations = {}
        # Define animations for different directions and death
        self.defineAnimations()
        # Set the default image for stopping
        self.stopimage = (8, 0)

    # Method to define animations for Pac-Man
    def defineAnimations(self):
        # Animation for moving left
        self.animations[LEFT] = Animator(((8, 0), (0, 0), (0, 2), (0, 0)))
        # Animation for moving right
        self.animations[RIGHT] = Animator(((10, 0), (2, 0), (2, 2), (2, 0)))
        # Animation for moving up
        self.animations[UP] = Animator(((10, 2), (6, 0), (6, 2), (6, 0)))
        # Animation for moving down
        self.animations[DOWN] = Animator(((8, 2), (4, 0), (4, 2), (4, 0)))
        # Death animation
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (
            10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    # Method to update Pac-Man's sprite based on direction and animation state
    def update(self, dt):
        # Check if Pac-Man is alive
        if self.entity.alive == True:
            # Check Pac-Man's current direction
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(
                    *self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(
                    *self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(
                    *self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(
                    *self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == STOP:
                # If Pac-Man is not moving, display the stopping image
                self.entity.image = self.getImage(*self.stopimage)
        else:
            # If Pac-Man is not alive, display the death animation
            self.entity.image = self.getImage(
                *self.animations[DEATH].update(dt))

    # Method to reset Pac-Man's animations
    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    # Method to get Pac-Man's starting image
    def getStartImage(self):
        return self.getImage(8, 0)

    # Override method to get an image using the base class method
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


# GhostSprites class for managing ghosts' sprites and animations
class GhostSprites(Spritesheet):
    def __init__(self, entity):
        # Initialize the superclass
        Spritesheet.__init__(self)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.entity = entity
        # Set the starting image for the ghost
        self.entity.image = self.getStartImage()

    # Method to update ghost's sprite based on direction and mode
    def update(self, dt):
        x = self.x[self.entity.name]
        # Check if the ghost is in SCATTER or CHASE mode
        if self.entity.mode.current in [SCATTER, CHASE]:
            # Check the ghost's current direction
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(x, 4)
        # Check if the ghost is in FREIGHT mode
        elif self.entity.mode.current == FREIGHT:
            # Display the freight mode sprite
            self.entity.image = self.getImage(10, 4)
        # Check if the ghost is in SPAWN mode
        elif self.entity.mode.current == SPAWN:
            # Check the ghost's current direction
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(8, 4)

    # Method to get the starting image for the ghost
    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)

    # Override method to get an image using the base class method
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


# FruitSprites class for managing fruit sprites
class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        # Initialize the superclass
        Spritesheet.__init__(self)
        self.entity = entity
        # Define different fruit sprites
        self.fruits = {0: (16, 8), 1: (18, 8), 2: (
            20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        # Set the starting image based on the current level
        self.entity.image = self.getStartImage(level % len(self.fruits))

    # Method to get the starting image for the fruit
    def getStartImage(self, key):
        return self.getImage(*self.fruits[key])

    # Override method to get an image using the base class method
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


# LifeSprites class for managing Pac-Man's remaining lives display
class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        # Initialize the superclass
        Spritesheet.__init__(self)
        # Reset the display with a certain number of lives
        self.resetLives(numlives)

    # Method to remove a life image from the display
    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    # Method to reset the display with a certain number of lives
    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0, 0))

    # Override method to get an image using the base class method
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


# MazeSprites class for managing maze-related sprites
class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        # Initialize the superclass
        Spritesheet.__init__(self)
        # Read maze configuration files
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    # Override method to get an image using the base class method
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    # Method to read a maze configuration file
    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    # Method to construct the maze background with appropriate rotation
    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    # Calculate the image index based on the digit in the maze file
                    x = int(self.data[row][col]) + 12
                    # Get the sprite image
                    sprite = self.getImage(x, y)
                    # Get the rotation value from the rotation file
                    rotval = int(self.rotdata[row][col])
                    # Rotate the sprite accordingly
                    sprite = self.rotate(sprite, rotval)
                    # Place the rotated sprite on the background
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    # If the character is '=', display a specific sprite
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background

    # Method to rotate a sprite
    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
