from base import *
import numexpr as ne
import numpy

# TODO: Mayor cleanup and refactor
# use numexpr high efficientcy array-operations for large performance improvements

class BulletManager():
    def __init__(self, screen: pygame.display, visible: bool = True, preTime: int = 0, lifeTime: int = 1, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}, size: str = "6", borderWidth: str = "1", x:str = "c", y:str = "t"):
        self.scr = screen
        self.visible = visible
        self.endOfLife = False # Managers with this set to true wil be removed as soon as all of their bullets are gone
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.time = 0 # Time since this object is created in seconds

        self.size = size
        self.borderWidth = borderWidth

        self.GX = x
        self.GY = y

        self.preTime = preTime #Passing down the bullet fuse
        self.lifeTime = lifeTime
        if self.lifeTime == -1:
            raise Exception("bullets must have a maximum lifetime")

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
            tmp = ne.evaluate(self.borderWidth)
            try:
                iter(tmp)
            except TypeError:
                tmp = [tmp] * len(self.bulletIndex)
            borderWidth = list(tmp)
            for i, item in enumerate(zip(self.bulletX, self.bulletY)):
                color = self.colorActive
                if not self.bulletActive[i]:
                    color = self.colorFaded
                if self.bulletTime[i] < self.preTime:
                    color = self.colorInactive
                self._drawBullet(item, self.bulletSize[i], borderWidth[i], color)

    def _drawBullet(self, coords, size, borderWidth, color):
        pos = (int(coords[0]), int(coords[1]))
        innerSize = int(size-0.5 * borderWidth)# prevent the border from exceeding the circle
        pygame.draw.circle(self.scr, color, pos, innerSize, borderWidth)


    def update(self, dt, player):
        self.time += dt
        cleanupQue = set()
        (px, py) = player.sPos()
        x, y = self.bulletX, self.bulletY
        tb = self.bulletTime
        tt = dt
        tb = list(ne.evaluate("tt+tb"))
        t = list(ne.evaluate("0.001*tb"))
        c = self.bulletIndex
        # ALL BULLET CALCULATIONS HERE

        self.bulletX = list(ne.evaluate(self.GX))
        self.bulletY = list(ne.evaluate(self.GY))
        tmp = ne.evaluate(self.size)
        try:
            iter(tmp)
        except TypeError:
            tmp = [tmp] * len(self.bulletIndex)
        self.bulletSize = list(tmp)


        for i, bi in enumerate(self.bulletIndex):
            pos = (self.bulletX[i], self.bulletY[i])
            a = self.bulletActive[i] and self.bulletTime[i] > self.preTime
            if distanceLess(pos, player.sPos(), self.bulletSize[i]+player.size) and a:
                player.hit(1)
                self.bulletActive[i] = False
            # Bullet cleanup (out of bounds & movement check)
            # Bullets that exceed their lifetime get cleansed
            if self.bulletTime[i] > self.lifeTime:
                cleanupQue.add(i)

        # Got our list, now we just need to remove the bullets
        # TODO: remove the bullets
        for index in cleanupQue:
            print("Bullet at index " + str(index) + " must be removed")


    def setDelete(self):
        self.endOfLife = True
        # While the endOfLife check in getdelete is obsolete, this way of checking
        # is easier to understand and change
        return self.getDelete()

    def getDelete(self):
        return self.endOfLife and len(self.bulletIndex) == 0

class BulletSpawner(BulletManager):
    def __init__(self, screen, spawningDelay: int = 90, preTime: int = 0, lifeTime: int = -1, visible: bool = True, color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}, size: str = "6", borderWidth: str = "1", x:str = "c", y:str = "t"):
        super().__init__(screen=screen, visible = visible, preTime = preTime, lifeTime = lifeTime, color = color, size = size, borderWidth = borderWidth, x = x, y = y)
        # Spawning timing variables
        self.delay = spawningDelay # Delay in ms between created bullets

    def update(self, dt, player):
        # Bullet creation
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
    def __init__(self, screen, visible: bool = True, patternSize: int = 10, preTime: int = 0, lifeTime: int = -1,  color: dict = {"active":PINK, "inactive":LIGHTGRAY, "faded":DARKGRAY}, size: str = "6", borderWidth: str = "1", x:str = "c", y:str = "t"):

        super().__init__(screen = screen, visible = visible, color = color, size = size, borderWidth = borderWidth, x = x, y = y)
        self.spawningPattern = PATTERNSTYLE.NONE
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


