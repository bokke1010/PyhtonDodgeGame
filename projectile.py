from base import *

class bulletSpawner():
    def __init__(self, screen, spawningDelay: int = 90, minSize: int = 16,
                 maxSize: int = 0, preTime: int = 0, lifeTime: int = -1,
                 borderWidth: int = 3, visible: bool = True, spawnerLT = -1):
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
        # Cosmetic
        self.spawningStyle = SPAWNINGSTYLE.NONE
        self.bulletBorderWidth = borderWidth
        self.bulletVisible = visible
        self.spawnerLT = spawnerLT

        self.minSize = minSize
        if maxSize == 0:
            self.maxSize = self.minSize
        else:
            self.maxSize = maxSize

    def setSpawningBox(self, spawningArea: tuple, spawningVels: tuple ):
        self.spawningStyle = SPAWNINGSTYLE.BOX
        # Defining the spawning area as a box with x1y1 - x2y2
        (self.xMin, self.yMin, self.xMax, self.yMax) = spawningArea
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        (self.dxMin, self.dyMin, self.dxMax, self.dyMax) = spawningVels

    def setSpawningExp(self, coords: tuple, spawningVels: tuple ):
        self.spawningStyle = SPAWNINGSTYLE.EXP
        t = 0
        # Defining the spawning area as a point with (x,y)
        (self.x, self.y) = coords
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        # If randomness is wanted in a expression-function, it can be implemented manually
        (self.dx, self.dy) = spawningVels

    def setSpawningPoint(self, coords: tuple, dir: tuple, speed: tuple ):
        self.spawningStyle = SPAWNINGSTYLE.POINT
        # Defining the spawning point
        (self.x, self.y) = coords
        # Getting the allowed angles
        (self.angleMin, self.angleMax) = dir
        # Defining the base velocity of projectiles with a minimum and maximum
        (self.speedMin, self.speedMax) = speed

    def setSpawningPointExp(self, coords: tuple, dir: str, speed: str ):
        self.spawningStyle = SPAWNINGSTYLE.POINTEXP
        # Defining the spawning point
        (self.x, self.y) = coords
        # Getting the allowed angle formula
        self.angle = dir
        # Defining the base velocity of the projectile
        self.speed = speed

    # Has both Exp and Bexp in the name to signify that both the spawn point
    # and the bullet pattern behave according to a mathematical expression
    def setSpawningExpBexp(self, coords: tuple, bulletPattern: (str, str) = None):
        self.spawningStyle = SPAWNINGSTYLE.EXPBEXP
        if self.lifeTime == -1:
            raise Exception("Expression bullets must have a maximum lifetime")

        (self.x, self.y) = coords
        # Keep in mind that using a bulletexpression (BEXP) means dx and dy are strings instead of numbers
        (self.dx, self.dy) = bulletPattern

    def setSpawningBexpAbs(self, coords: (str,str)):
        self.spawningStyle = SPAWNINGSTYLE.BEXPABS
        if self.lifeTime == -1:
            raise Exception("Expression bullets must have a maximum lifetime")
        (self.x, self.y) = coords

    def draw(self):
        if self.bulletVisible:
            for blt in self.bullets:
                blt.draw(self.scr)

    def update(self, dt, player):
        self.time += dt*1000 # We get dt in seconds for simulation purposes
        self.spawning = True
        if (not self.spawnerLT == -1) and self.time > self.spawnerLT:
            self.spawning = False
        if self.spawning:
            # Bullet creation
            while (self.time - self.spawnCounter * self.delay) >= self.delay:

                x, y, dx, dy = 0, 0, 0, 0
                # Determining the ball size
                ballSize = 0
                if self.minSize == self.maxSize:
                    ballSize = self.minSize
                else:
                    ballSize = random.randint(self.minSize, self.maxSize)

                bullet = Bullet(color = PINK, size = ballSize, preTime = self.preTime, lifeTime = self.lifeTime, borderWidth = self.bulletBorderWidth)

                if self.spawningStyle == SPAWNINGSTYLE.NONE:
                    raise Exception("Spawning style not set")

                elif self.spawningStyle == SPAWNINGSTYLE.BOX:
                    x = random.randint(self.xMin, self.xMax)
                    y = random.randint(self.yMin, self.yMax)
                    dx = randomBetween(self.dxMin, self.dxMax)
                    dy = randomBetween(self.dyMin, self.dyMax)
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy))

                elif self.spawningStyle == SPAWNINGSTYLE.EXP:
                    t = self.time/1000
                    c = self.spawnCounter
                    x, y = eval(self.x), eval(self.y)
                    dx, dy = eval(self.dx), eval(self.dy)
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy))

                elif self.spawningStyle == SPAWNINGSTYLE.POINT:
                    x, y = self.x, self.y
                    speed = randomBetween(self.speedMin, self.speedMax)
                    angle = randomBetween(self.angleMin, self.angleMax)
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy))

                elif self.spawningStyle == SPAWNINGSTYLE.POINTEXP:
                    t = self.time / 1000
                    c = self.spawnCounter
                    x, y = eval(self.x), eval(self.y)
                    speed = eval(self.speed)
                    angle = eval(self.angle)
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    bullet.setBulletPatternLine(pos= (x,y), vel = (dx,dy))

                elif self.spawningStyle == SPAWNINGSTYLE.EXPBEXP:
                    t = self.time / 1000
                    c = self.spawnCounter
                    x, y = eval(self.x), eval(self.y)
                    dx, dy = self.dx, self.dy
                    bullet.setBulletPatternExpRel(pos = (x, y), vel = (dx, dy))

                elif self.spawningStyle == SPAWNINGSTYLE.BEXPABS:
                    t = self.time / 1000
                    c = self.spawnCounter
                    x, y = self.x, self.y
                    bullet.setBulletPatternExpAbs(pos = (x, y), count= self.spawnCounter)


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


