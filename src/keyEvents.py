from base import *
# Since this'll be responsible for buttons, menu is a required import
import menu

class EventManager():

    def __init__(self, UI):
        """This class manages global events like keyboard and mouse input. It
        requires a UI reference to read button locations and triggers"""
        self.UI = UI

    def mainLoopEvent(self, gameState):
        """Returns a events with all actions that should happen according to game input"""
        events = Que()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.add(Data("stop"))

            # Evaluate menu items (callback/passback????)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for UIElement in self.UI:
                    if isinstance(UIElement, menu.Button):
                        events.add(UIElement.getClick(pos))

            elif event.type == pygame.KEYDOWN:
                # KeyPressed events
                if event.key in gameState.keyDown:
                    events.add(gameState.keyDown[event.key])

                # KeyDown events
                if event.key in keyCodes:
                    events.add(Data("keySet", key=keyCodes[event.key], value = True))


            elif event.type == pygame.KEYUP:
                # KeyReleased events
                # if event.key in gameState.keyUp:
                #     ret(gameState.keyUp[event.key])

                # KeyUp events
                if event.key in keyCodes:
                    events.add(Data("keySet", key=keyCodes[event.key], value = False))
        return list(events)
