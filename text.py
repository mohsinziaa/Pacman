import pygame
from vector import Vector
from gameConstants import *


# Text class representing a text element
class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        # Unique identifier for the text element
        self.id = id
        # Text content, color, size, and visibility
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        # Position of the text
        self.position = Vector(x, y)
        # Timer and lifespan for handling text visibility duration
        self.timer = 0
        self.lifespan = time
        # Pygame font-related attributes
        self.label = None
        self.destroy = False
        # Font setup using a specified font file
        self.setupFont("assets/PressStart2P-Regular.ttf")
        # Create the label surface
        self.createLabel()

    # Set up the font for rendering text
    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    # Create the label surface based on the current text content, color, and font
    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    # Set new text content and update the label
    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()

    # Update method to handle text visibility duration
    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    # Render the text on the screen if it's visible
    def render(self, screen):
        if self.visible:
            x, y = self.position.vectorTuple()
            screen.blit(self.label, (x, y))


# TextGroup class managing multiple Text elements
class TextGroup(object):
    def __init__(self):
        # ID tracking for new text elements
        self.nextid = 10
        # Dictionary to store all text elements
        self.alltext = {}
        # Initialize and set up default text elements
        self.setupText()
        self.showText(READYTXT)

    # Add a new text element to the group
    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(
            text, color, x, y, size, time=time, id=id)
        return self.nextid

    # Remove a text element from the group by its ID
    def removeText(self, id):
        self.alltext.pop(id)

    # Set up default text elements
    def setupText(self):
        size = TILEHEIGHT - 2
        self.alltext[SCORETXT] = Text(
            "0".zfill(6), WHITE, 10, TILEHEIGHT + 13, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(
            3), WHITE, 23*TILEWIDTH - 9, TILEHEIGHT + 13, size)
        self.alltext[READYTXT] = Text(
            "READY!", YELLOW, 11.6 * TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text(
            "PAUSED!", YELLOW, 11.1 * TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text(
            "GAMEOVER!", YELLOW, 10.15*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText("SCORE", WHITE, 10, 10, size)
        self.addText("LEVEL", WHITE, 23*TILEWIDTH - 10, 10, size)

    # Update all text elements in the group
    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    # Show a specific text element based on its ID
    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True

    # Hide specific text elements
    def hideText(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    # Update the displayed score text
    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    # Update the displayed level text
    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))

    # Update the text content of a specific text element
    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    # Render all text elements on the screen
    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