class Bullet():
    def __init__(self, color: tuple = PINK, size: int = 12, borderWidth: int = 2, preTime: int = 0, active: bool = True, lifeTime: int = -1):
        # Pattern related
        self.size = size
        self.movementMode = BULLETPATTERN.NONE

        # Style related
        self.color = color
        self.style = PROJECTILETYPE.BALL
        self.fadedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
        self.borderWidth = borderWidth # Border width

        # Activity related
        self.active = active
        self.time = 0 # Time since creation
        self.preTime = preTime
        self.lifeTime = lifeTime

    def setBulletPatternLine(self, pos: (int, int), vel: (int, int)):
        self.movementMode = BULLETPATTERN.LINE
        (self.x, self.y) = pos
        (self.dx, self.dy) = vel

    def setBulletPatternExpRel(self, pos: (int, int), vel: (str, str)):
        self.movementMode = BULLETPATTERN.EXPREL
        (self.x, self.y) = pos
        (self.dx, self.dy) = vel

    def setBulletPatternExpAbs(self, pos: (str, str), count: int = 0):
        self.movementMode = BULLETPATTERN.EXPABS
        (self.gx, self.gy) = pos
        self.count = count

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
        innerSize = int(self.size-0.5 * self.borderWidth)# prevent the border from exceeding the circle
        pygame.draw.circle(scr, color, pos, innerSize, self.borderWidth)

    def update(self, dt, player):
        # Movement
        self.time += dt
        if self.movementMode == BULLETPATTERN.LINE:
            self.x += self.dx * dt
            self.y += self.dy * dt

        elif self.movementMode == BULLETPATTERN.EXPREL:
            t = self.time
            x, y = self.x, self.y
            px, py = player.x, player.y
            self.x += eval(self.dx) * dt
            self.y += eval(self.dy) * dt

        elif self.movementMode == BULLETPATTERN.EXPABS:
            c = self.count
            t = self.time
            self.x = eval(self.gx)
            self.y = eval(self.gy)

        # Player collision
        collision = distance((self.x, self.y), player.sPos()) < self.size + player.size
        active = self.active and self.time >= self.preTime
        if collision and active:
            player.hit(1)
            self.active = False
