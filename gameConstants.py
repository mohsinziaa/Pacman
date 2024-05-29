# RGB color values for various entities and elements
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
TEAL = (100, 255, 255)
PINK = (255, 100, 150)
ORANGE = (230, 190, 40)
BLACK = (0, 0, 0)

# Text-related constants
SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4

# Constants related to tile dimensions and screen size
NROWS = 37
NCOLS = 28
TILEWIDTH = 20
TILEHEIGHT = 20
SCREENWIDTH = NCOLS * TILEWIDTH
SCREENHEIGHT = NROWS * TILEHEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# Entity types
PACMAN = 0
PELLET = 1
POWERPELLET = 2
GHOST = 3
BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUIT = 8

# Directional constants for movement
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
PORTAL = 3

# Ghost behavior modes
SCATTER = 0
CHASE = 1
FREIGHT = 2
SPAWN = 3
