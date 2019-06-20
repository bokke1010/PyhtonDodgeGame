from base import *

class bulletSpawner():
    def __init__(self, screen, spawningDelay: int = 90, minSize: int = 16,
                 maxSize: int = 0, preTime: int = 0, lifeTime: int = -1,
                 borderWidth: int = 3, visible: bool = True):
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.delay = spawningDelay # Delay in ms between created bullets
        self.time = 0 # Time since this object is created in seconds
        self.bullets = [] # locally referencing all bullets
        self.preTime = preTime #Passing down the bullet fuse
        self.lifeTime = lifeTime
        self.spawningStyle = SPAWNINGSTYLE.NONE
        self.bulletBorderWidth = borderWidth
        self.bulletVisible = visible
        self.minSize = minSize
        if maxSize == 0:
            self.maxSize = self.minSize
        else:
            self.maxSize = maxSize
        self.scr = screen

    def setSpawningBox(self, spawningArea: tuple, spawningVels: tuple ):
        self.spawningStyle = SPAWNINGSTYLE.BOX
        # Defining the spawning area as a box with x1y1 - x2y2
        self.xMin = spawningArea[0]
        self.yMin = spawningArea[1]
        self.xMax = spawningArea[2]
        self.yMax = spawningArea[3]
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        self.dxMin = spawningVels[0]
        self.dyMin = spawningVels[1]
        self.dxMax = spawningVels[2]
        self.dyMax = spawningVels[3]

    def setSpawningExp(self, coords: tuple, spawningVels: tuple ):
        self.spawningStyle = SPAWNINGSTYLE.EXP
        t = 0
        # Defining the spawning area as a box with x1y1 - x2y2
        self.x = coords[0]
        self.y = coords[1]
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        # If randomness is wanted in a expression-function, it can be implemented manually
        self.dx = spawningVels[0]
        self.dy = spawningVels[1]

    def setSpawningPoint(self, coords: tuple, dir: tuple, speed: tuple ):
        self.spawningStyle = SPAWNINGSTYLE.POINT
        # Defining the spawning point
        self.x = coords[0]
        self.y = coords[1]
        # Getting the allowed angles
        self.angleMin = dir[0]
        self.angleMax = dir[1]
        # Defining the base velocity of projectiles with a minimum and maximum
        self.speedMin = speed[0]
        self.speedMax = speed[1]

    def setSpawningPointExp(self, coords: tuple, dir: str, speed: str ):
        self.spawningStyle = SPAWNINGSTYLE.POINTEXP
        # Defining the spawning point
        self.x = coords[0]
        self.y = coords[1]
        # Getting the allowed angle formula
        self.angle = dir
        # Defining the base velocity of the projectile
        self.speed = speed

    # Has both Exp and Bexp in the name to signify that both the spawn point
    # and the bullet pattern behave according to a mathematical expression
    def setSpawningPointExpBexp(self, coords: tuple, bulletPattern: (str, str) = None):
        self.spawningStyle = SPAWNINGSTYLE.EXPBEXP
        (self.x, self.y) = coords
        (self.dx, self.dy) = bulletPattern

    def draw(self):
        if self.bulletVisible:
            for blt in self.bullets:
                blt.draw(self.scr)

    def update(self, dt, player):
        self.time += dt*1000 # We get dt in seconds for simulation purposes
        # Bullet creation
        while (self.time - self.spawnCounter * self.delay) >= self.delay:
            x, y, dx, dy = 0, 0, 0, 0
            ballSize = random.randint(self.minSize, self.maxSize)
            if self.spawningStyle == SPAWNINGSTYLE.NONE:
                raise Exception("Spawning style not set")

            elif self.spawningStyle == SPAWNINGSTYLE.BOX:
                x = random.randint(self.xMin, self.xMax)
                y = random.randint(self.yMin, self.yMax)
                dx = randomBetween(self.dxMin, self.dxMax)
                dy = randomBetween(self.dyMin, self.dyMax)

            elif self.spawningStyle == SPAWNINGSTYLE.EXP:
                t = self.time/1000
                c = self.spawnCounter
                x = eval(self.x)
                y = eval(self.y)
                dx = eval(self.dx)
                dy = eval(self.dy)

            elif self.spawningStyle == SPAWNINGSTYLE.POINT:
                x, y = self.x, self.y
                speed = randomBetween(self.speedMin, self.speedMax)
                angle = randomBetween(self.angleMin, self.angleMax)
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed

            elif self.spawningStyle == SPAWNINGSTYLE.POINTEXP:
                t = self.time / 1000
                c = self.spawnCounter
                x, y = eval(self.x), eval(self.y)
                speed = eval(self.speed)
                angle = eval(self.angle)
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed

            elif self.spawningStyle == SPAWNINGSTYLE.EXPBEXP:
                t = self.time / 1000
                c = self.spawnCounter
                x, y = eval(self.x), eval(self.y)
                dx, dy = self.dx, self.dy

            temp = Bullet(pos = (x, y), color = PINK, size = ballSize, preTime = self.preTime, lifeTime = self.lifeTime, borderWidth = self.bulletBorderWidth)

            # Set bullet as pattern or line type bullet
            if self.spawningStyle == SPAWNINGSTYLE.EXPBEXP:
                temp.setBulletPatternExpRel(vel = (dx, dy))
            else:
                temp.setBulletPatternLine(vel = (dx, dy))

            self.bullets.append(temp)
            self.spawnCounter += 1
        # Bullet update
        cleanupQue = set()
        for blt in self.bullets:
            # Updating individual bullets
            blt.update(dt, player)

            # Bullet cleanup (out of bounds & movement check)
            if blt.dx == 0 and blt.dy == 0 and blt.lifeTime == -1:
                cleanupQue.add(blt)
            if blt.time > blt.lifeTime and blt.lifeTime > 0:
                cleanupQue.add(blt)
            if not self.spawningStyle == SPAWNINGSTYLE.EXPBEXP:
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
            else:
                if not 0 <= blt.x <= w:
                    cleanupQue.add(blt)
                if not 0 <= blt.y <= h:
                    cleanupQue.add(blt)

        for item in cleanupQue:
            self.bullets.remove(item)


