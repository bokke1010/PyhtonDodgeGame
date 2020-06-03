import projectile, pattern_manager, menu, keyEvents, player, gamestates
from base import *

# This file acts as a hub for all other files (except base.py, that one only
# contains some lightweight universal constants and functions).
#
# These files can send data back using lists with Data() objects, which are
# dicts in a wrapper that ensures they must have a 'type' key (with value)
# These are rarely longer than 4 key/data pairs

# All initialization

# Clearing logfile
open('log.txt', 'w').close()

pygame.init()

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

gameState = None
loadedStates = {}

# NOTE: This is where you can add custom gamestates (before the state loading)

for key, state in gamestates.gameStates.items():
    loadedStates[key] = state() # Can also use state.value, but we've already got the keys

def setGamestateUI(UIElements, gameState, UI):
    for key, item in UIElements.items():
        if gameState.value in item.visibles:
            activateUIElement(UI, item)
        else:
            deactivateUIElement(UI, item)

def setGameState(state = GAMESTATE.MMENU):
    global gameState, UIElements, UI, loadedStates
    if (gameState == None) or (not gameState.value == state):
        gameState = loadedStates[state]
        setGamestateUI(UIElements, gameState, UI)

def stopMainLoop():
    global done
    done = True

# Defining in-game variables
done = False

deltaTime = 0
time = 0

playerCharacter = player.Player(playerSize, [0.5, 0.9], RED, speed, playerLives, screen)
patternManager = pattern_manager.PatternManager(screen, playerCharacter)

levelIndex = 0
levels = patternManager.loadJson("levels.json")
levelIndexName = levels[levelIndex]

keyDownFlags = {}
for key in keyCodes.values():
    keyDownFlags[key] = False
print(keyDownFlags)

# Passing around the required variables to our gamestate controller
gamestates.passClass(screen = screen, clock = clock, patternManager = patternManager, playerCharacter = playerCharacter)


def handleReturnData(data):
    """Handle returned [Data()] objects with commands/information"""
    for action in data:
        log(str(action))
        if action.type == "stop":
            stopMainLoop()
        elif action.type == "gameState":
            setGameState(action.state)
        elif action.type == "level":
            if action.hasattr("deltaLevel"):
                levelRelative(action.deltaLevel)
            else:
                patternManager.startLevel(levels[levelIndex])
                setGameState(GAMESTATE.ACTIVE)
        elif action.type == "keySet":
            keyDownFlags[action.key] = action.value
        elif action.type == "hit":
            playerCharacter.hit(action.damage)

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


UIElements = menu.parseJson(menu.loadJson("menuItems.json"), screen)
UI = []
# Calling a empty levelRelative to initiate the level select button text
# This is obviously kind of clunky, but that whole button is kind of a hack
levelRelative(0)

# I would consider giving ui import dicts like MenuButtons a unique ID, but I can't imagine
# a scenario where multiple copies of the same UI would need to exist right now...
eventManager = keyEvents.EventManager(UI)


# Initialization done, loading gameState
setGameState(GAMESTATE.MMENU)

# Starting game loop
while not done:
    # Event management
    actions = eventManager.mainLoopEvent(gameState)

    # Handling the que from the eventManager
    handleReturnData(actions)

    # Game active loop
    # We already passed most required objects earlier (why there not here or the other way around?)
    # So we only need to pass kdf
    returnData = gameState.update(keyDownFlags = keyDownFlags)
    if not returnData == None:
        handleReturnData(returnData)


    # UI layer
    # UI uses a seperate system from object drawing.
    # it is created and rendered last and not affected by gamestate
    for UIElement in UI:
        UIElement.draw()
    pygame.display.flip()
pygame.quit()
