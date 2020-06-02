from base import *
import pygame, numexpr

class ParticleManager():

    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.age = 0

    def update(self, dt):
        self.age += dt

        for particle in self.particles:
            if particle["lifeTime"] < self.age:
                self.particles.remove(particle)
            else:
                particle["pos"] = (particle["pos"][0] + particle["dxdy"][0], particle["pos"][1] + particle["dxdy"][1])
                particle["size"] += particle["ds"]

    def draw(self):
        for particle in self.particles:
            pos = (int(particle["pos"][0]*w), int(particle["pos"][1]*h))
            drawSize = int(particle["size"] * w)
            if drawSize > 1:
                pygame.draw.circle(self.screen, particle["color"], pos, drawSize)

    def summon(self, coords, size, lifeTime, color = LIGHTGRAY, dxdy = (0,0), ds = (0)):
        self.particles.append({"pos": coords, "size": size, "lifeTime": lifeTime+self.age, "color": color, "dxdy": dxdy, "ds":ds})
