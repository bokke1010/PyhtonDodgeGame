from base import *
import collision
import numexpr as ne
import numpy as np

class BulletManager():
    def __init__(self, screen: pygame.display, **kwargs):
        self.scr = screen
        self.visible = kwargs["visible"] if "visible" in kwargs else True
        self.endOfLife = False # Managers with this set to true wil be removed as soon as all of their bullets are gone
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.bulletcount = 0
        self.time = 0 # Time since this object is created in seconds


        # Style related
        colors = kwargs["color"] if "color" in kwargs else {}
        self.colorActive = colors["active"] if "active" in colors else PINK
        self.colorInactive = colors["inactive"] if "inactive" in colors else DARKGRAY
        self.colorFaded = colors["faded"] if "faded" in colors else DARKGRAY

        # bullet information
        self.bulletIndex = []
        self.bulletActive = []
        self.bulletTime = [] # Time since creation

    def setBulletStyle(self, **kwargs):
        """setting constant characteristics of the bullet, like:
        damage, lifetime and fade-in time"""
        self.damage = kwargs["damage"] if "damage" in kwargs else 1
        self.fadein = kwargs["fadein"] if "fadein" in kwargs else 0 #Passing down the bullet fuse
        self.lifeTime = kwargs["lifeTime"] if "lifeTime" in kwargs else 1000
        return self

    def setBulletPattern(self, shape:BULLETSHAPE, **kwargs):
        """setting expressed values of the bullet like shape, size and location"""
        self.shape = shape
        if (shape == BULLETSHAPE.BALL):
            self.GX = kwargs["x"]
            self.GY = kwargs["y"]
            self.size = kwargs["size"] if "size" in kwargs else "0.01"

            self.bulletX = []
            self.bulletY = []
            self.bulletSize = []
        elif (shape == BULLETSHAPE.BOX):
            self.GX = kwargs["x"]
            self.GY = kwargs["y"]
            self.GDX = kwargs["dx"]
            self.GDY = kwargs["dy"]

            self.bulletX = []
            self.bulletY = []
            self.bulletDX = []
            self.bulletDY = []
        elif (shape == BULLETSHAPE.LINE):
            self.invert = kwargs["invert"] if "invert" in kwargs else False
            self.Y1 = kwargs["y1"]
            self.Y2 = kwargs["y2"]
            self.DX1 = kwargs["dx1"]
            self.DX2 = kwargs["dx2"]

            self.bulletY1 = []
            self.bulletY2 = []
            self.bulletDX1 = []
            self.bulletDX2 = []
        return self

    def _createBullet(self, time: int = -1, lateFraction: int = 0):
        """Internal function that uses internal variables to create a bullet (NOT FOR EXTERNAL USE)"""

        if time == -1:
            time = self.time

        self.bulletIndex.append(self.spawnCounter)
        self.bulletcount += 1

        self.bulletTime.append(lateFraction)
        self.bulletActive.append(not self.fadein == -1)

        if (self.shape == BULLETSHAPE.BALL):
            self.bulletX.append(0)
            self.bulletY.append(0)
            self.bulletSize.append(0)
        elif (self.shape == BULLETSHAPE.BOX):
            self.bulletX.append(0)
            self.bulletY.append(0)
            self.bulletDX.append(0)
            self.bulletDY.append(0)
        elif (self.shape == BULLETSHAPE.LINE):
            self.bulletY1.append(0)
            self.bulletY2.append(0)
            self.bulletDX1.append(0)
            self.bulletDX2.append(0)

        self.spawnCounter += 1


    def draw(self):
        if self.visible:
            c = self.bulletIndex
            t = self.bulletTime
            for i in range(len(self.bulletIndex)):
                color = self.colorActive
                if not self.bulletActive[i]:
                    color = self.colorFaded
                if self.bulletTime[i] < self.fadein:
                    color = self.colorInactive
                self._drawBullet(color, i)

    def _drawBullet(self, color, i):
        if (self.shape == BULLETSHAPE.BALL):
            pos = (int(self.bulletX[i]*w), int(self.bulletY[i]*h))
            pygame.draw.circle(self.scr, color, pos, int(self.bulletSize[i]*w), 0)
        elif (self.shape == BULLETSHAPE.BOX):
            dx, dy = self.bulletDX[i], self.bulletDY[i]
            pos = (int((self.bulletX[i] - 0.5 * dx) * w), int((self.bulletY[i] - 0.5 * dy) * h))
            pygame.draw.rect(self.scr, color, pygame.Rect(*pos, int(dx * w), int(dy * h)))
        elif (self.shape == BULLETSHAPE.LINE):
            y1, y2 = self.bulletY1[i], self.bulletY2[i]
            y3, y4 = (self.bulletDX1[i] + y1)*h, (self.bulletDX2[i] + y2)*h
            pygame.draw.polygon(self.scr, color, ((0,y1*h), (0,y2*h), (w,y4), (w,y3)))


    def _setNPArrayShape(self, array:np.ndarray, count):
        if len(array.shape) == 0:
            return [float(array)] * count
        else:
            return list(array)


    def update(self, dt, player):
        events = Que()
        self.time += dt
        cleanupQue = set()
        (px, py) = player.pos()
        # TODO: possible future bulletshapes might not use x,y
        tb = self.bulletTime
        tt = dt
        tb = list(ne.evaluate("tb + tt")) # time = time + deltatime
        t = list(ne.evaluate("0.001 * tb")) # tb (timeBullet) is in microseconds, t is in seconds
        self.bulletTime = tb
        c = self.bulletIndex
        # ALL BULLET CALCULATIONS HERE

        # TODO: add function to listify numpy 0d or 1d arrays to given lenght
        if self.shape == BULLETSHAPE.BALL:
            x, y = self.bulletX, self.bulletY
            self.bulletX = self._setNPArrayShape(ne.evaluate(self.GX), self.bulletcount)
            self.bulletY = self._setNPArrayShape(ne.evaluate(self.GY), self.bulletcount)
            self.bulletSize = self._setNPArrayShape(ne.evaluate(self.size), self.bulletcount)
        elif self.shape == BULLETSHAPE.BOX:
            self.bulletX = self._setNPArrayShape(ne.evaluate(self.GX), self.bulletcount)
            self.bulletY = self._setNPArrayShape(ne.evaluate(self.GY), self.bulletcount)
            self.bulletDX = self._setNPArrayShape(ne.evaluate(self.GDX), self.bulletcount)
            self.bulletDY = self._setNPArrayShape(ne.evaluate(self.GDY), self.bulletcount)
        elif self.shape == BULLETSHAPE.LINE:
            self.bulletY1 = self._setNPArrayShape(ne.evaluate(self.Y1), self.bulletcount)
            self.bulletY2 = self._setNPArrayShape(ne.evaluate(self.Y2), self.bulletcount)
            self.bulletDX1 = self._setNPArrayShape(ne.evaluate(self.DX1), self.bulletcount)
            self.bulletDX2 = self._setNPArrayShape(ne.evaluate(self.DX2), self.bulletcount)



        for i, bi in enumerate(self.bulletIndex):
            a = self.bulletActive[i] and self.bulletTime[i] > self.fadein

            touching = False
            if self.shape == BULLETSHAPE.BALL:
                touching = collision.collidecircir((px, py), playerSize, (self.bulletX[i], self.bulletY[i]), self.bulletSize[i])
            elif self.shape == BULLETSHAPE.BOX:
                touching = collision.collidecirrect((px, py), playerSize, (self.bulletX[i], self.bulletY[i]), (self.bulletDX[i], self.bulletDY[i]))
            elif self.shape == BULLETSHAPE.LINE:
                touching = self.invert != collision.collidepointbetweenlineline(self.bulletY1[i], self.bulletDX1[i], self.bulletY2[i], self.bulletDX2[i], (px, py))

            # Collisions here
            if a and touching:
                events.add(Data("hit", damage=self.damage))
            # Bullets that exceed their lifetime get cleansed
            if self.bulletTime[i] > self.lifeTime:
                cleanupQue.add(i)

        # Got our list, now we just need to remove the bullets
        # TODO: clean up redundancy
        cleanupQue = list(cleanupQue)
        while len(cleanupQue) > 0:
            self.bulletcount -= 1
            index = cleanupQue[-1]
            self.bulletIndex.pop(index)
            if self.shape == BULLETSHAPE.BALL:
                self.bulletX.pop(index)
                self.bulletY.pop(index)
                self.bulletSize.pop(index)
            elif self.shape == BULLETSHAPE.BOX:
                self.bulletX.pop(index)
                self.bulletY.pop(index)
                self.bulletDX.pop(index)
                self.bulletDY.pop(index)
            elif self.shape == BULLETSHAPE.LINE:
                self.bulletY1.pop(index)
                self.bulletY2.pop(index)
                self.bulletDX1.pop(index)
                self.bulletDX2.pop(index)
            self.bulletTime.pop(index)
            self.bulletActive.pop(index)
            cleanupQue.pop()
        return list(events)



    def setDelete(self):
        self.endOfLife = True
        # While the endOfLife check in getdelete is obsolete, this way of checking
        # is easier to understand and change
        return self.getDelete()

    def getDelete(self):
        return self.endOfLife and len(self.bulletIndex) == 0

