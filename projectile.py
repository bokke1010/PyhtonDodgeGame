from base import *

class BulletManager():
    def __init__(self, screen, visible: bool = True, preTime: int = 0, lifeTime: int = -1,):
        self.scr = screen
        self.visible = visible
        self.delete = False
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.time = 0 # Time since this object is created in seconds
        self.preTime = preTime #Passing down the bullet fuse
        self.lifeTime = lifeTime
        # locally referencing all bullets
        self.bullets = []

    def addBullet(self, bullet):
        self.bullets.append(bullet)

    def setSpawningBox(self, spawningArea: (int, int), spawningVels: (int, int), size: (int, int), borderWidth: int ):
        self.spawningStyle = SPAWNINGSTYLE.BOX
        # Defining the spawning area as a box with x1y1 - x2y2
        (self.xMin, self.yMin, self.xMax, self.yMax) = spawningArea
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        (self.dxMin, self.dyMin, self.dxMax, self.dyMax) = spawningVels
        (self.minSize, self.maxSize) = size
        self.bulletBorderWidth = borderWidth


    def setSpawningExp(self, coords: (str, str), spawningVels: (str, str), size: str, borderWidth: str ):
        self.spawningStyle = SPAWNINGSTYLE.EXP
        t = 0
        # Defining the spawning area as a point with (x,y)
        (self.x, self.y) = coords
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        # If randomness is wanted in a expression-function, it can be implemented manually
        (self.dx, self.dy) = spawningVels
        self.size = size
        self.bulletBorderWidth = borderWidth

    def setSpawningPoint(self, coords: (int, int), dir: (int, int), speed: (int, int), size: (int, int), borderWidth: int ):
        self.spawningStyle = SPAWNINGSTYLE.POINT
        # Defining the spawning point
        (self.x, self.y) = coords
        # Getting the allowed angles
        (self.angleMin, self.angleMax) = dir
        # Defining the base velocity of projectiles with a minimum and maximum
        (self.speedMin, self.speedMax) = speed
        (self.minSize, self.maxSize) = size
        self.bulletBorderWidth = borderWidth

    def setSpawningPointExp(self, coords: (int, int), dir: str, speed: str, size: str, borderWidth: str):
        self.spawningStyle = SPAWNINGSTYLE.POINTEXP
        # Defining the spawning point
        (self.x, self.y) = coords
        # Getting the allowed angle formula
        self.angle = dir
        # Defining the base velocity of the projectile
        self.speed = speed
        self.size = size
        self.bulletBorderWidth = borderWidth

    # A spawning style with Bexp in the name means that the bullet itself also evaluates expressions
    # These include bullet size, x, y, dx, dy etc.
    def setSpawningExpBexp(self, coords: tuple, bulletPath: (str, str), size: str, borderWidth: str):
        self.spawningStyle = SPAWNINGSTYLE.EXPBEXP
        if self.lifeTime == -1:
            raise Exception("Expression bullets must have a maximum lifetime")

        (self.x, self.y) = coords
        # Keep in mind that using a bulletexpression (BEXP) means dx and dy are strings instead of numbers
        (self.dx, self.dy) = bulletPath
        self.size = size
        self.bulletBorderWidth = borderWidth

    def setSpawningBexpAbs(self, coords: (str,str), size: str, borderWidth: str):
        self.spawningStyle = SPAWNINGSTYLE.BEXPABS
        if self.lifeTime == -1:
            raise Exception("Expression bullets must have a maximum lifetime")
        (self.x, self.y) = coords
        self.size = size
        self.bulletBorderWidth = borderWidth

    def _createBullet(self, time: int = -1, lateFraction: int = 0):
        """Internal function that uses internal variables to create a bullet (NOT FOR EXTERNAL USE)"""

        if time == -1:
            time = self.time
        bullet = Bullet(screen = self.scr, color = PINK, preTime = self.preTime, lifeTime = self.lifeTime)

        if self.spawningStyle == SPAWNINGSTYLE.NONE:
            raise Exception("Spawning style not set")

        elif self.spawningStyle == SPAWNINGSTYLE.BOX:
            dx = randomBetween(self.dxMin, self.dxMax)
            dy = randomBetween(self.dyMin, self.dyMax)
            x = random.randint(self.xMin, self.xMax) + lateFraction * dx
            y = random.randint(self.yMin, self.yMax) + lateFraction * dx
            size = randomBetween(self.minSize, self.maxSize)
            borderWidth = self.bulletBorderWidth
            bullet.setBulletPathLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

        elif self.spawningStyle == SPAWNINGSTYLE.EXP:
            t = time/1000
            c = self.spawnCounter
            x, y = eval(self.x), eval(self.y)
            dx, dy = eval(self.dx), eval(self.dy)
            size = eval(self.size)
            borderWidth = eval(self.bulletBorderWidth)
            bullet.setBulletPathLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

        elif self.spawningStyle == SPAWNINGSTYLE.POINT:
            speed = randomBetween(self.speedMin, self.speedMax)
            angle = randomBetween(self.angleMin, self.angleMax)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            x, y = self.x + dx*lateFraction, self.y + dy*lateFraction
            size = randomBetween(self.minSize, self.maxSize)
            borderWidth = self.bulletBorderWidth
            bullet.setBulletPathLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

        elif self.spawningStyle == SPAWNINGSTYLE.POINTEXP:
            t = time / 1000
            c = self.spawnCounter
            speed = eval(self.speed)
            angle = eval(self.angle)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            x, y = eval(self.x) + dx * lateFraction, eval(self.y) + dy * lateFraction
            size = eval(self.size)
            borderWidth = eval(self.bulletBorderWidth)
            bullet.setBulletPathLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

        elif self.spawningStyle == SPAWNINGSTYLE.EXPBEXP:
            t = time / 1000
            c = self.spawnCounter
            x, y = eval(self.x), eval(self.y)
            dx, dy = self.dx, self.dy
            size = self.size
            borderWidth = self.bulletBorderWidth
            bullet.setBulletPathExpRel(pos = (x, y), vel = (dx, dy), count= self.spawnCounter, size = size, borderWidth = borderWidth, timeStart = lateFraction)

        elif self.spawningStyle == SPAWNINGSTYLE.BEXPABS:
            x, y = self.x, self.y
            size = self.size
            borderWidth = self.bulletBorderWidth
            bullet.setBulletPathExpAbs(pos = (x, y), count= self.spawnCounter, size = size, borderWidth = borderWidth, timeStart = lateFraction)

        return bullet

    def draw(self):
        if self.visible:
            for blt in self.bullets:
                blt.draw()

    def update(self, dt, player):
        self.time += dt*1000 # We get dt in seconds for simulation purposes
        cleanupQue = set()
        for blt in self.bullets:
            # Updating individual bullets
            blt.update(dt, player)

            # Bullet cleanup (out of bounds & movement check)
            # Bullets that exceed their lifetime get cleansed
            if blt.time > blt.lifeTime and blt.lifeTime > 0:
                cleanupQue.add(blt)
            # Bullets that are guaranteed to never reenter the playfield get
            # deleted
            if blt.movementMode == BULLETPATH.LINE:
                # No bullet tumors
                if blt.dx == 0 and blt.dy == 0 and blt.lifeTime == -1:
                    cleanupQue.add(blt)
                if blt.dx > 0:
                    if blt.x > w:
                        cleanupQue.add(blt)
                elif blt.dx < 0:
                    if blt.x < 0:
                        cleanupQue.add(blt)
                if blt.dy > 0:
                    if blt.y > h:
                        cleanupQue.add(blt)
                elif blt.dy < 0:
                    if blt.y < 0:
                        cleanupQue.add(blt)

        # Got our list, now we're removing their references to let the garbage
        # collector do the rest
        # A better way of doing this might be needed in the future
        for item in cleanupQue:
            self.bullets.remove(item)

    def deleteManager(self):
        self.delete = True
        return len(self.bullets) == 0


