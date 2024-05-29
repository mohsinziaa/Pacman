# Import necessary modules
from pygame.locals import *
from vector import Vector
from gameConstants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites


# Ghost class, inheriting from Entity
class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        # Initialize Ghost with attributes specific to ghost entities
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        # Reset method to reset the state of the Ghost
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        # Update method to handle the logic of ghost entities
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        # Set the goal to an initial position during scatter mode
        self.goal = Vector()

    def chase(self):
        # Set the goal to the position of the pacman during chase mode
        self.goal = self.pacman.position

    def spawn(self):
        # Set the goal to the spawnNode's position during spawn mode
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        # Set the spawnNode for the Ghost
        self.spawnNode = node

    def startSpawn(self):
        # Set the Ghost to spawn mode and initialize its properties
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        # Set the Ghost to freight mode and initialize its properties
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        # Set the Ghost back to normal mode and adjust its properties
        self.setSpeed(120)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)


# Blinky class, inheriting from Ghost
class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)


# Pinky class, inheriting from Ghost
class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        # Set the goal to a specific position during scatter mode
        self.goal = Vector(TILEWIDTH * NCOLS, 0)

    def chase(self):
        # Set the goal based on the position and direction of the pacman during chase mode
        self.goal = self.pacman.position + \
            self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


# Inky class, inheriting from Ghost
class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        # Set the goal to a specific position during scatter mode
        self.goal = Vector(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    def chase(self):
        # Calculate a goal based on pacman's position and a vector from blinky
        vec1 = self.pacman.position + \
            self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


# Clyde class, inheriting from Ghost
class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        # Set the goal to a specific position during scatter mode
        self.goal = Vector(0, TILEHEIGHT * NROWS)

    def chase(self):
        # Calculate the goal based on pacman's position and distance
        d = self.pacman.position - self.position
        ds = d.vectorMagnitudeSqr()
        if ds <= (TILEWIDTH * 8) ** 2:
            self.scatter()
        else:
            self.goal = self.pacman.position + \
                self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


# GhostGroup class to manage a group of ghosts
class GhostGroup(object):
    def __init__(self, node, pacman):
        # Initialize a group of ghosts with specified node and pacman
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        # Iterator for the GhostGroup
        return iter(self.ghosts)

    def update(self, dt):
        # Update method to update all ghosts in the group
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        # Start freight mode for all ghosts in the group
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        # Set spawnNode for all ghosts in the group
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        # Update points for all ghosts in the group
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        # Reset points for all ghosts in the group
        for ghost in self:
            ghost.points = 200

    def hide(self):
        # Hide all ghosts in the group
        for ghost in self:
            ghost.visible = False

    def show(self):
        # Show all ghosts in the group
        for ghost in self:
            ghost.visible = True

    def reset(self):
        # Reset all ghosts in the group
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        # Render all ghosts in the group
        for ghost in self:
            ghost.render(screen)
