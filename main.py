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

def setGamestateUI(UIElements, gameState, UI):
    for key, item in UIElements.items():
        if gameState in item.visibles:
            activateUIElement(UI, item)
        else:
            deactivateUIElement(UI, item)

def gameStateActive():
    global gameState, UIELements, UI
    if not gameState == GAMESTATE.ACTIVE:
        gameState = GAMESTATE.ACTIVE
        setGamestateUI(UIElements, gameState, UI)

def gameStateMenu():
    global gameState
    if not gameState == GAMESTATE.MMENU:
        gameState = GAMESTATE.MMENU
        setGamestateUI(UIElements, gameState, UI)

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

def parseMenuList(items:dict, UIElements:dict, screen:pygame.display):
    for key, item in items.items():
        coords = (item["coordinates"][0]*w, item["coordinates"][1]*h, item["coordinates"][2]*w, item["coordinates"][3]*h)
        item["result"] = None if not "result" in item else item["result"]
        item["color"] = GRAY if not "color" in item else item["color"]
        UIElements[key] = item["object"](screen = screen, coords = coords, text = item["text"], result = item["result"], visibles = item["visibles"], color=item["color"])

# I considered using Data() for this, but dicts are probably better suited
# The only downside is that keys are strings instead of arguments, making it slightly more chaotic
# The key here is also the key in UIElements, this step is required to simplify
# and eventually externalize UI
MenuButtons = {
    "Resume":{"text":"resume", "object":menu.Button, "coordinates":(0.1, 0.3, 0.9, 0.4), "result":Data("gameState", state=GAMESTATE.ACTIVE), "visibles":[GAMESTATE.MMENU], "color":DARKGREEN},
    "Exit":{"text":"exit", "object":menu.Button, "coordinates":(0.1, 0.5, 0.9, 0.6), "result":Data("stop"), "visibles":[GAMESTATE.MMENU], "color":RED},
    "Title":{"text":"Dodge something?", "object": menu.Text, "coordinates":(0.1, 0.1, 0.9, 0.2), "visibles":[GAMESTATE.MMENU], "color":WHITE},
    "spawnGuide":{"text":"Add patterns", "object": menu.Text, "coordinates":(0.1, 0.7, 0.9, 0.75), "visibles":[GAMESTATE.MMENU]},
    "prev":{"text":"<--", "object":menu.Button, "coordinates":(0.1, 0.75, 0.3, 0.85), "result":Data("level", deltaLevel = -1), "visibles":[GAMESTATE.MMENU]},
    "startLevel":{"text":levels[levelIndex], "object":menu.Button, "coordinates":(0.4, 0.75, 0.6, 0.85), "result":Data("level"), "visibles":[GAMESTATE.MMENU]},
    "next":{"text":"-->", "object":menu.Button, "coordinates":(0.7, 0.75, 0.9, 0.85), "result":Data("level", deltaLevel = 1), "visibles":[GAMESTATE.MMENU]},

}

UIElements = {}

UI = []

# I would consider giving ui import dicts like MenuButtons a unique ID, but I can't imagine
# a scenario where multiple copies of the same UI would need to exist right now...
parseMenuList(MenuButtons, UIElements, screen)

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

        patternManager.update(deltaTime, playerCharacter)
        patternManager.draw()

        # Player code
        pd = playerCharacter.update((keyDownFlags['d'] - keyDownFlags['a']),
            (keyDownFlags['s'] - keyDownFlags['w']), keyDownFlags["shift"], deltaTime)
        playerCharacter.draw()

        # The player can now also return data from it's update function which needs to be handled
        handleReturnData(pd)



    elif gameState == GAMESTATE.MMENU:
        clock.tick(20)
        screen.fill(DARKGRAY)

        patternManager.draw()
        playerCharacter.draw()

    # UI layer
    # UI uses a seperate system from object drawing.
    # it is created and rendered last and not affected by gamestate
    for UIElement in UI:
        UIElement.draw()

    pygame.display.flip()
pygame.quit()
