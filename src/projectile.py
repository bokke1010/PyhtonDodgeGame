from base import *
import numexpr as ne
import numpy as np

class BulletManager():
    def __init__(self, screen: pygame.display, visible: bool = True, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}):
        self.scr = screen
        self.visible = visible
        self.endOfLife = False # Managers with this set to true wil be removed as soon as all of their bullets are gone
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.bulletcount = 0
        self.time = 0 # Time since this object is created in seconds


        # Style related
        self.colorActive = color["active"]
        self.colorInactive = color["inactive"]
        self.colorFaded = color["faded"]

        # bullet information
        self.bulletIndex = []
        self.bulletActive = []
        self.bulletTime = [] # Time since creation
        return self

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

        self.spawnCounter += 1


    def draw(self):
        if self.visible:
            c = self.bulletIndex
            t = self.bulletTime
            for i, loc in enumerate(zip(self.bulletX, self.bulletY)):
                color = self.colorActive
                if not self.bulletActive[i]:
                    color = self.colorFaded
                if self.bulletTime[i] < self.fadein:
                    color = self.colorInactive
                self._drawBullet(loc, color, i)

    def _drawBullet(self, coords, color, i):
        if (self.shape == BULLETSHAPE.BALL):
            pos = (int(coords[0]*w), int(coords[1]*h))
            pygame.draw.circle(self.scr, color, pos, int(self.bulletSize[i]*w), 0)
        elif (self.shape == BULLETSHAPE.BOX):
            dx, dy = self.bulletDX[i], self.bulletDY[i]
            pos = (int((coords[0] - 0.5 * dx) * w), int((coords[1] - 0.5 * dy) * h))
            pygame.draw.rect(self.scr, color, pygame.Rect(*pos, int(dx * w), int(dy * h)))

    def _collide(self, i, playerPos, playerSize):
        # Bullet location, player location, bullet scale, player scale, bullet direction
        if self.shape == BULLETSHAPE.BALL:
            # pos, player.pos(), self.bulletSize[i]+player.size
            return distanceLess(playerPos, (self.bulletX[i], self.bulletY[i]), self.bulletSize[i] + playerSize)
        elif self.shape == BULLETSHAPE.BOX:
            x, y = self.bulletX[i], self.bulletY[i]
            collideX = abs(playerPos[0] - x) < 0.5 * self.bulletDX[i] + playerSize
            collideY = abs(playerPos[1] - y) < 0.5 * self.bulletDY[i] + playerSize
            return collideX and collideY
        return False

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
        x, y = self.bulletX, self.bulletY
        tb = self.bulletTime
        tt = dt
        tb = list(ne.evaluate("tb + tt")) # time = time + deltatime
        t = list(ne.evaluate("0.001 * tb")) # tb (timeBullet) is in microseconds, t is in seconds
        self.bulletTime = tb
        c = self.bulletIndex
        # ALL BULLET CALCULATIONS HERE

        self.bulletX = list(ne.evaluate(self.GX))
        self.bulletY = list(ne.evaluate(self.GY))
        # TODO: add function to listify numpy 0d or 1d arrays to given lenght
        if self.shape == BULLETSHAPE.BALL:
            self.bulletSize = self._setNPArrayShape(ne.evaluate(self.size), self.bulletcount)
        elif self.shape == BULLETSHAPE.BOX:
            self.bulletDX = self._setNPArrayShape(ne.evaluate(self.GDX), self.bulletcount)
            self.bulletDY = self._setNPArrayShape(ne.evaluate(self.GDX), self.bulletcount)



        for i, bi in enumerate(self.bulletIndex):
            a = self.bulletActive[i] and self.bulletTime[i] > self.fadein

            # Collisions here
            if a and self._collide(i, player.pos(), player.size):
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
            self.bulletX.pop(index)
            self.bulletY.pop(index)
            if self.shape == BULLETSHAPE.BALL:
                self.bulletSize.pop(index)
            elif self.shape == BULLETSHAPE.BOX:
                self.bulletDX.pop(index)
                self.bulletDY.pop(index)
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
    def __init__(self, screen, spawningDelay: int = 90, visible: bool = True, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}):
        super().__init__(screen=screen, visible = visible, color = color)
        # Spawning timing variables
        self.spawning = True
        self.delay = spawningDelay # Delay in ms between created bullets

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
    def __init__(self, screen, visible: bool = True, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}):
        super().__init__(screen = screen, visible = visible, color = color)

    def setBulletPattern(self, **kwargs):
        self.count = kwargs["count"] if "count" in kwargs else 10
        super.__init__(**kwargs)

    def trigger(self):
        if not self.endOfLife:
            self.spawnCounter = 0
            for i in range(self.count):
                self._createBullet()
        else:
            raise Warning("This pattern is waiting for removal, will not spawn bullets")
