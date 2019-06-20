import projectile, fun_patterns, menu
from base import *

# All initialization

pygame.init()

gameState = None

def gameStateActive():
    global gameState
    if not gameState == GAMESTATE.ACTIVE:
        gameState = GAMESTATE.ACTIVE
        deactivateUIElement(UI, UIElements["Resume"])
        deactivateUIElement(UI, UIElements["Title"])
        deactivateUIElement(UI, UIElements["Exit"])


def gameStateMenu():
    global gameState
    if not gameState == GAMESTATE.MMENU:
        gameState = GAMESTATE.MMENU
        activateUIElement(UI, UIElements["Resume"])
        activateUIElement(UI, UIElements["Title"])
        activateUIElement(UI, UIElements["Exit"])

def stopMainLoop():
    global done
    done = True

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
            stopMainLoop()
    def sPos(self):
        return (int(self.x),int(self.y))

player = Player(playerSize, [w/2, h-playerSize], WHITE, acceleration, drag, 64)

UIElements = {}
UIElements["Resume"] = menu.Button(screen=screen, coords = (w/10,3*h/10,8*w/10,h/10), text = "resume", result="gameStateActive()")
UIElements["Exit"] = menu.Button(screen=screen, coords = (w/10,5*h/10,8*w/10,h/10), text = "exit", result="stopMainLoop()")
UIElements["Title"] = menu.Text(screen=screen, coords = (w/10,h/10,8*w/10,h/10), text = "Game Title")
UI = []

# fun_patterns.pattern_fast_spin(screen)
fun_patterns.pattern_sudden(screen, 0.1)
fun_patterns.pattern_dual_central_spiral(screen)
# fun_patterns.pattern_dodgeball(screen)
# p1 = projectile.bulletSpawner(screen=screen, spawningDelay=120, minSize=8)
# p1.setSpawningPointExpBexp(coords=("w/2", "0"), bulletPattern = ("400*math.cos(t*math.pi)","20"))
# fun_patterns.add_pattern(p1)

# Initialization done, loading gameState
gameStateMenu()

# Starting game loop
while not done:
    # Event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopMainLoop()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for UIElement in UI:
                if type(UIElement == 'menu.Button'):
                    res = UIElement.getClick(pos)
                    if not res == None:
                        eval(res)
        if event.type == pygame.KEYDOWN:
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
                    gameStateActive()
                if event.key == 27: # Esc. key
                    stopMainLoop()
            if gameState == GAMESTATE.ACTIVE: # All game keyEvents
                if event.key == 276: # Left arrow
                    gameStateMenu()
                if event.key == 27: # Esc. key
                    gameStateMenu()
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

        fun_patterns.updateDraw(dt, player)


    elif gameState == GAMESTATE.MMENU:
        clock.tick(20)
        screen.fill(DARKGRAY)
        fun_patterns.draw()
        player.draw(screen)

    # UI layer
    # UI uses a seperate system from object drawing.
    # it is created and rendered last and not affected by gamestate
    for UIElement in UI:
        UIElement.draw()

    pygame.display.flip()
pygame.quit()