class BulletSpawner(BulletManager):
    def __init__(self, screen, delay: int = 90, **kwargs):
        super().__init__(screen=screen, **kwargs)
        # Spawning timing variables
        self.spawning = True
        self.delay = delay # Delay in ms between created bullets

    def update(self, dt, player):
        # Bullet creation
        if self.spawning:
            while (self.time - self.spawnCounter * self.delay) >= self.delay:
                time = (self.spawnCounter + 1) * self.delay
                # Using fraction in the name specifies that this variable is a
                # part (of a second), and as such measured in seconds
                lateFraction = (self.time - time)/1000
                # Using a internal helper to create the bullet
                # This function is defined in bulletManager, and uses internal variables
                # That is the reason we don't pass many arguments
                self._createBullet(time, lateFraction)
        return super().update(dt, player)

    def setDelete(self):
        self.spawning = False
        return super().setDelete()

class BulletPattern(BulletManager):
    def __init__(self, screen, **kwargs):
        super().__init__(screen = screen, **kwargs)

    def setBulletPattern(self, shape:BULLETSHAPE, **kwargs):
        self.count = kwargs["count"] if "count" in kwargs else 10
        return super().setBulletPattern(shape, **kwargs)

    def trigger(self):
        if not self.endOfLife:
            self.spawnCounter = 0
            for i in range(self.count):
                self._createBullet()
        else:
            raise Warning("This pattern is waiting for removal, will not spawn bullets")
