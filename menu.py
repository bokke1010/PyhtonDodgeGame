from base import *
from pygame import freetype
freetype.init()

class Text():
    def __init__(self, screen, coords: tuple = (40,40,w-80,h-80), text: str = "click here!", border = True, textSize = 20, color: tuple = (0  ,0  ,0  ), visibles:list = [], **kwargs):
        # We accept more kwargs to allow overflowing when using this interchangably with more complex UIElement that inherits Text
        self.screen = screen
        self.coords = coords
        self.text = text
        self.color = color
        self.font = freetype.Font(None, textSize)
        self.border = border
        self.visibles = visibles

    def updateText(self, text):
        self.text = text

    def draw(self):
        # absolute coords of the textbox corners, and the textbox width and height
        x1, y1 = self.coords[0], self.coords[1]
        x2, y2 = self.coords[2], self.coords[3]
        dx, dy = x2 - x1       , y2 - y1

        # Draw the text border
        if self.border:
            pygame.draw.rect(self.screen, self.color, (x1,y1,dx,dy), 2)

        # First we calculate the central position of the Button
        # Then we get the size of the text we're rendering
        # Using these values, we calculate the top-left corner for that text to be centered
        # Then we render it
        buttonCenter = (0.5*(x1+x2), 0.5*(y1+y2))
        textRect = self.font.get_rect(self.text, size=self.font.size)

        textPos = (int(buttonCenter[0]-0.5*textRect.width), int(buttonCenter[1]-0.5*textRect.height))
        self.font.render_to(self.screen, textPos, self.text, fgcolor=self.color)

class Button(Text):
    def __init__(self, result: Data = Data("pass"), **kw):
        super().__init__(**kw)
        self.result = result

    def getClick(self, pos):
        if self.coords[0] <= pos[0] <= self.coords[2] and self.coords[1] <= pos[1] <= self.coords[3]:
            return self.onClick()

    def onClick(self):
        print("Button clicked once, returning: " + str(self.result))
        return self.result

class sButton(Button):

    def getClick(self, pos):
        if self.coords[0] <= pos[0] <= self.coords[2] and self.coords[1] <= pos[1] <= self.coords[3]:
            level = (pos[0]-self.coords[0])/self.coords[2]
            return self.onClick(level)

    def onClick(self, level):
        return self.result.set("level", level)
