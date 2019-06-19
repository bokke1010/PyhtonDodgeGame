from base import *

class bulletSpawner():
    def __init__(self, screen, spawningDelay: int = 90, minSize: int = 16, maxSize: int = 0, safeTime: int = 0):
        self.spawnCounter = 0 # Amount of bullets this spawner has created in its lifetime
        self.delay = spawningDelay # Delay in ms between created bullets
        self.time = 0 # Time since this object is created in seconds
        self.bullets = [] # locally referencing all bullets
        self.safeTime = safeTime #Passing down the bullet fuse
        self.spawningStyle = SPAWNINGSTYLE.NONE
        self.minSize = minSize
        if maxSize == 0:
            self.maxSize = self.minSize
        else:
            self.maxSize = maxSize
        self.scr = screen

    def setSpawningBox(self, spawningArea: list, spawningVels: list ):
        self.spawningStyle = SPAWNINGSTYLE.BOX
        # Defining the spawning area as a box with x1y1 - x2y2
        self.spawnXMin = spawningArea[0]
        self.spawnYMin = spawningArea[1]
        self.spawnXMax = spawningArea[2]
        self.spawnYMax = spawningArea[3]
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        self.velXMin = spawningVels[0]
        self.velYMin = spawningVels[1]
        self.velXMax = spawningVels[2]
        self.velYMax = spawningVels[3]

    def setSpawningPoint(self, coords: list, dir: list, speed: list ):
        self.spawningStyle = SPAWNINGSTYLE.POINT
        # Defining the spawning point
        self.x = coords[0]
        self.y = coords[1]
        # Getting the allowed angles
        self.angleMin = dir[0]
        self.angleMax = dir[1]
        # Defining the base velocity of projectiles with a minimum and maximumvalue for both x and y
        self.speedMin = speed[0]
        self.speedMax = speed[1]

    def draw(self):
        for blt in self.bullets:
            blt.draw(self.scr)

    def update(self, dt, player):
        self.time += dt*1000 # We get dt in seconds for simulation purposes
        # Bullet creation
        while (self.time - self.spawnCounter * self.delay) >= self.delay:
            x, y, dx, dy = 0, 0, 0, 0
            bs = random.randint(self.minSize, self.maxSize)
            if self.spawningStyle == SPAWNINGSTYLE.NONE:
                raise Exception("Spawning style not set")
            elif self.spawningStyle == SPAWNINGSTYLE.BOX:
                x = random.randint(self.spawnXMin, self.spawnXMax)
                y = random.randint(self.spawnYMin, self.spawnYMax)
                dx = random.randint(self.velXMin, self.velXMax)
                dy = random.randint(self.velYMin, self.velYMax)
            elif self.spawningStyle == SPAWNINGSTYLE.POINT:
                x, y = self.x, self.y
                speed = random.randint(self.speedMin, self.speedMax)
                angle = math.pi * random.randint(self.angleMin, self.angleMax) / 180
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
            self.bullets.append(Bullet((x, y), (dx, dy), PINK, bs, 5, self.safeTime))
            self.spawnCounter += 1
        # Bullet update
        cleanupQue = set()
        for blt in self.bullets:
            # Updating individual bullets
            blt.update(dt, player)

            # Bullet cleanup (out of bounds & movement check)
            if blt.dx == 0 and blt.dy == 0:
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

        for item in cleanupQue:
            self.bullets.remove(item)


class Bullet():
    def __init__(self, pos: (int, int), vel: (int,int), color: tuple = PINK, size: int = 12, bdw: int = 2, actTime: int = 0, active: bool = True):
        self.x = pos[0]
        self.y = pos[1]
        self.dx = vel[0]
        self.dy = vel[1]
        self.color = color
        self.style = PROJECTILETYPE.BALL
        self.fadedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
        self.size = size # projectile size
        self.bdw = bdw # Border width
        self.active = active
        self.time = 0 # Time since creation
        self.actTime = actTime

    def draw(self, scr):
        pos = (int(self.x), int(self.y))
        innerSize = int(self.size-0.5 * self.bdw)# prevent the border from exceeding the circle
        if self.active and self.time >= self.actTime:
            pygame.draw.circle(scr, self.color, pos, innerSize, self.bdw)
        elif not self.active:
            pygame.draw.circle(scr, self.fadedColor, pos, innerSize, self.bdw)
        else:
            pygame.draw.circle(scr, WHITE, pos, innerSize, self.bdw)
    def update(self, dt, player):
        # Movement
        self.time += dt
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Player collision
        if(distance((self.x, self.y), player.sPos()) < self.size + player.size) and self.active and self.time >= self.actTime:
            # print("collision: (" + str(self.x) + ", " + str(self.y) + ") and " + str(pl.sPos()) + ".")
            player.lives -= 1
            self.active = False
