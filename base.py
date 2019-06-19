from enum import Enum
import pygame, random, math

w, h = 800, 600

class PROJECTILETYPE(Enum):
    BALL = 0
    BOX = 1

class SPAWNINGSTYLE(Enum):
    NONE = 0
    BOX = 1
    POINT = 2

class GAMESTATE(Enum):
    ACTIVE = 0
    MMENU = 1

gameState = GAMESTATE.ACTIVE

# Some default colors:
BLACK     = (0  ,0  ,0  )
DARKGRAY  = (63 ,63 ,63 )
GRAY      = (63 ,63 ,63 )
LIGHTGRAY = (63 ,63 ,63 )
WHITE     = (255,255,255)
PINK      = (153,9  ,153)
CYAN      = (0  ,192,192)
DARKGREEN = (31 ,127,31 )

# Player properties
playerSize = 8
acceleration = 4000
drag = 0.6

# Universal functions
def distance(p1, p2):
    return ( ( (p1[0]-p2[0])**2 ) + ( (p1[1]-p2[1])**2) )**0.5

def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
