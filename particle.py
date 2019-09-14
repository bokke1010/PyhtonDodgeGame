from base import *
import pygame

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
                pass

    def draw(self):
        for particle in self.particles:
            pos = (int(particle["pos"][0]*w), int(particle["pos"][1]*h))
            pygame.draw.circle(self.screen, particle["color"], pos, int(particle["size"]*w))

    def summon(self, coords, size, lifeTime, color):
        self.particles.append({"pos": coords, "size": size, "lifeTime": lifeTime+self.age, "color": color})
