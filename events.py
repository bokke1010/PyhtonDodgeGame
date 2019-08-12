from base import *
# Since this'll be responsible for buttons, menu is a required import
import menu

class EventManager():

    def __init__(self, UI):
        """This class manages global events like keyboard and mouse input. It
        requires a UI reference to read button locations and triggers"""
        self.UI = UI

    def mainLoopEvent(self, gameState):
        """Returns a que with all actions that should happen according to game input"""
        que = []
        def ret(x: Data):
            """Appends a data object to the return value"""
            que.append(x)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                que.append(Data("stop"))

            # Evaluate menu items (callback/passback????)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for UIElement in self.UI:
                    # print(type(UIElement))
                    if isinstance(UIElement, menu.Button):
                        res = UIElement.getClick(pos)
                        if not res == None:
                            ret(Data("exec", data=res, variable = 0))
                    elif isinstance(UIElement, menu.sButton):
                        res = UIElement.getClick(pos)
                        if not res == None:
                            (r, func) = res
                            ret(Data("exec", data=func, variable=r))

            if event.type == pygame.KEYDOWN:
                # Navigation keys
                if gameState == GAMESTATE.MMENU: # All menu keyEvents
                    if event.key == 275: # Right arrow
                        ret(Data("gameState", state=GAMESTATE.ACTIVE))
                    # if event.key == 27: # Esc. key
                    #     stopMainLoop()
                if gameState == GAMESTATE.ACTIVE: # All game keyEvents
                    if event.key in [276, 27]: # Left arrow or Esc
                        ret(Data("gameState", state=GAMESTATE.MMENU))

                # Directional keys
                # TODO: These should not be handled on a per_case basis
                keyStr = str(event.key)
                if keyStr in keyCodes:
                    ret(Data("keySet", key=keyCodes[keyStr], value = True))


            # KeyUp events for directional keys
            if event.type == pygame.KEYUP:
                keyStr = str(event.key)
                if keyStr in keyCodes:
                    ret(Data("keySet", key=keyCodes[keyStr], value = False))
        return que
