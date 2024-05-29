# Import constants from the constants module
from gameConstants import *

'''
 Scatter Mode:
    -Ghosts move to predefined corners of the maze.
    -Each ghost has a specific corner to target during Scatter mode.
    -Provides players with relief and a predictable pattern in ghost movements.

 Chase Mode:
    -Ghosts have individual strategies to target and capture Pac-Man.
    -Each ghost follows a distinct targeting strategy based on Pac-Man's position, direction, or other factors.
    -Introduces unpredictability and dynamic pursuit patterns to challenge the player.
'''


# MainMode class defining the main modes of the game (SCATTER, CHASE)
class MainMode(object):
    def __init__(self):
        # Initialize MainMode with timer and initial scatter mode
        self.timer = 0
        self.scatter()

    def update(self, dt):
        # Update method to switch between SCATTER and CHASE modes based on time
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        # Set the mode to SCATTER with specific time duration
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        # Set the mode to CHASE with specific time duration
        self.mode = CHASE
        self.time = 20
        self.timer = 0


# ModeController class managing the modes of an entity (Ghost)
class ModeController(object):
    def __init__(self, entity):
        # Initialize ModeController with timer, time, MainMode instance, current mode, and associated entity
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self, dt):
        # Update method to handle mode transitions and timer
        self.mainmode.update(dt)

        # Check if the entity is in FREIGHT mode
        if self.current is FREIGHT:
            self.timer += dt
            # Check if the FREIGHT mode time has elapsed
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode

        # Check if the entity is in SCATTER or CHASE mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        # Check if the entity is in SPAWN mode
        if self.current is SPAWN:
            # Check if the entity is at the spawn node
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode

    def setFreightMode(self):
        # Set the entity to FREIGHT mode and initialize the timer and time
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def setSpawnMode(self):
        # Set the entity to SPAWN mode
        if self.current is FREIGHT:
            self.current = SPAWN
