'''
The PelletGroup class contributes to managing the state,
behavior, and rendering of pellets in the game, including both 
regular pellets and special power pellets. Pellets are collectible 
items that the player's character (in this case, Pac-Man) can 
consume by moving over them. Each pellet usually contributes to the player's score
'''

# Import necessary modules
import pygame
from vector import Vector
from gameConstants import *
import numpy as np


# Class representing a regular Pellet in the game
class Pellet(object):
    def __init__(self, row, column):
        # Initialize Pellet attributes
        self.name = PELLET
        self.position = Vector(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = WHITE
        self.radius = int(3 * TILEWIDTH / 16)
        self.collideRadius = 2 * TILEWIDTH / 16
        self.points = 10
        self.visible = True

    def render(self, screen):
        # Render the Pellet on the screen if it is visible
        if self.visible:
            adjust = Vector(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.vectorInt(), self.radius)


# Class representing a PowerPellet in the game, which has additional attributes and flash behavior
class PowerPellet(Pellet):
    def __init__(self, row, column):
        # Initialize PowerPellet attributes by calling the parent class's constructor
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        # Update the visibility of the PowerPellet based on flashing time
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


# Class representing a group of Pellets, including regular Pellets and PowerPellets
class PelletGroup(object):
    def __init__(self, pelletfile):
        # Initialize PelletGroup with empty lists for regular and power pellets and create the pellet list
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0

    def update(self, dt):
        # Update the visibility of power pellets
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def createPelletList(self, pelletfile):
        # Read the pellet file and create Pellet and PowerPellet objects based on the data
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        # Read the pellet file and return the data as a NumPy array
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        # Check if the pellet list is empty
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, screen):
        # Render all pellets in the pellet list
        for pellet in self.pelletList:
            pellet.render(screen)
