from base import *
import menu

class Player():
    """This class defines a player character, using general parameters and player input
    to function"""

    def __init__(self, size, pos, color, acc, drag, lives, scr):
        self.size = size
        (self.x, self.y) = pos
        self.dx, self.dy = 0, 0
        self.acc = acc
        self.drag = drag
        self.color = color # Health bar color
        self.lives = lives
        self.mLives = lives
        self.secCol = DARKGREEN # Object's color
        self.scr =  scr
        self.healthMeter = menu.Text(screen = self.scr, coords = (0.02*h, 0.02*h, 0.12*h, 0.12*h), text = self._healthStr(), border = False, textSize = 18, color=self.color, backGround = True)

    def _healthStr(self):
        return str(self.lives)

    def draw(self):
        # pygame.draw.circle(scr, self.color, self.sPos(), self.size)
        dPos = self.sPos()
        healthBarRad = self.size + 6
        # rect = pygame.Rect(int(dPos[0]-healthBarRad),int(dPos[1]-healthBarRad),
        #     int(2*healthBarRad),int(2*healthBarRad))
        # This command uses topLeft and width/height, that's why we enter .1 instead of .12
        rect = pygame.Rect(0.02*h, 0.02*h, 0.1*h, 0.1*h)

        # Health bar
        pygame.draw.arc(self.scr, self.color, rect, 0, 2*math.pi*self.lives / self.mLives, 2)
        # Drawing text and small background circle for contrast
        # TODO: Integrate contrast circle into menu.Text()
        # pygame.draw.circle(self.scr, BLACK, (int(0.07*h), int(0.07*h)), int(0.04*h))
        self.healthMeter.draw()
        # Player draw/collision marker
        pygame.draw.circle(self.scr, self.secCol, dPos, self.size)


    def update(self, xInp, yInp, sneak, dt):
        rtd = []

        # Game implementation
        # The second part prevents diagonal input from being faster than horizontal
        # input
        diagMod = 0.70710678118 if xInp != 0 and yInp != 0 else 1
        self.x += (self.acc * xInp * (2-sneak) * dt * 0.001) * diagMod
        self.y += (self.acc * yInp * (2-sneak) * dt * 0.001) * diagMod

        # Prevent out-of-bounds character
        self.x = clamp(self.x, 0, w)
        self.y = clamp(self.y, 0, h)

        # Keep the UI updated
        # This part of the UI is integrated into the player instead of the
        # main UI storage, and doesn't get updated by the general UI loop as a result
        self.healthMeter.updateText(self._healthStr())

        # End game when dead
        if self.lives <= 0:
            print("Player lives reached zero, stopping program.")
            rtd.append(Data("stop"))
        return rtd

    def sPos(self):
        return (int(self.x),int(self.y))

    def hit(self, damage):
        self.lives -= damage
