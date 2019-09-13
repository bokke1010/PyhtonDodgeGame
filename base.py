from enum import Enum
import pygame, random, math
from math import pi

w, h = 500, 500

class PROJECTILETYPE(Enum):
    BALL = 0
    BOX = 1

class GAMESTATE(Enum):
    ACTIVE = 0
    MMENU = 1
    HELP = 2

keyCodes = {119:"w", 97:"a", 115:"s", 100:"d", 304:"shift"}

# Some default colors:
BLACK     = (0  ,0  ,0  )
DARKGRAY  = (63 ,63 ,63 )
GRAY      = (127,127,127)
LIGHTGRAY = (191,191,191)
WHITE     = (255,255,255)
PINK      = (153,9  ,153)
CYAN      = (0  ,192,192)
DARKGREEN = (31 ,127,31 )
GREEN     = (63 ,255,63 )
RED       = (255,0  ,0  )
BLUE      = (0  ,0  ,255)


# Player properties
playerSize = 5
playerLives = 24
acceleration = 160
drag = 0.5

# Universal functions
distance = lambda p1, p2: ( ( (p1[0]-p2[0])**2 ) + ( (p1[1]-p2[1])**2) )**0.5

clamp = lambda x, l, u: max(l, min(u, x))

def isState(a,b):
    if not type(a) == int:
        a = a.value
    if not type(b) == int:
        b = b.value
    return a == b

def distanceLess(p1, p2, distance, inclusiveEqual: bool = False):
    if inclusiveEqual:
        return ( (p1[0]-p2[0])**2 ) + ( (p1[1]-p2[1])**2) <= distance**2
    else:
        return ( (p1[0]-p2[0])**2 ) + ( (p1[1]-p2[1])**2) < distance**2

def deactivateUIElement(UI, UIElement):
    if UIElement in UI:
        UI.remove(UIElement)

def activateUIElement(UI, UIElement):
    if not UIElement in UI:
        UI.append(UIElement)

sgn = lambda a : (a > 0) - (a < 0)

# Universal data type
class Data():
    def __init__(self, type: str, **data):
        self.type = type
        self.__dict__.update(data)

    def __repr__(self):
        x = "D"
        for key, item in self.__dict__.items():
            x += ", " + str(key) + ": " + str(item)
        return x

    def __len__(self):
        return len(self.__dict__)

    def __dir__(self):
        return list(self.__dict__)

    def set(self, key, value):
        self.__dict__[key] = value
        return self

    def hasattr(self, value):
        return value in self.__dict__
