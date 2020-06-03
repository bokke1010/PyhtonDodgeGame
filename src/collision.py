from base import *
import math

sqdistance = lambda p1, p2: (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

distance = lambda p1, p2: sqdistance(p1, p2)**0.5

def distanceLess(p1, p2, distance, inclusiveEqual: bool = False):
    if inclusiveEqual:
        return sqdistance(p1, p2) <= distance**2
    else:
        return sqdistance(p1, p2) < distance**2

def sqdistancecirrect(p1, xy, dxdy):
    x, y = xy[0], xy[1]
    dx = max(abs(p1[0] - x) - dxdy[0] / 2, 0);
    dy = max(abs(p1[1] - y) - dxdy[1] / 2, 0);
    return dx * dx + dy * dy;

def pointaboveline(s1, cof1, p2):
    return s1 + cof1 * p2[0] < p2[1]

def collidecircir(p1, rad1, p2, rad2):
    return distanceLess(p1, p2, rad1 + rad2)

def collidecirrect(p1, rad1, xy, dxdy):
    return sqdistancecirrect(p1, xy, dxdy) < rad1 * rad1;

def collidepointbetweenlineline(p1, cof1, p2, cof2, p3):
    return pointaboveline(p1, cof1, p3) != pointaboveline(p2, cof2, p3)
