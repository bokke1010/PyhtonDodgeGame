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
        self.healthMeter = menu.Text(screen = self.scr, coords = (0.02*h, 0.02*h, 0.12*h, 0.12*h), text = self._healthStr(), border = False, textSize = 18, color=self.color)

    def _healthStr(self):
        return str(round(100*self.lives/self.mLives))

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
        pygame.draw.circle(self.scr, BLACK, (int(0.07*h), int(0.07*h)), int(0.04*h))
        self.healthMeter.draw()
        # Player draw/collision marker
        pygame.draw.circle(self.scr, self.secCol, dPos, self.size)


    def update(self, xInp, yInp, sneak, dt):
        rtd = []
        # air resistance as expected
        # self.dx += self.acc * xInp * dt
        # self.dx -= self.drag * abs(self.dx)**2 * ((self.dx > 0) - (self.dx < 0)) * dt
        # self.x += self.dx * dt
        #
        # self.dy += self.acc * yInp * dt
        # self.dy -= self.drag * abs(self.dy)**2 * ((self.dy > 0) - (self.dy < 0)) * dt
        # self.y += self.dy * dt

        # Game implementation
        # Maximum speed is 320px in each direction (160*2), so sqrt(320^2+320^2) = 453 total
        self.dx = self.acc * xInp
        # self.dx -= self.drag * abs(self.dx)**2 * ((self.dx > 0) - (self.dx < 0)) * dt
        self.x += self.dx * (2-sneak) * dt * 0.001

        self.dy = self.acc * yInp
        # self.dy -= self.drag * abs(self.dy)**2 * ((self.dy > 0) - (self.dy < 0)) * dt
        self.y += self.dy * (2-sneak) * dt * 0.001

        # Prevent out-of-bounds character
        while self.x > w:
            self.x = w
            if self.dx > 0:
                self.dx = 0
        while self.x < 0:
            self.x = 0
            if self.dx < 0:
                self.dx = 0
        while self.y > h:
            self.y = h
            if self.dy > 0:
                self.dy = 0
        while self.y < 0:
            self.y = 0
            if self.dy < 0:
                self.dy = 0

        # End game when dead
        self.healthMeter.updateText(self._healthStr())
        if self.lives <= 0:
            print("Player lives reached zero, stopping program.")
            rtd.append(Data("stop"))
        return rtd

    def sPos(self):
        return (int(self.x),int(self.y))

    def hit(self, damage):
        self.lives -= damage
