from base import *
from pygame import freetype
freetype.init()

class Button():
    def __init__(self, screen, coords: list = [40,40,w-80,h-80], text: str = "click here!", obj = None, result: str = "print('works')"):
        self.screen = screen
        self.coords = coords
        self.text = text
        self.object = obj
        self.result = result
        self.textRenderer = Text(screen, coords, text)

    def draw(self):
        self.textRenderer.draw()

    def getClick(self, pos):
        if self.coords[0] <= pos[0] <= self.coords[2] and self.coords[1] <= pos[1] <= self.coords[3]:
            self.onClick()

    def onClick(self):
        o = self.object
        eval(self.result)

class Text():
    def __init__(self, screen, coords: list = [40,40,w-80,h-80], text: str = "click here!"):
        self.screen = screen
        self.coords = coords
        self.text = text
        self.font = freetype.Font(None, 20)

    def draw(self, color: tuple = BlACK):
        pygame.draw.rect(self.screen, color, self.coords, 1)
        # First we calculate the central position of the Button
        # Then we get the size of the text we're rendering
        # Using these values, we calculate the top-left corner for that text to be centered
        # Then we render it
        bm = (self.coords[0]+0.5*self.coords[2], self.coords[1]+0.5*self.coords[3])
        textRect = self.font.get_rect(self.text, size=self.font.size)
        ts = (textRect[2]-textRect[0], self.font.size)

        textPos = (int(bm[0]-0.5*ts[0]), int(bm[1]-0.5*ts[1]))
        self.font.render_to(self.screen, textPos, self.text, fgcolor=color)

    def getClick(self, pos):
        if self.coords[0] <= pos[0] <= self.coords[2] and self.coords[1] <= pos[1] <= self.coords[3]:
            self.onClick()

    def onClick(self):
        o = self.object
        eval(self.result)