class BulletSpawner(BulletManager):
    def __init__(self, screen, spawningDelay: int = 90, preTime: int = 0, lifeTime: int = -1,
                 visible: bool = True, spawning: bool = True):
        super().__init__(screen=screen, visible = visible, preTime = preTime, lifeTime = lifeTime)
        # Spawning timing variables
        self.delay = spawningDelay # Delay in ms between created bullets
        # Activation times

        self.spawning = spawning
        # Cosmetic
        self.spawningStyle = SPAWNINGSTYLE.NONE


    def update(self, dt, player):
        if self.spawning:
            # Bullet creation
            while (self.time - self.spawnCounter * self.delay) >= self.delay:
                time = (self.spawnCounter + 1) * self.delay
                # whatever reason I have for keeping time in milliseconds, it just doesn't work for lateFraction
                lateFraction = (self.time - time)/1000
                # Using a internal helper to create the bullet
                # This function is defined in bulletManager, and uses internal variables
                # That is the reason we don't pass many arguments
                bullet = self._createBullet(time, lateFraction)
                self.spawnCounter += 1

                self.bullets.append(bullet)
        super().update(dt, player)

    def deleteManager(self):
        self.spawning = False
        return super().deleteManager()

class BulletPattern(BulletManager):
    def __init__(self, screen, visible: bool = True, patternSize: int = 10, preTime: int = 0, lifeTime: int = -1):
        super().__init__(screen = screen, visible = visible)
        self.spawningPattern = PATTERNSTYLE.NONE
        self.patternSize = patternSize
        self.preTime = preTime
        self.lifeTime = lifeTime

    def trigger(self):
        if not self.delete:
            self.spawnCounter = 0
            for i in range(self.patternSize):
                bullet = self._createBullet()
                self.spawnCounter += 1
                self.bullets.append(bullet)
        else:
            raise Warning("This pattern is waiting for removal, will not spawn bullets")




