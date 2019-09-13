from base import *
from pygame import freetype
import json
freetype.init()

def loadJson(fileName:str) -> dict:
    """Way to simple json load function, why is this even here?"""
    with open(fileName) as json_file:
        return json.load(json_file)


def parseJson(jsonIn: dict) -> dict:
    """Parses JSON from a file to dicts readable by parseMenuList() (see main.py)"""
    def formatData(value: dict) -> dict:
        textValue = value["text"]
        menuType = globals()[value["object"]]

        # TODO: make up my mind on a common standard to add data this way
        resultOut = None
        if "result" in value:
            resultIn = value["result"].split(":")
            if resultIn[0] == "stop":
                resultOut = Data("stop")
            elif resultIn[0] == "level":
                resultOut = Data("level")
                if len(resultIn) == 2:
                    resultOut.set("deltaLevel", int(resultIn[1]))
            elif resultIn[0] == "gameState": # gameState:1
                resultOut = Data("gameState", state = int(resultIn[1]))


        color = globals()[value["color"]] if "color" in value else BLACK
        visibles = [getattr(GAMESTATE, x) for x in value["visibles"]]
        border = value["border"] if "border" in value else True

        return {"text":textValue, "object":menuType, "coordinates":tuple(value["coordinates"]), "result":resultOut, "visibles":visibles, "color":color, "border":border}
    rv = {}
    for key, value in jsonIn.items():
        rv[key] = formatData(value)
    return rv

def parseMenuList(items:dict, screen:pygame.display) -> dict:
    UIElements = {}
    for key, item in items.items():
        coords = (item["coordinates"][0]*w, item["coordinates"][1]*h, item["coordinates"][2]*w, item["coordinates"][3]*h)
        item["result"] = None if not "result" in item else item["result"]
        item["color"] = GRAY if not "color" in item else item["color"]
        text = item["text"]

        UIElements[key] = item["object"](screen = screen, coords = coords, text = text, result = item["result"], visibles = item["visibles"], color=item["color"], border = item["border"])
    # print(UIElements)
    return UIElements

class MenuItem():
    def __init__(self, screen, coords: tuple = (40,40,w-40,h-40), visibles:list = [], **kw):
        self.screen = screen
        self.coords = coords
        self.visibles = visibles

    def draw(self):
        pass

    def __repr__(self):
        return "MenuItem parent class, visibles: " + str(self.visibles)


class Text(MenuItem):
    def __init__(self, text: str = "text box", border = True, textSize = 20, color: tuple = (0  ,0  ,0  ), backGround:bool = False, **kw):
        super().__init__(**kw)
        # We accept more kwargs to allow overflowing when using this interchangably with more complex UIElements

        self.text = text
        self.color = color
        self.font = freetype.Font(None, textSize)
        self.border = border
        self.backGround = backGround

    def updateText(self, text):
        self.text = text

    def draw(self):
        super().draw()
        # absolute coords of the textbox corners, and the textbox width and height
        x1, y1 = self.coords[0], self.coords[1]
        x2, y2 = self.coords[2], self.coords[3]
        dx, dy = x2 - x1       , y2 - y1

        # First we calculate the central position of the Button
        # Then we get the size of the text we're rendering
        # Using these values, we calculate the top-left corner for that text to be centered
        buttonCenter = (0.5*(x1+x2), 0.5*(y1+y2))
        textRect = self.font.get_rect(self.text, size=self.font.size)
        textPos = (int(buttonCenter[0]-0.5*textRect.width), int(buttonCenter[1]-0.5*textRect.height))

        # Draw the text border
        if self.border:
            pygame.draw.rect(self.screen, self.color, (x1,y1,dx,dy), 2)
        if self.backGround:
            bgColor = BLACK if sum([channel/3 for channel in self.color]) > 63 else WHITE
            bgB = 4 # background border width
            backgroundRect = (textPos[0]-bgB, textPos[1]-bgB, textRect.width+2*bgB, textRect.height+2*bgB)
            pygame.draw.rect(self.screen, bgColor, backgroundRect)

        self.font.render_to(self.screen, textPos, self.text, fgcolor=self.color)

    def __repr__(self):
        return "MenuItem Text class: " + str(self.visibles)


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

    def __repr__(self):
        return "MenuItem Button class: " + str(self.visibles)
# This needs to be reimplemented as a proper silder later
#
# class sButton(Button):
#
#     def getClick(self, pos):
#         if self.coords[0] <= pos[0] <= self.coords[2] and self.coords[1] <= pos[1] <= self.coords[3]:
#             level = (pos[0]-self.coords[0])/self.coords[2]
#             return self.onClick(level)
#
#     def onClick(self, level):
#         return self.result.set("level", level)
