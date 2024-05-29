# Import constants module to use predefined constants
from gameConstants import *


# Animator class for handling animation logic
class Animator(object):

    def __init__(self, frames=[], speed=100, loop=True):
        # Initialize Animator with a list of frames, animation speed, and loop flag
        self.frames = frames
        self.currentFrame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0  # Delta time accumulator for frame timing
        self.finished = False  # Flag to indicate if the animation has finished

    def reset(self):
        # Reset the animation to its initial state
        self.currentFrame = 0
        self.finished = False

    def update(self, dt):
        # Update the animation state based on the elapsed time (dt)
        if not self.finished:
            self.nextFrame(dt)

        # Check if the animation has reached the end
        if self.currentFrame == len(self.frames):
            if self.loop:
                # If looping is enabled, reset to the first frame
                self.currentFrame = 0
            else:
                # If looping is disabled, mark the animation as finished
                self.finished = True
                self.currentFrame -= 1  # Ensure currentFrame doesn't exceed the last frame index

        # Return the current frame of the animation
        return self.frames[self.currentFrame]

    def nextFrame(self, dt):
        # Advance to the next frame based on the elapsed time and animation speed
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.currentFrame += 1
            self.dt = 0  # Reset the delta time for the next frame
