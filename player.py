from base import *
import menu, particle

class Player():
    """This class defines a player character, using general parameters and player input
    to function"""

    def __init__(self, size, pos, color, acc, drag, lives, screen):
        self.size = size

        (self.x, self.y) = pos
        self.dx, self.dy = 0, 0
        self.acc = acc
        self.drag = drag

        self.lives = lives
        self.mLives = lives

        self.age = 0
        self.hitTimer = 0

        self.color = color # Health bar color
        self.secCol = DARKGREEN # Object's color

        self.screen =  screen

        self.healthMeter = menu.Text(screen = self.screen, coords = (0.02*h, 0.02*h, 0.12*h, 0.12*h), text = self._healthStr(), border = False, textSize = 18, color=self.color, backGround = True)
        self.particle = particle.ParticleManager(screen = self.screen)

    def _healthStr(self):
        return str(self.lives)

    def draw(self):
        dPos = self._sPos()

        # This command uses topLeft and width/height, that's why we enter .1 instead of .12
        rect = pygame.Rect(0.02*h, 0.02*h, 0.1*h, 0.1*h)

        # Health bar
        pygame.draw.arc(self.screen, self.color, rect, 0, 2*math.pi*self.lives / self.mLives, 2)
        # Drawing text and small background circle for contrast
        self.healthMeter.draw()
        self.particle.draw()
        # Player draw/collision marker
        pygame.draw.circle(self.screen, self.secCol, dPos, int(self.size*w))


    def update(self, xInp, yInp, sneak, dt):
        rtd = []

        self.age += dt
        # Game implementation
        # The second part prevents diagonal input from being faster than horizontal
        # input
        diagMod = 0.70710678118 if xInp != 0 and yInp != 0 else 1
        self.x += (self.acc * xInp * (2-sneak) * dt * 0.001) * diagMod
        self.y += (self.acc * yInp * (2-sneak) * dt * 0.001) * diagMod

        # Prevent out-of-bounds character
        self.x = clamp(self.x, 0, 1)
        self.y = clamp(self.y, 0, 1)

        # Keep the UI updated
        # This part of the UI is integrated into the player instead of the
        # main UI storage, and doesn't get updated by the general UI loop as a result
        self.healthMeter.updateText(self._healthStr())
        self.particle.update(dt)

        # End game when dead
        if self.lives <= 0:
            print("Player lives reached zero, stopping program.")
            rtd.append(Data("stop"))
        return rtd

    def _sPos(self):
        return (int(self.x * w),int(self.y * h))

    def pos(self):
        return (self.x,self.y)

    def _vulnerable(self):
        return self.age > self.hitTimer

    def hit(self, damage):
        if self._vulnerable():
            self.hitTimer = self.age + 600
            self.lives -= damage
            self.particle.summon(self.pos(), 0.1, 900, LIGHTGRAY, ds=-0.01)
            return True
        return False
