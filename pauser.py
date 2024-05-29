# Class representing the pause functionality in the game
class Pause(object):
    def __init__(self, paused=False):
        # Initialize the pause object with the specified attributes
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None

    def update(self, dt):
        # Update the pause state and execute the specified function if the pause duration is over
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        return None

    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        # Set the pause attributes and trigger the pause state
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    def flip(self):
        # Toggle the pause state
        self.paused = not self.paused