#
#
# class Bullet():
#     def __init__(self, screen, color: tuple = PINK, preTime: int = 0, active: bool = True, lifeTime: int = -1, timeStart: int = 0):
#         # Pattern related
#         self.movementMode = BULLETPATH.NONE
#         self.scr = screen
#         # Style related
#         self.color = color
#         self.style = PROJECTILETYPE.BALL
#         self.fadedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
#
#         # Activity related
#         self.active = active
#         self.time = timeStart # Time since creation
#         self.preTime = preTime
#         self.lifeTime = lifeTime
#
#     def setBulletPathLine(self, pos: (int, int), vel: (int, int), size: int = 12, borderWidth: int = 3):
#         self.movementMode = BULLETPATH.LINE
#         (self.bx, self.by) = pos
#         self.x, self.y = self.bx, self.by
#         (self.dx, self.dy) = vel
#         self.size = size
#         self.borderWidth = borderWidth
#
#     def setBulletPathExpRel(self, pos: (int, int), vel: (str, str), count: int = 0, size: str = "12", borderWidth: str = "3", a: int = 0, b:int = 0):
#         self.movementMode = BULLETPATH.EXPREL
#         (self.x, self.y) = pos
#         (self.dx, self.dy) = vel
#         self.count = count
#         self.sizeExp = size
#         self.borderWidthExp = borderWidth
#         self.a, self.b = a, b
#         if self.lifeTime == -1:
#             raise Exception("This expression bullet has no set lifetime")
#
#     def setBulletPathExpAbs(self, pos: (str, str), count: int = 0, size: str = "12", borderWidth: str = "3", a: int = 1, b:int = 1):
#         self.movementMode = BULLETPATH.EXPABS
#         (self.gx, self.gy) = pos
#         self.count = count
#         self.sizeExp = size
#         self.borderWidthExp = borderWidth
#         self.a, self.b = a, b
#         if self.lifeTime == -1:
#             raise Exception("This expression bullet has no set lifetime")
#
#     def draw(self):
#         # Draw either active projectile, used projectile or yet unactivated projectile
#         if self.active and self.time >= self.preTime:
#             self._drawSelf(self.color)
#         elif not self.active and self.time >= self.preTime:
#             self._drawSelf(self.fadedColor)
#         elif self.time < self.preTime:
#             self._drawSelf(WHITE)
#
#     def _drawSelf(self, color):
#         # if not (hasattr(self, 'size') or hasattr(self, 'x')):
#         #     raise Exception("""This projectile has a expression which hasn't been calculated yet,
#         #     make sure it's update function was called.""")
#         pos = (int(self.x), int(self.y))
#         innerSize = int(self.size-0.5 * self.borderWidth)# prevent the border from exceeding the circle
#         pygame.draw.circle(self.scr, color, pos, innerSize, self.borderWidth)
#
#     def update(self, dt, player):
#         # Movement
#         self.time += dt
#         if self.movementMode == BULLETPATH.LINE:
#             self.x = self.bx + self.dx * self.time * 0.001
#             self.y = self.by + self.dy * self.time * 0.001
#
#         elif self.movementMode == BULLETPATH.EXPREL:
#             c = self.count
#             t = self.time * 0.001 # Expression clock in seconds
#             a, b = self.a, self.b
#             x, y = self.x, self.y
#             px, py = player.x, player.y
#             self.x += ne.evaluate(self.dx) * dt * 0.001
#             self.y += ne.evaluate(self.dy) * dt * 0.001
#             self.size = ne.evaluate(self.sizeExp)
#             self.borderWidth = ne.evaluate(self.borderWidthExp)
#
#         elif self.movementMode == BULLETPATH.EXPABS:
#             c = self.count
#             t = self.time * 0.001 # Expression clock in seconds
#             a, b = self.a, self.b
#             px, py = player.x, player.y
#             self.x = ne.evaluate(self.gx)
#             self.y = ne.evaluate(self.gy)
#             self.size = ne.evaluate(self.sizeExp)
#             self.borderWidth = ne.evaluate(self.borderWidthExp)
#
#         # Player collision
#         collision = distanceLess((self.x, self.y), player.sPos(), self.size + player.size)
#         active = self.active and self.time >= self.preTime
#         if collision and active:
#             player.hit(1)
#             self.active = False
