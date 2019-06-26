import projectile, pattern_manager, menu
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
        deactivateUIElement(UI, UIElements["spawnGuide"])

        deactivateUIElement(UI, UIElements["prev"])
        deactivateUIElement(UI, UIElements["startLevel"])
        deactivateUIElement(UI, UIElements["next"])


def gameStateMenu():
    global gameState
    if not gameState == GAMESTATE.MMENU:
        gameState = GAMESTATE.MMENU
        activateUIElement(UI, UIElements["Resume"])
        activateUIElement(UI, UIElements["Title"])
        activateUIElement(UI, UIElements["Exit"])
        activateUIElement(UI, UIElements["spawnGuide"])

        activateUIElement(UI, UIElements["prev"])
        activateUIElement(UI, UIElements["startLevel"])
        activateUIElement(UI, UIElements["next"])

def stopMainLoop():
    global done
    done = True

class Player():
    def __init__(self, size, pos, color, acc, drag, lives, scr):
        self.size = size
        (self.x, self.y) = pos
        self.dx, self.dy = 0, 0
        self.acc = acc
        self.drag = drag
        self.color = color
        self.lives = lives
        self.mLives = lives
        self.secCol = DARKGREEN
        self.scr =  scr

    def draw(self):
        # pygame.draw.circle(scr, self.color, self.sPos(), self.size)
        dPos = self.sPos()
        healthCS = self.size + 3
        rect = pygame.Rect(int(dPos[0]-healthCS),int(dPos[1]-healthCS),
            int(2*healthCS),int(2*healthCS))
        # Health bar
        pygame.draw.arc(self.scr, self.color, rect, 0, 2*math.pi*self.lives / self.mLives)
        # Collision marker
        pygame.draw.circle(self.scr, self.secCol, dPos, self.size)

    def update(self, xInp, yInp, dt):
        # air resistance as expected
        # self.dx += self.acc * xInp * dt
        # self.dx -= self.drag * abs(self.dx)**2 * ((self.dx > 0) - (self.dx < 0)) * dt
        # self.x += self.dx * dt
        #
        # self.dy += self.acc * yInp * dt
        # self.dy -= self.drag * abs(self.dy)**2 * ((self.dy > 0) - (self.dy < 0)) * dt
        # self.y += self.dy * dt

        # Game implementation
        # Maximum speed is 320px in each direction (160*2), so sqrt(320^2+320^2) = 453 total
        self.dx = self.acc * xInp
        # self.dx -= self.drag * abs(self.dx)**2 * ((self.dx > 0) - (self.dx < 0)) * dt
        self.x += self.dx * (2-keysDown['shift']) * dt * 0.001

        self.dy = self.acc * yInp
        # self.dy -= self.drag * abs(self.dy)**2 * ((self.dy > 0) - (self.dy < 0)) * dt
        self.y += self.dy * (2-keysDown['shift']) * dt * 0.001

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

    def hit(self, damage):
        self.lives -= damage

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

done = False

deltaTime = 0
time = 0

keysDown = {"w": False, "a":False, "s":False, "d":False, "shift":False}

player = Player(playerSize, [w/2, h-playerSize], WHITE, acceleration, drag, 64, screen)
patternManager = pattern_manager.PatternManager(screen)
levels = patternManager.loadJson("levels.json")
levelIndex = 0

# UI will eventually get a seperate system like the level system

def nextLevel():
    global levelIndex, levelCount
    levelIndex += 1
    if levelIndex > patternManager.levelCount-1:
        levelIndex = 0
    UIElements["startLevel"].updateText(levels[levelIndex])


def prevLevel():
    global levelIndex, levelCount
    levelIndex -= 1
    if levelIndex < 0:
        levelIndex = patternManager.levelCount-1
    UIElements["startLevel"].updateText(levels[levelIndex])



UIElements = {}
UIElements["Resume"] = menu.Button(screen=screen, coords = (w/10,3*h/10,8*w/10,h/10),
    text = "resume", result="gameStateActive()")
UIElements["Exit"] = menu.Button(screen=screen, coords = (w/10,5*h/10,8*w/10,h/10),
    text = "exit", result="stopMainLoop()")
UIElements["Title"] = menu.Text(screen=screen, coords = (w/10,h/10,8*w/10,h/10),
    text = "Game Title")
UIElements["spawnGuide"] = menu.Text(screen=screen, coords = (w/10,7*h/10,8*w/10,0.5*h/10),
    text = "Add patterns")

UIElements["prev"] = menu.Button(screen=screen, coords = (w/10,7.5*h/10,2*w/10,h/10),
    text = "<--", result="prevLevel()")
UIElements["startLevel"] = menu.Button(screen=screen, coords = (4*w/10,7.5*h/10,2*w/10,h/10),
    text = levels[levelIndex], result="patternManager.startLevel(levels[levelIndex])")
UIElements["next"] = menu.Button(screen=screen, coords = (7*w/10,7.5*h/10,2*w/10,h/10),
    text = "-->", result="nextLevel()")
UI = []


# Initialization done, loading gameState
gameStateMenu()

# Starting game loop
while not done:
    # Event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopMainLoop()
        # Evaluate menu items
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for UIElement in UI:
                # print(type(UIElement))
                if isinstance(UIElement, menu.Button):
                    res = UIElement.getClick(pos)
                    if not res == None:
                        eval(res)
                if isinstance(UIElement, menu.sButton):
                    res = UIElement.getClick(pos)
                    if not res == None:
                        (r, func) = res
                        eval(func)

        if event.type == pygame.KEYDOWN:
            # Directional keys
            if event.key == 119:
                keysDown['w'] = True
            if event.key == 97:
                keysDown['a'] = True
            if event.key == 115:
                keysDown['s'] = True
            if event.key == 100:
                keysDown['d'] = True

            if event.key == 304:
                keysDown['shift'] = True

            # Navigation keys
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

        # KeyUp events for directional keys
        if event.type == pygame.KEYUP:
            if event.key == 119: # W-key (event.unicode doesn't exist for KEYUP)
                keysDown['w'] = False
            if event.key == 97: # A-key
                keysDown['a'] = False
            if event.key == 115: # S-key
                keysDown['s'] = False
            if event.key == 100: # D-key
                keysDown['d'] = False

            if event.key == 304: # Shift-key
                keysDown['shift'] = False

    # Game active loop
    if gameState == GAMESTATE.ACTIVE:

        # Time and game clock management
        deltaTime = clock.tick(60)
        time += deltaTime # time and deltatime in milliseconds

        # Reset screen to start drawing frame
        screen.fill(BLACK)

        # Player code
        player.update((keysDown['d'] - keysDown['a']), (keysDown['s'] - keysDown['w']), deltaTime)
        player.draw()

        patternManager.update(deltaTime, player)
        patternManager.draw()


    elif gameState == GAMESTATE.MMENU:
        clock.tick(20)
        screen.fill(DARKGRAY)

        player.draw()
        patternManager.draw()

    # UI layer
    # UI uses a seperate system from object drawing.
    # it is created and rendered last and not affected by gamestate
    for UIElement in UI:
        UIElement.draw()

    pygame.display.flip()
pygame.quit()
