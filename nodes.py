# Import necessary modules and classes
import pygame
from vector import Vector
from gameConstants import *
import numpy as np


# Node class representing a single node in the maze
class Node(object):
    def __init__(self, x, y):
        # Initialize Node with position, neighbors, and access permissions
        self.position = Vector(x, y)
        self.neighbors = {UP: None, DOWN: None,
                          LEFT: None, RIGHT: None, PORTAL: None}
        self.access = {UP: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       DOWN: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       LEFT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       RIGHT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def denyAccess(self, direction, entity):
        # Deny access for the specified entity in the given direction
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allowAccess(self, direction, entity):
        # Allow access for the specified entity in the given direction
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def render(self, screen):
        # Render node connections and position
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.vectorTuple()
                line_end = self.neighbors[n].position.vectorTuple()
                # Draw lines between neighboring nodes
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                # Draw circle at node position
                pygame.draw.circle(screen, RED, self.position.vectorInt(), 12)


# NodeGroup class managing a group of nodes in the maze
class NodeGroup(object):
    def __init__(self, level):
        # Initialize NodeGroup with level information and node-related data
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None

    def readMazeFile(self, textfile):
        # Read maze data from a text file
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        # Create a table of nodes based on maze data
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    # Create Node object and add to the lookup table
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        # Construct a unique key for a node based on coordinates
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        # Connect nodes horizontally based on maze data
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        # Connect current node with the previous one horizontally
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        # Connect nodes vertically based on transposed maze data
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        # Connect current node with the previous one vertically
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getStartTempNode(self):
        # Get the starting temporary node
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        # Set a portal pair between two nodes
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            # Set portal neighbors for the corresponding nodes
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def createHomeNodes(self, xoffset, yoffset):
        # Create home nodes for ghosts
        homedata = np.array([['X', 'X', '+', 'X', 'X'],
                             ['X', 'X', '.', 'X', 'X'],
                             ['+', 'X', '.', 'X', '+'],
                             ['+', '.', '+', '.', '+'],
                             ['+', 'X', 'X', 'X', '+']])
        # Create home nodes based on data and connect them
        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):
        # Connect home nodes in a specified direction
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

    def getNodeFromPixels(self, xpixel, ypixel):
        # Get the node at given pixel coordinates
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        # Get the node at given tile coordinates
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def denyAccess(self, col, row, direction, entity):
        # Deny access for an entity in a specific direction at given tile coordinates
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        # Allow access for an entity in a specific direction at given tile coordinates
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    def denyAccessList(self, col, row, direction, entities):
        # Deny access for a list of entities in a specific direction at given tile coordinates
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    def allowAccessList(self, col, row, direction, entities):
        # Allow access for a list of entities in a specific direction at given tile coordinates
        for entity in entities:
            self.allowAccess(col, row, direction, entity)

    def denyHomeAccess(self, entity):
        # Deny access for an entity to the home node
        self.nodesLUT[self.homekey].denyAccess(DOWN, entity)

    def allowHomeAccess(self, entity):
        # Allow access for an entity to the home node
        self.nodesLUT[self.homekey].allowAccess(DOWN, entity)

    def denyHomeAccessList(self, entities):
        # Deny access for a list of entities to the home node
        for entity in entities:
            self.denyHomeAccess(entity)

    def allowHomeAccessList(self, entities):
        # Allow access for a list of entities to the home node
        for entity in entities:
            self.allowHomeAccess(entity)

    def render(self, screen):
        # Render nodes on the screen
        for node in self.nodesLUT.values():
            node.render(screen)
