# Import necessary modules
from entity import Entity
from gameConstants import *
from sprites import FruitSprites


# Fruit class, inheriting from Entity
class Fruit(Entity):
    def __init__(self, node, level=0):
        # Initialize Fruit with attributes specific to fruit entities
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5  # Lifespan of the fruit in seconds
        self.timer = 0  # Timer to track the elapsed time since creation
        self.destroy = False  # Flag to indicate whether the fruit should be destroyed
        # Points awarded for consuming the fruit, scaling with level
        self.points = 100 + level * 20
        # Set the initial position of the fruit between nodes in the RIGHT direction
        self.setBetweenNodes(RIGHT)
        # Initialize FruitSprites for graphical representation
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        # Update method to handle the logic of fruit entities
        self.timer += dt  # Increment the timer with the elapsed time

        # Check if the fruit's lifespan has exceeded
        if self.timer >= self.lifespan:
            # Set the destroy flag to True, indicating that the fruit should be removed
            self.destroy = True
