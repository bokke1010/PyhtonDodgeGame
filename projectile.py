from base import *

class bulletSpawner():
    def __init__(self, screen, spawningDelay: int = 90, preTime: int = 0, lifeTime: int = -1,
                 visible: bool = True, spawnerLT: int = -1, spawning: bool = True):
        self.scr = screen
        # Spawning timing variables
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.delay = spawningDelay # Delay in ms between created bullets
        self.time = 0 # Time since this object is created in seconds
        # locally referencing all bullets
        self.bullets = []
        # Activation times
        self.preTime = preTime #Passing down the bullet fuse
        self.lifeTime = lifeTime
        self.spawning = spawning
        self.delete = False
        # Cosmetic
        self.spawningStyle = SPAWNINGSTYLE.NONE
        self.bulletVisible = visible

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
    def setSpawningExpBexp(self, coords: tuple, bulletPattern: (str, str), size: str, borderWidth: str):
        self.spawningStyle = SPAWNINGSTYLE.EXPBEXP
        if self.lifeTime == -1:
            raise Exception("Expression bullets must have a maximum lifetime")

        (self.x, self.y) = coords
        # Keep in mind that using a bulletexpression (BEXP) means dx and dy are strings instead of numbers
        (self.dx, self.dy) = bulletPattern
        self.size = size
        self.bulletBorderWidth = borderWidth

    def setSpawningBexpAbs(self, coords: (str,str), size: str, borderWidth: str):
        self.spawningStyle = SPAWNINGSTYLE.BEXPABS
        if self.lifeTime == -1:
            raise Exception("Expression bullets must have a maximum lifetime")
        (self.x, self.y) = coords
        self.size = size
        self.bulletBorderWidth = borderWidth

    def draw(self):
        if self.bulletVisible:
            for blt in self.bullets:
                blt.draw(self.scr)

    def update(self, dt, player):
        self.time += dt*1000 # We get dt in seconds for simulation purposes
        if self.spawning:
            # Bullet creation
            while (self.time - self.spawnCounter * self.delay) >= self.delay:
                # Determining the ball size

                bullet = Bullet(color = PINK, preTime = self.preTime, lifeTime = self.lifeTime)

                if self.spawningStyle == SPAWNINGSTYLE.NONE:
                    raise Exception("Spawning style not set")

                elif self.spawningStyle == SPAWNINGSTYLE.BOX:
                    x = random.randint(self.xMin, self.xMax)
                    y = random.randint(self.yMin, self.yMax)
                    dx = randomBetween(self.dxMin, self.dxMax)
                    dy = randomBetween(self.dyMin, self.dyMax)
                    size = randomBetween(self.minSize, self.maxSize)
                    borderWidth = self.bulletBorderWidth
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

                elif self.spawningStyle == SPAWNINGSTYLE.EXP:
                    t = self.time/1000
                    c = self.spawnCounter
                    x, y = eval(self.x), eval(self.y)
                    dx, dy = eval(self.dx), eval(self.dy)
                    size = eval(self.size)
                    borderWidth = eval(self.bulletBorderWidth)
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

                elif self.spawningStyle == SPAWNINGSTYLE.POINT:
                    x, y = self.x, self.y
                    speed = randomBetween(self.speedMin, self.speedMax)
                    angle = randomBetween(self.angleMin, self.angleMax)
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    size = randomBetween(self.minSize, self.maxSize)
                    borderWidth = self.bulletBorderWidth
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

                elif self.spawningStyle == SPAWNINGSTYLE.POINTEXP:
                    t = self.time / 1000
                    c = self.spawnCounter
                    x, y = eval(self.x), eval(self.y)
                    speed = eval(self.speed)
                    angle = eval(self.angle)
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    size = eval(self.size)
                    borderWidth = eval(self.bulletBorderWidth)
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy), size = size, borderWidth = borderWidth)

                elif self.spawningStyle == SPAWNINGSTYLE.EXPBEXP:
                    t = self.time / 1000
                    c = self.spawnCounter
                    x, y = eval(self.x), eval(self.y)
                    dx, dy = self.dx, self.dy
                    size = self.size
                    borderWidth = self.bulletBorderWidth
                    bullet.setBulletPatternExpRel(pos = (x, y), vel = (dx, dy), count= self.spawnCounter, size = size, borderWidth = borderWidth)

                elif self.spawningStyle == SPAWNINGSTYLE.BEXPABS:
                    t = self.time / 1000
                    c = self.spawnCounter
                    x, y = self.x, self.y
                    size = self.size
                    borderWidth = self.bulletBorderWidth
                    bullet.setBulletPatternExpAbs(pos = (x, y), count= self.spawnCounter, size = size, borderWidth = borderWidth)


                self.bullets.append(bullet)
                self.spawnCounter += 1

        # Bullet update
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
            if blt.movementMode == BULLETPATTERN.LINE:
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

    def deleteSpawner(self):
        self.spawning = False
        self.delete = True
        return len(self.bullets) == 0