class Bullet():
    def __init__(self, screen, color: tuple = PINK, preTime: int = 0, active: bool = True, lifeTime: int = -1):
        # Pattern related
        self.movementMode = BULLETPATH.NONE
        self.scr = screen
        # Style related
        self.color = color
        self.style = PROJECTILETYPE.BALL
        self.fadedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)

        # Activity related
        self.active = active
        self.time = 0 # Time since creation
        self.preTime = preTime
        self.lifeTime = lifeTime

    def setBulletPathLine(self, pos: (int, int), vel: (int, int), size: int = 12, borderWidth: int = 3):
        self.movementMode = BULLETPATH.LINE
        (self.x, self.y) = pos
        (self.dx, self.dy) = vel
        self.size = size
        self.borderWidth = borderWidth

    def setBulletPathExpRel(self, pos: (int, int), vel: (str, str), count: int = 0, size: str = "12", borderWidth: str = "3", timeStart: int = 0):
        self.movementMode = BULLETPATH.EXPREL
        (self.x, self.y) = pos
        (self.dx, self.dy) = vel
        self.count = count
        self.sizeExp = size
        self.borderWidthExp = borderWidth
        self.time = timeStart

    def setBulletPathExpAbs(self, pos: (str, str), count: int = 0, size: str = "12", borderWidth: str = "3", timeStart: int = 0):
        self.movementMode = BULLETPATH.EXPABS
        (self.gx, self.gy) = pos
        self.count = count
        self.sizeExp = size
        self.borderWidthExp = borderWidth
        self.time = timeStart

    def draw(self):
        # Draw either active projectile, used projectile or yet unactivated projectile
        if self.active and self.time >= self.preTime:
            self._drawSelf(self.color)
        elif not self.active and self.time >= self.preTime:
            self._drawSelf(self.fadedColor)
        elif self.time < self.preTime:
            self._drawSelf(WHITE)

    def _drawSelf(self, color):
        if not (hasattr(self, 'size') or hasattr(self, 'x')):
            raise Exception("""This projectile has a expression which hasn't been calculated yet,
            make sure it's update function was called.""")
        pos = (int(self.x), int(self.y))
        innerSize = int(self.size-0.5 * self.borderWidth)# prevent the border from exceeding the circle
        pygame.draw.circle(self.scr, color, pos, innerSize, self.borderWidth)

    def update(self, dt, player):
        # Movement
        self.time += dt
        if self.movementMode == BULLETPATH.LINE:
            self.x += self.dx * dt
            self.y += self.dy * dt

        elif self.movementMode == BULLETPATH.EXPREL:
            c = self.count
            t = self.time
            x, y = self.x, self.y
            px, py = player.x, player.y
            self.x += eval(self.dx) * dt
            self.y += eval(self.dy) * dt
            self.size = eval(self.sizeExp)
            self.borderWidth = eval(self.borderWidthExp)

        elif self.movementMode == BULLETPATH.EXPABS:
            c = self.count
            t = self.time
            px, py = player.x, player.y
            self.x = eval(self.gx)
            self.y = eval(self.gy)
            self.size = eval(self.sizeExp)
            self.borderWidth = eval(self.borderWidthExp)

        # Player collision
        collision = distance((self.x, self.y), player.sPos()) < self.size + player.size
        active = self.active and self.time >= self.preTime
        if collision and active:
            player.hit(1)
            self.active = False