class Bullet():
    def __init__(self, pos: (int, int), color: tuple = PINK, size: int = 12, borderWidth: int = 2, preTime: int = 0, active: bool = True, lifeTime: int = -1):
        # Pattern related
        self.x = pos[0]
        self.y = pos[1]
        self.size = size # projectile size
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

    def setBulletPatternLine(self, vel: (int, int)):
        self.movementMode = BULLETPATTERN.LINE
        (self.dx, self.dy) = vel

    def setBulletPatternExpRel(self, vel: (str, str)):
        self.movementMode = BULLETPATTERN.EXPREL
        (self.dx, self.dy) = vel

    def setBulletPatternExpAbs(self, vel: (str, str)):
        self.movementMode = BULLETPATTERN.EXPABS
        (self.dx, self.dy) = vel

    def draw(self, scr):
        pos = (int(self.x), int(self.y))
        innerSize = int(self.size-0.5 * self.borderWidth)# prevent the border from exceeding the circle
        # Draw either active projectile, used projectile or yet unactivated projectile
        if self.active and self.time >= self.preTime:
            pygame.draw.circle(scr, self.color, pos, innerSize, self.borderWidth)
        elif not self.active:
            pygame.draw.circle(scr, self.fadedColor, pos, innerSize, self.borderWidth)
        else:
            pygame.draw.circle(scr, WHITE, pos, innerSize, self.borderWidth)

    def update(self, dt, player):
        # Movement
        self.time += dt
        if self.movementMode == BULLETPATTERN.LINE:
            self.x += self.dx * dt
            self.y += self.dy * dt

        elif self.movementMode == BULLETPATTERN.EXPREL:
            t = self.time
            x, y = self.x, self.y
            self.x += eval(self.dx) * dt
            self.y += eval(self.dy) * dt

        elif self.movementMode == BULLETPATTERN.EXPABS:
            t = self.time
            x, y = self.x, self.y
            self.x = eval(self.dx)
            self.y = eval(self.dy)

        # Player collision
        collision = distance((self.x, self.y), player.sPos()) < self.size + player.size
        active = self.active and self.time >= self.preTime
        if collision and active:
            player.lives -= 1
            self.active = False
