import projectile, pattern_manager, menu, keyEvents, player
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


screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

done = False

deltaTime = 0
time = 0

playerCharacter = player.Player(playerSize, [w/2, h-playerSize], WHITE, acceleration, drag, 600, screen)
patternManager = pattern_manager.PatternManager(screen)

levelIndex = 0
levels = patternManager.loadJson("levels.json")

keyDownFlags = {}
for key in keyCodes.values():
    keyDownFlags[key] = False
print(keyDownFlags)

def handleReturnData(data):
    for action in data:
        if action.type == "stop":
            stopMainLoop()
        elif action.type == "exec":
            r = action.variable
            eval(action.data)
        elif action.type == "gameState":
            if action.state == GAMESTATE.ACTIVE:
                gameStateActive()
            if action.state == GAMESTATE.MMENU:
                gameStateMenu()
        elif action.type == "keySet":
            keyDownFlags[action.key] = action.value

# UI needs it's own file/import, preferably another JSON file like the level system

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

eventManager = keyEvents.EventManager(UI)
# UI will eventually get a seperate system


# Initialization done, loading gameState
gameStateMenu()

# Starting game loop
while not done:
    # Event management
    actions = eventManager.mainLoopEvent(gameState)

    # Handling the que from the eventManager
    handleReturnData(actions)

    # Game active loop
    if gameState == GAMESTATE.ACTIVE:

        # Time and game clock management
        deltaTime = clock.tick(60)
        time += deltaTime # time and deltatime in milliseconds

        # Reset screen to start drawing frame
        screen.fill(BLACK)

        # Player code
        pd = playerCharacter.update((keyDownFlags['d'] - keyDownFlags['a']),
            (keyDownFlags['s'] - keyDownFlags['w']), keyDownFlags["shift"], deltaTime)
        playerCharacter.draw()

        # The player can now also return data from it's update function which needs to be handled
        handleReturnData(pd)

        patternManager.update(deltaTime, playerCharacter)
        patternManager.draw()


    elif gameState == GAMESTATE.MMENU:
        clock.tick(20)
        screen.fill(DARKGRAY)

        playerCharacter.draw()
        patternManager.draw()

    # UI layer
    # UI uses a seperate system from object drawing.
    # it is created and rendered last and not affected by gamestate
    for UIElement in UI:
        UIElement.draw()

    pygame.display.flip()
pygame.quit()
