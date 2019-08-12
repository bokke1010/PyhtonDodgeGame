from base import *

class Player():
    """This class defines a player character, using general parameters and player input
    to function"""
    def __init__(self, size, pos, color, acc, drag, lives, scr):
        self.size = size
        (self.x, self.y) = pos
        self.dx, self.dy = 0, 0
        self.acc = acc
        self.drag = drag
        self.color = color
        self.lives = lives
        self.mLives = lives
        self.secCol = DARKGREEN
        self.scr =  scr

    def draw(self):
        # pygame.draw.circle(scr, self.color, self.sPos(), self.size)
        dPos = self.sPos()
        healthCS = self.size + 3
        rect = pygame.Rect(int(dPos[0]-healthCS),int(dPos[1]-healthCS),
            int(2*healthCS),int(2*healthCS))
        # Health bar
        pygame.draw.arc(self.scr, self.color, rect, 0, 2*math.pi*self.lives / self.mLives)
        # Collision marker
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
        if self.lives <= 0:
            rtd.append(Data("stop"))
        return rtd

    def sPos(self):
        return (int(self.x),int(self.y))

    def hit(self, damage):
        self.lives -= damage
