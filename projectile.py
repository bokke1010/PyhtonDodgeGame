from base import *
import numexpr as ne
# import numpy

class BulletManager():
    def __init__(self, screen: pygame.display, visible: bool = True, preTime: int = 0, lifeTime: int = 1000, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}, size: str = "6", x:str = "c", y:str = "t"):
        self.scr = screen
        self.visible = visible
        self.endOfLife = False # Managers with this set to true wil be removed as soon as all of their bullets are gone
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.time = 0 # Time since this object is created in seconds

        self.size = size

        self.GX = x
        self.GY = y

        self.damage = 1
        self.preTime = preTime #Passing down the bullet fuse
        self.lifeTime = lifeTime


        # Style related
        self.colorActive = color["active"]
        self.colorInactive = color["inactive"]
        self.colorFaded = color["faded"]

        # bullet information
        self.bulletIndex = []
        self.bulletX = []
        self.bulletY = []
        self.bulletSize = []
        self.bulletActive = []
        self.bulletTime = [] # Time since creation

    def _createBullet(self, time: int = -1, lateFraction: int = 0):
        """Internal function that uses internal variables to create a bullet (NOT FOR EXTERNAL USE)"""

        if time == -1:
            time = self.time

        self.bulletIndex.append(self.spawnCounter)

        self.bulletTime.append(lateFraction)
        self.bulletActive.append(not self.preTime == -1)

        self.bulletX.append(0)
        self.bulletY.append(0)
        self.bulletSize.append(0)

        self.spawnCounter += 1


    def draw(self):
        if self.visible:
            c = self.bulletIndex
            t = self.bulletTime
            for i, item in enumerate(zip(self.bulletX, self.bulletY)):
                color = self.colorActive
                if not self.bulletActive[i]:
                    color = self.colorFaded
                if self.bulletTime[i] < self.preTime:
                    color = self.colorInactive
                self._drawBullet(item, self.bulletSize[i], color)

    def _drawBullet(self, coords, size, color):
        pos = (int(coords[0]*w), int(coords[1]*h))
        pygame.draw.circle(self.scr, color, pos, int(size*w), 0)


    def update(self, dt, player):
        events = Que()
        self.time += dt
        cleanupQue = set()
        (px, py) = player.pos()
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
        bulletSize = ne.evaluate(self.size)
        try:
            bulletSize = list(bulletSize)
        except:
            bulletSize = [float(bulletSize)] * len(self.bulletIndex)
        self.bulletSize = bulletSize


        for i, bi in enumerate(self.bulletIndex):
            pos = (self.bulletX[i], self.bulletY[i])
            a = self.bulletActive[i] and self.bulletTime[i] > self.preTime

            # Collisions here
            if distanceLess(pos, player.pos(), self.bulletSize[i]+player.size) and a:
                events.add(Data("hit", damage=self.damage))
            # Bullets that exceed their lifetime get cleansed
            if self.bulletTime[i] > self.lifeTime:
                cleanupQue.add(i)

        # Got our list, now we just need to remove the bullets
        # TODO: clean up redundancy
        cleanupQue = list(cleanupQue)
        while len(cleanupQue) > 0:
            index = cleanupQue[-1]
            self.bulletIndex.pop(index)
            self.bulletX.pop(index)
            self.bulletY.pop(index)
            self.bulletSize.pop(index)
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
    def __init__(self, screen, spawningDelay: int = 90, preTime: int = 0, lifeTime: int = 1000, visible: bool = True, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}, size: str = "6", x:str = "c", y:str = "t"):
        super().__init__(screen=screen, visible = visible, preTime = preTime, lifeTime = lifeTime, color = color, size = size, x = x, y = y)
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
        super().update(dt, player)

    def setDelete(self):
        self.spawning = False
        return super().setDelete()

class BulletPattern(BulletManager):
    def __init__(self, screen, visible: bool = True, patternSize: int = 10, preTime: int = 0, lifeTime: int = -1,  color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}, size: str = "6", x:str = "c", y:str = "t"):

        super().__init__(screen = screen, visible = visible, color = color, size = size, x = x, y = y)
        self.patternSize = patternSize
        self.preTime = preTime
        self.lifeTime = lifeTime

    def trigger(self):
        if not self.endOfLife:
            self.spawnCounter = 0
            for i in range(self.patternSize):
                self._createBullet()
        else:
            raise Warning("This pattern is waiting for removal, will not spawn bullets")
