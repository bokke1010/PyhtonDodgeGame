import projectile, pattern_manager, menu, keyEvents, player
from base import *

# This file acts as a hub for all other files (except base.py, that one only
# contains some lightweight universal constants and functions).
#
# These files can send data back using lists with Data() objects, which are
# dicts in a wrapper that ensures they must have a 'type' key (with value)
# These are rarely longer than 4 key/data pairs

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

playerCharacter = player.Player(playerSize, [w/2, h-playerSize], RED, acceleration, drag, 600, screen)
patternManager = pattern_manager.PatternManager(screen)

levelIndex = 0
levels = patternManager.loadJson("levels.json")

keyDownFlags = {}
for key in keyCodes.values():
    keyDownFlags[key] = False
print(keyDownFlags)

def handleReturnData(data):
    """Handle returned [Data()] objects with commands/information"""
    for action in data:
        if action.type == "stop":
            stopMainLoop()
        elif action.type == "gameState":
            if action.state == GAMESTATE.ACTIVE:
                gameStateActive()
            if action.state == GAMESTATE.MMENU:
                gameStateMenu()
        elif action.type == "level":
            if action.hasattr("deltaLevel"):
                levelRelative(action.deltaLevel)
            else:
                patternManager.startLevel(levels[levelIndex])
                gameStateActive()
        elif action.type == "keySet":
            keyDownFlags[action.key] = action.value

# UI needs it's own file/import, preferably another JSON file like the level system

def levelRelative(relative):
    """Moves the level index according to the given value"""
    global levelIndex, levelCount
    levelIndex += relative
    while levelIndex > patternManager.levelCount-1:
        levelIndex -= patternManager.levelCount
    while levelIndex < 0:
        levelIndex += patternManager.levelCount
    UIElements["startLevel"].updateText(levels[levelIndex])


UIElements = {}
UIElements["Resume"] = menu.Button(screen=screen, coords = (0.1*w,0.3*h,0.9*w,0.4*h),
    text = "resume", result=Data("gameState", state = GAMESTATE.ACTIVE))
UIElements["Exit"] = menu.Button(screen=screen, coords = (0.1*w,0.5*h,0.9*w,0.6*h),
    text = "exit", result=Data("stop"))
UIElements["Title"] = menu.Text(screen=screen, coords = (0.1*w,0.1*h,0.9*w,0.2*h),
    text = "Game Title")
UIElements["spawnGuide"] = menu.Text(screen=screen, coords = (0.1*w,0.7*h,0.9*w,0.75*h),
    text = "Add patterns")

UIElements["prev"] = menu.Button(screen=screen, coords = (0.1*w,0.75*h,0.3*w,0.85*h),
    text = "<--", result=Data("level", deltaLevel = -1))
UIElements["startLevel"] = menu.Button(screen=screen, coords = (0.4*w,0.75*h,0.6*w,0.85*h),
    text = levels[levelIndex], result=Data("level"))
UIElements["next"] = menu.Button(screen=screen, coords = (0.7*w,0.75*h,0.9*w,0.85*h),
    text = "-->", result=Data("level", deltaLevel = 1))
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