class Bullet():
    def __init__(self, color: tuple = PINK, preTime: int = 0, active: bool = True, lifeTime: int = -1):
        # Pattern related
        self.movementMode = BULLETPATTERN.NONE

        # Style related
        self.color = color
        self.style = PROJECTILETYPE.BALL
        self.fadedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)

        # Activity related
        self.active = active
        self.time = 0 # Time since creation
        self.preTime = preTime
        self.lifeTime = lifeTime

    def setBulletPatternLine(self, pos: (int, int), vel: (int, int), size: int = 12, borderWidth: int = 3):
        self.movementMode = BULLETPATTERN.LINE
        (self.x, self.y) = pos
        (self.dx, self.dy) = vel
        self.size = size
        self.borderWidth = borderWidth

    def setBulletPatternExpRel(self, pos: (int, int), vel: (str, str), count: int = 0, size: str = "12", borderWidth: str = "3"):
        self.movementMode = BULLETPATTERN.EXPREL
        (self.x, self.y) = pos
        (self.dx, self.dy) = vel
        self.count = count
        self.sizeExp = size
        self.borderWidthExp = borderWidth

    def setBulletPatternExpAbs(self, pos: (str, str), count: int = 0, size: str = "12", borderWidth: str = "3"):
        self.movementMode = BULLETPATTERN.EXPABS
        (self.gx, self.gy) = pos
        self.count = count
        self.sizeExp = size
        self.borderWidthExp = borderWidth

    def draw(self, scr):
        # Draw either active projectile, used projectile or yet unactivated projectile
        if self.active and self.time >= self.preTime:
            self.__drawSelf__(scr, self.color)
        elif not self.active and self.time >= self.preTime:
            self.__drawSelf__(scr, self.fadedColor)
        elif self.time < self.preTime:
            self.__drawSelf__(scr, WHITE)

    def __drawSelf__(self, scr, color):
        pos = (int(self.x), int(self.y))
        if not hasattr(self, 'size'):
            raise Exception("""This projectile has a expression size which hasn't been calculated yet,
             make sure it's update function was called.""")
        innerSize = int(self.size-0.5 * self.borderWidth)# prevent the border from exceeding the circle
        pygame.draw.circle(scr, color, pos, innerSize, self.borderWidth)

    def update(self, dt, player):
        # Movement
        self.time += dt
        if self.movementMode == BULLETPATTERN.LINE:
            self.x += self.dx * dt
            self.y += self.dy * dt

        elif self.movementMode == BULLETPATTERN.EXPREL:
            c = self.count
            t = self.time
            x, y = self.x, self.y
            px, py = player.x, player.y
            self.x += eval(self.dx) * dt
            self.y += eval(self.dy) * dt
            self.size = eval(self.sizeExp)
            self.borderWidth = eval(self.borderWidthExp)

        elif self.movementMode == BULLETPATTERN.EXPABS:
            c = self.count
            t = self.time
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
