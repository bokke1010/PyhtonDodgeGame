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

def setGameState(state = GAMESTATE.MMENU):
    global gameState, UIElements, UI
    if not gameState == state:
        gameState = state
        setGamestateUI(UIElements, gameState, UI)

def isState(a,b):
    if not type(a) == int:
        a = a.value
    if not type(b) == int:
        b = b.value
    return a == b

def stopMainLoop():
    global done
    done = True

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

done = False

deltaTime = 0
time = 0

playerCharacter = player.Player(playerSize, [w/2, h-playerSize], RED, acceleration, drag, 10, screen)
patternManager = pattern_manager.PatternManager(screen)

levelIndex = 0
levels = patternManager.loadJson("levels.json")
levelIndexName = levels[levelIndex]

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
            if isState(action.state, GAMESTATE.ACTIVE):
                setGameState(GAMESTATE.ACTIVE)
            elif isState(action.state, GAMESTATE.MMENU):
                setGameState(GAMESTATE.MMENU)
            elif isState(action.state, GAMESTATE.HELP):
                setGameState(GAMESTATE.HELP)
        elif action.type == "level":
            if action.hasattr("deltaLevel"):
                levelRelative(action.deltaLevel)
            else:
                patternManager.startLevel(levels[levelIndex])
                setGameState(GAMESTATE.ACTIVE)
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

    # Trying to remove all button-specific code eventually
    levelIndexName = levels[levelIndex]
    UIElements["startLevel"].updateText(levelIndexName)


UIElements = menu.parseMenuList(menu.parseJson(menu.loadJson("menuItems.json")), screen)
UI = []
# Calling a empty levelRelative to initiate the level select button text
# This is obviously kind of clunky, but that whole button is kind of a hack
levelRelative(0)

# I would consider giving ui import dicts like MenuButtons a unique ID, but I can't imagine
# a scenario where multiple copies of the same UI would need to exist right now...
eventManager = keyEvents.EventManager(UI)
# UI will eventually get a seperate system


# Initialization done, loading gameState
setGameState(GAMESTATE.MMENU)

# Starting game loop
while not done:
    # Event management
    actions = eventManager.mainLoopEvent(gameState)

    # Handling the que from the eventManager
    handleReturnData(actions)

    # Game active loop
    if isState(gameState, GAMESTATE.ACTIVE):

        # Time and game clock management
        deltaTime = clock.tick(60)
        time += deltaTime # time and deltatime in milliseconds

        # Reset screen to start drawing frame
        screen.fill(BLACK)

        patternManager.update(deltaTime, playerCharacter)
        patternManager.draw()

        # Player code
        kdf = keyDownFlags
        pd = playerCharacter.update((kdf['d'] - kdf['a']),
            (kdf['s'] - kdf['w']), kdf["shift"], deltaTime)
        playerCharacter.draw()

        # The player can now also return data from it's update function which needs to be handled
        handleReturnData(pd)



    elif isState(gameState, GAMESTATE.MMENU):
        clock.tick(20)
        screen.fill(DARKGRAY)

        patternManager.draw()
        playerCharacter.draw()

    elif isState(gameState, GAMESTATE.HELP):
        clock.tick(20)
        screen.fill(BLACK)

    # UI layer
    # UI uses a seperate system from object drawing.
    # it is created and rendered last and not affected by gamestate
    for UIElement in UI:
        UIElement.draw()

    pygame.display.flip()
pygame.quit()
