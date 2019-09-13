from base import *

gameStates = {}

screen = None
clock = None
patternManager = None
playerCharacter = None
def passClass(**kwargs):
    for key, value in kwargs.items():
        if key in globals():
            globals()[key] = value

class Gamestate():
    def __init__(self):
        super().__init__()
        self.keyUp = {}
        self.keyDown = {}

    def update(self):
        pass

class GamestateMenu(Gamestate):

    def __init__(self):
        super().__init__()
        self.keyUp[275] = Data("gameState", state=GAMESTATE.ACTIVE)

    def update(self, **kwarg):
        super().update()
        clock.tick(20)
        screen.fill(DARKGRAY)


class GamestateMainMenu(GamestateMenu):
    value = GAMESTATE.MMENU
    def update(self, **kwarg):
        super().update()
        patternManager.draw()
        playerCharacter.draw()
gameStates[GamestateMainMenu.value] = GamestateMainMenu

class GamestateHelp(GamestateMenu):
    value = GAMESTATE.HELP
    def update(self, **kwarg):
        super().update()
gameStates[GamestateHelp.value] = GamestateHelp


class GamestateActive(Gamestate):
    value = GAMESTATE.ACTIVE

    def __init__(self, **kwarg):
        super().__init__()
        self.time = 0
        self.keyUp[27] = Data("gameState", state=GAMESTATE.MMENU)
        self.keyUp[276] = Data("gameState", state=GAMESTATE.MMENU)

    def update(self, **kwarg):
        super().update()
        # Time and game clock management
        deltaTime = clock.tick(60)
        self.time += deltaTime # time and deltatime in milliseconds

        # Reset screen to start drawing frame
        screen.fill(BLACK)

        patternManager.update(deltaTime, playerCharacter)
        patternManager.draw()

        # Player code
        kdf = kwarg["keyDownFlags"] # Keyword argument passed into update
        pd = playerCharacter.update((kdf['d'] - kdf['a']),
            (kdf['s'] - kdf['w']), kdf["shift"], deltaTime)
        playerCharacter.draw()

        # The player can now also return data from it's update function which needs to be handled
        return pd
gameStates[GamestateActive.value] = GamestateActive

def addState(state):
    gameStates[state.value] = state


print(gameStates)
