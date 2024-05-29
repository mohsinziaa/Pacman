# Import necessary modules and classes
import pygame
from pygame.locals import *
from vector import Vector
from gameConstants import *
from entity import Entity
from sprites import PacmanSprites


# Pacman class representing the player-controlled character
class Pacman(Entity):
    def __init__(self, node):
        # Initialize Pacman with node, name, color, direction, and other attributes
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        # Reset Pacman's attributes to the initial state
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
        self.setSpeed(120)

    def die(self):
        # Set Pacman as not alive and stop its movement
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        # Update Pacman's position, direction, and sprites
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        if self.overshotTarget():
            # Update Pacman's node and target based on its movement
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            # Reverse Pacman's direction if it's moving in the opposite direction
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        # Get the valid key pressed for Pacman's movement
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        # Check if Pacman collides with any pellets in the given list
        for pellet in pelletList:
            # Check collision with each pellet
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        # Check if Pacman collides with a ghost
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        # Check if Pacman collides with another entity
        d = self.position - other.position
        dSquared = d.vectorMagnitudeSqr()
        rSquared = (self.collideRadius + other.collideRadius)**2
        # Check if the distance between Pacman and the other entity is within the collision radius
        if dSquared <= rSquared:
            return True
        return False
