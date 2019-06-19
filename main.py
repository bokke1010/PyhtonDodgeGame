import projectile
from base import *
pygame.init()

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

done = False

deltaTime = 0
time = 0
keysDown = {"w": False, "a":False, "s":False, "d":False}


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
        pygame.draw.arc(scr, self.color, rect, 0, 2*math.pi*self.lives / self.mLives)
        # Collision marker
        pygame.draw.circle(scr, self.secCol, dPos, self.size)
    def update(self, xInp, yInp, dt):
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
            global done
            done = True
    def sPos(self):
        return (int(self.x),int(self.y))

player = Player(playerSize, [w/2, h/2], WHITE, acceleration, drag, 32)

spawner_main = projectile.bulletSpawner(screen=screen, spawningDelay=250, minSize=24, maxSize=32)
spawner_main.setSpawningBox(spawningArea=[0,0,w, 0], spawningVels=[-1, h/3, 1, h/2])

spawner_pattern = projectile.bulletSpawner(screen=screen, spawningDelay=20, minSize=8)
spawner_pattern.setSpawningPoint(coords=[w/2, h/2], dir=[0,0], speed=[180,180])
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

        spawner_main.update(dt, player)
        spawner_main.draw()

        spawner_pattern.update(dt, player)
        spawner_pattern.draw()

        # This all needs to be integrated into the spawner
        t = math.pi * (time/1000)
        direction = int((t + (1 * math.pi)) * 180 / math.pi)
        spawner_pattern.x = int(0.5 * w * (1+math.cos(t)))
        spawner_pattern.y = int(0.5 * h * (1+math.sin(t)))
        spawner_pattern.angleMin = direction
        spawner_pattern.angleMax = direction



    elif gameState == GAMESTATE.MMENU:
        clock.tick(20)
        screen.fill(DARKGRAY)
        spawner_main.draw()
        spawner_pattern.draw()
        player.draw(screen)


    pygame.display.flip()
pygame.quit()
