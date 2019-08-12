from enum import Enum
import pygame, random, math
from math import pi

w, h = 500, 500

class PROJECTILETYPE(Enum):
    BALL = 0
    BOX = 1

class BULLETPATH(Enum):
    NONE = 0
    LINE = 1
    EXPREL = 2
    EXPABS = 3

class SPAWNINGSTYLE(Enum):
    NONE = 0
    BOX = 1
    EXP = 2
    POINT = 3
    POINTEXP = 4
    EXPBEXP = 5 # This also allows the projectiles to evaluate their course
    BEXPABS = 6 # Projectiles use absolute coordinates

class PATTERNSTYLE(Enum):
    NONE = 0
    POINT = 1

class GAMESTATE(Enum):
    ACTIVE = 0
    MMENU = 1

keyCodes = {"119":"w", "97":"a", "115":"s", "100":"d", "304":"shift"}

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
acceleration = 160
drag = 0.5

# Universal functions
def distance(p1, p2):
    return ( ( (p1[0]-p2[0])**2 ) + ( (p1[1]-p2[1])**2) )**0.5

def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randomBetween(a, b):
    return a + (random.random() * (b-a))

def deactivateUIElement(UI, UIElement):
    if UIElement in UI:
        UI.remove(UIElement)

def activateUIElement(UI, UIElement):
    if not UIElement in UI:
        UI.append(UIElement)

def sgn(a):
    return (a > 0) - (a < 0)

# Universal data type
class Data():
    def __init__(self, type, **data):
        self.type = type
        self.__dict__.update(data)
