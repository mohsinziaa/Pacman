# Import necessary modules
import pygame
from pygame.locals import *
from vector import Vector
from gameConstants import *
from random import randint


# Entity class for defining game entities
class Entity(object):
    def __init__(self, node):
        # Initialize basic attributes for an entity
        self.name = None
        # Dictionary mapping direction constants to corresponding 2D vectors
        self.directions = {UP: Vector(
            0, -1), DOWN: Vector(0, 1), LEFT: Vector(-1, 0), RIGHT: Vector(1, 0), STOP: Vector()}
        self.direction = STOP
        # set speed function controls speed of the pacman
        self.setSpeed(120)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        # Set the entity's position based on the current node
        self.position = self.node.position.vectorCopy()

    def update(self, dt):
        # Update the entity's position based on its direction and speed
        self.position += self.directions[self.direction] * self.speed * dt

        # Check if the entity overshot its target node
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                # Check for portal and move to the connected node if available
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def validDirection(self, direction):
        # Check if the given direction is valid for the entity to move
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        # Get the new target node based on the given direction
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        # Check if the entity has overshot its target node
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.vectorMagnitudeSqr()
            node2Self = vec2.vectorMagnitudeSqr()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        # Reverse the direction of the entity
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        # Check if the given direction is opposite to the entity's current direction
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def validDirections(self):
        # Get a list of valid directions for the entity to move
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        # Choose a random direction from the list of valid directions
        return directions[randint(0, len(directions) - 1)]

    def goalDirection(self, directions):
        # Choose the direction that brings the entity closer to its goal
        distances = []
        for direction in directions:
            vec = self.node.position + \
                self.directions[direction] * TILEWIDTH - self.goal
            distances.append(vec.vectorMagnitudeSqr())
        index = distances.index(min(distances))
        return directions[index]

    def setStartNode(self, node):
        # Set the initial node and position for the entity
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        # Set the entity between its current node and the neighbor node in the given direction
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        # Reset the entity to its initial state
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        # Set the speed of the entity based on the given speed value
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        # Render the entity on the screen
        if self.visible:
            if self.image is not None:
                adjust = Vector(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.vectorTuple())
            else:
                p = self.position.vectorInt()
                pygame.draw.circle(screen, self.color, p, self.radius)
