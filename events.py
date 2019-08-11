from base import *
# Since this'll be responsible for buttons, menu is a required import
import menu

class ReturnData():
    def __init__(self, type, **data):
        self.type = type
        self.__dict__.update(data)

class EventManager():
    """This class manages global events like keyboard and mouse input. It
    requires a reference to read button locations and output"""

    def __init__(self, UI):
        self.UI = UI

    def mainLoopEvent(self, gameState):
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(ReturnData("stop"))

            # Evaluate menu items (callback/passback????)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for UIElement in self.UI:
                    # print(type(UIElement))
                    if isinstance(UIElement, menu.Button):
                        res = UIElement.getClick(pos)
                        if not res == None:
                            actions.append(ReturnData("exec", data=res, variable = 0))
                    elif isinstance(UIElement, menu.sButton):
                        res = UIElement.getClick(pos)
                        if not res == None:
                            (r, func) = res
                            actions.append(ReturnData("exec", data=func, variable=r))

            if event.type == pygame.KEYDOWN:
                # Navigation keys
                if gameState == GAMESTATE.MMENU: # All menu keyEvents
                    if event.key == 275: # Right arrow
                        actions.append(ReturnData("gameState", state=GAMESTATE.ACTIVE))
                    # if event.key == 27: # Esc. key
                    #     stopMainLoop()
                if gameState == GAMESTATE.ACTIVE: # All game keyEvents
                    if event.key in [276, 27]: # Left arrow or Esc
                        actions.append(ReturnData("gameState", state=GAMESTATE.MMENU))
                # Directional keys
                if event.key == 119:
                    actions.append(ReturnData("keySet", key = 'w', value = True))
                if event.key == 97:
                    actions.append(ReturnData("keySet", key = 'a', value = True))
                if event.key == 115:
                    actions.append(ReturnData("keySet", key = 's', value = True))
                if event.key == 100:
                    actions.append(ReturnData("keySet", key = 'd', value = True))

                if event.key == 304:
                    actions.append(ReturnData("keySet", key = 'shift', value = True))


            # KeyUp events for directional keys
            if event.type == pygame.KEYUP:
                if event.key == 119: # W-key (event.unicode doesn't exist for KEYUP)
                    actions.append(ReturnData("keySet", key = 'w', value = False))
                if event.key == 97: # A-key
                    actions.append(ReturnData("keySet", key = 'a', value = False))
                if event.key == 115: # S-key
                    actions.append(ReturnData("keySet", key = 's', value = False))
                if event.key == 100: # D-key
                    actions.append(ReturnData("keySet", key = 'd', value = False))

                if event.key == 304: # Shift-key
                    actions.append(ReturnData("keySet", key = 'shift', value = False))
        return actions
