# Import constants from the constants module
from gameConstants import *


# MazeBase class providing a base structure for maze configuration
class MazeBase(object):
    def __init__(self):
        # Initialize attributes common to all mazes
        self.portalPairs = {}  # Dictionary to store portal pairs
        self.homeoffset = (0, 0)  # Offset for home nodes
        # Dictionary to deny access to ghost nodes
        self.ghostNodeDeny = {UP: (), DOWN: (), LEFT: (), RIGHT: ()}

    def setPortalPairs(self, nodes):
        # Set portal pairs in the maze nodes
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)

    def connectHomeNodes(self, nodes):
        # Connect home nodes with specific offsets
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)

    def addOffset(self, x, y):
        # Add home offset to coordinates
        return x + self.homeoffset[0], y + self.homeoffset[1]

    def denyGhostsAccess(self, ghosts, nodes):
        # Deny access to specific nodes for ghosts
        nodes.denyAccessList(*(self.addOffset(2, 3) + (LEFT, ghosts)))
        nodes.denyAccessList(*(self.addOffset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.denyAccessList(*(values + (direction, ghosts)))


# Maze1 class, inheriting from MazeBase, representing the configuration of the first maze
class Maze1(MazeBase):
    def __init__(self):
        # Initialize attributes specific to Maze1
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0: ((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        # self.fruitStart = (9, 20)
        self.ghostNodeDeny = {UP: ((12, 14), (15, 14), (12, 26), (15, 26)), LEFT: (self.addOffset(2, 3),),
                              RIGHT: (self.addOffset(2, 3),)}


# Maze2 class, inheriting from MazeBase, representing the configuration of the second maze
class Maze2(MazeBase):
    def __init__(self):
        # Initialize attributes specific to Maze2
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0: ((0, 4), (27, 4)), 1: ((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        # self.fruitStart = (11, 20)
        self.ghostNodeDeny = {UP: ((9, 14), (18, 14), (11, 23), (16, 23)), LEFT: (self.addOffset(2, 3),),
                              RIGHT: (self.addOffset(2, 3),)}


# MazeData class managing the available mazes
class MazeData(object):
    def __init__(self):
        # Initialize MazeData with an object placeholder and a dictionary of mazes
        self.obj = None
        self.mazedict = {0: Maze1, 1: Maze2}

    def loadMaze(self, level):
        # Load a maze based on the given level
        self.obj = self.mazedict[level % len(self.mazedict)]()
