import pygame, random, math
from enum import Enum

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

class GAMESTATE(Enum):
    ACTIVE = 0
    MMENU = 1
gameState = GAMESTATE.ACTIVE

# Some default colors:
BLACK     = (0  ,0  ,0  )
DARKGRAY  = (63 ,63 ,63 )
GRAY      = (63 ,63 ,63 )
LIGHTGRAY = (63 ,63 ,63 )
WHITE     = (255,255,255)
PINK      = (153,9  ,153)
CYAN      = (0  ,192,192)
DARKGREEN = (31 ,127,31 )

done = False
bs = 8
deltaTime = 0
time = 0
hVel = 0
acceleration = 4000
drag = 0.6
keysDown = {"w": False, "a":False, "s":False, "d":False}

def distance(p1, p2):
    return (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**0.5

def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

bullets = []

class bulletSpawner():
    def __init__(self, spawningDelay: int, spawningArea, spawningVels, minSize, maxSize, safeTime = 0):
        self.spawnCounter = 0
        self.delay = spawningDelay
        self.time = 0
        self.bullets = []
        self.spawnXMin = spawningArea[0]
        self.spawnYMin = spawningArea[1]
        self.spawnXMax = spawningArea[2]
        self.spawnYMax = spawningArea[3]
        self.velXMin = spawningVels[0]
        self.velYMin = spawningVels[1]
        self.velXMax = spawningVels[2]
        self.velYMax = spawningVels[3]
        self.minSize = minSize
        self.maxSize = maxSize
        self.safeTime = safeTime

    def draw(self):
        for blt in self.bullets:
            blt.draw(screen)

    def update(self, dt):
        self.time += dt*1000 # We get dt in seconds for simulation purposes
        # Bullet creation
        while (self.time - self.spawnCounter * self.delay) >= self.delay:
            x = random.randint(self.spawnXMin, self.spawnXMax)
            y = random.randint(self.spawnYMin, self.spawnYMax)
            dx = random.randint(self.velXMin, self.velXMax)
            dy = random.randint(self.velYMin, self.velYMax)
            bs = random.randint(self.minSize, self.maxSize)
            self.bullets.append(Bullet((x, y), (dx, dy), PINK, bs, 5, self.safeTime))
            self.spawnCounter += 1
        # Bullet update
        cleanupQue = set()
        for blt in self.bullets:
            blt.update(player, dt)
            # Bullet cleanup (out of bounds & movement check)
            if blt.dx == 0 and blt.dy == 0:
                cleanupQue.add(blt)
            if blt.dx > 0:
                if blt.dy > 0:
                    if (blt.x > w or blt.y > h):
                        cleanupQue.add(blt)
                elif blt.dy < 0:
                    if (blt.x > w or blt.y < 0):
                        cleanupQue.add(blt)
            elif blt.dx < 0:
                if blt.dy > 0:
                    if (blt.x < 0 or blt.y > h):
                        cleanupQue.add(blt)
                elif blt.dy < 0:
                    if (blt.x < 0 or blt.y < 0):
                        cleanupQue.add(blt)

        for item in cleanupQue:
            self.bullets.remove(item)


class Bullet():
    def __init__(self, pos: (int, int), vel: (int,int), color: tuple, size: int, bdw: int, actTime = 0):
        self.x = pos[0]
        self.y = pos[1]
        self.dx = vel[0]
        self.dy = vel[1]
        self.color = color
        self.fadedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
        self.size = size
        self.bdw = bdw
        self.active = True
        self.time = 0
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
    def update(self, pl, dt):
        # Movement
        self.time += dt
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Player collision
        if(distance((self.x, self.y), pl.sPos()) < self.size + bs) and self.active and self.time >= self.actTime:
            # print("collision: (" + str(self.x) + ", " + str(self.y) + ") and " + str(pl.sPos()) + ".")
            pl.lives -= 1
            self.active = False

class Player():
    def __init__(self, size, pos, color, acc, drag, lives):
        self.size = size
        self.x = pos[0]
        self.y = pos[1]
        self.dx = 0
        self.dy = 0
        self.acc = acc
        self.drag = drag
        self.color = color
        self.lives = lives
        self.mLives = lives
        self.secCol = DARKGREEN

    def draw(self, scr):
        # pygame.draw.circle(scr, self.color, self.sPos(), self.size)
        dPos = self.sPos()
        healthCS = self.size + 3
        rect = pygame.Rect(int(dPos[0]-healthCS),int(dPos[1]-healthCS),int(2*healthCS),int(2*healthCS))
        # Health bar
        pygame.draw.arc(scr, self.color, rect, 0, 2*3.14*self.lives / self.mLives)
        # Collision marker
        pygame.draw.circle(scr, self.secCol, dPos, self.size)
    def update(self, xInp, yInp, dt):
        global done
        # air resistance as expected, not what I use
        self.dx += self.acc * xInp * dt
        self.dx -= self.drag * abs(self.dx)**1.5 * ((self.dx > 0) - (self.dx < 0)) * dt
        self.x += self.dx * dt
        self.dy += self.acc * yInp * dt
        self.dy -= self.drag * abs(self.dy)**1.5 * ((self.dy > 0) - (self.dy < 0)) * dt
        self.y += self.dy * dt

        # Prevent out-of-bounds character
        while self.x > w:
            self.x = w
            if self.dx > 0:
                self.dx = 0
        while self.x < 0:
            self.x = 0
            if self.dx < 0:
                self.dx = 0
        while self.y > h:
            self.y = h
            if self.dy > 0:
                self.dy = 0
        while self.y < 0:
            self.y = 0
            if self.dy < 0:
                self.dy = 0

        # End game when dead
        if self.lives <= 0:
            done = True
    def sPos(self):
        return (int(self.x),int(self.y))


player = Player(bs, [w/2, h-bs], WHITE, acceleration, drag, 32)
# sp1 = bulletSpawner(450, [-10,0,w+10, 0], [0, h/2, 0, h/2], 16, 32)
# sp2 = bulletSpawner(450, [-10,h,w+10, h], [0, -h/2, 0, -h/2], 16, 32)
sp1 = bulletSpawner(250, [0,0,w, h], [-10, -10, 10, 10], 10, 10, 0.5)

secondarySpawner = bulletSpawner(80, [0, h/2, 0, h/2], [3, 0, 3, 0], 8, 8)
while not done:

    # Event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 27: # Esc. key
                done = True
            if event.unicode == 'w':
                keysDown['w'] = True
            if event.unicode == 'a':
                keysDown['a'] = True
            if event.unicode == 's':
                keysDown['s'] = True
            if event.unicode == 'd':
                keysDown['d'] = True
            if gameState == GAMESTATE.MMENU: # All menu keyEvents
                if event.key == 275: # Right arrow
                    gameState = GAMESTATE.ACTIVE
            if gameState == GAMESTATE.ACTIVE: # All game keyEvents
                if event.key == 276: # Left arrow
                    gameState = GAMESTATE.MMENU
        if event.type == pygame.KEYUP:
            if event.key == 119: # W-key (event.unicode doesn't exist for KEYUP)
                keysDown['w'] = False
            if event.key == 97: # A-key
                keysDown['a'] = False
            if event.key == 115: # S-key
                keysDown['s'] = False
            if event.key == 100: # D-key
                keysDown['d'] = False

    # Game active loop
    if gameState == GAMESTATE.ACTIVE:

        # Time and game clock management
        deltaTime = clock.tick(60)
        time += deltaTime # time and deltatime in milliseconds
        dt = deltaTime/1000 # deltatime in seconds

        # Reset screen to start drawing frame
        screen.fill(BLACK)

        # Player code
        player.draw(screen)
        player.update((keysDown['d'] - keysDown['a']), (keysDown['s'] - keysDown['w']), dt)

        sp1.update(dt)
        sp1.draw()
        sp2.update(dt)
        sp2.draw()

        secondarySpawner.update(dt)
        secondarySpawner.draw()
        t = time/(280*math.pi)
        xp = int(0.5 * h * (1+math.cos(t)))
        yp = int(0.5 * w * (1+math.sin(t)))
        secondarySpawner.spawnYMin = xp
        secondarySpawner.spawnYMax = xp
        secondarySpawner.spawnXMin = yp
        secondarySpawner.spawnXMax = yp
        s = 180
        dirX = -int(s * (math.sin(t)))
        dirY = -int(s * (math.cos(t)))
        secondarySpawner.velXMin = dirX
        secondarySpawner.velXMax = dirX
        secondarySpawner.velYMin = dirY
        secondarySpawner.velYMax = dirY

    elif gameState == GAMESTATE.MMENU:
        clock.tick(20)
        screen.fill(DARKGRAY)
        sp1.draw()
        sp2.draw()
        secondarySpawner.draw()
        player.draw(screen)


    pygame.display.flip()
pygame.quit()
