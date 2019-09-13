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
            # Too lazy to do this inline
            if not x == None:
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
                        ret(UIElement.getClick(pos))
                    # elif isinstance(UIElement, menu.sButton):
                    #     ret(UIElement.getClick(pos))

            # TODO: Integrate this into gamestate classes somehow
            if event.type == pygame.KEYDOWN:
                # Navigation keys
                if event.key in gameState.keyUp:
                    ret(gameState.keyUp[event.key])

                # Directional keys
                if event.key in keyCodes:
                    ret(Data("keySet", key=keyCodes[event.key], value = True))


            # KeyUp events for directional keys
            if event.type == pygame.KEYUP:
                if event.key in keyCodes:
                    ret(Data("keySet", key=keyCodes[event.key], value = False))
        return que
