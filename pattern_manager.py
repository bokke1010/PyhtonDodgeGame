import json
import projectile
from base import *

class PatternManager():

    def __init__(self, screen):
        self.screen = screen
        self.spawners = {}
        self.que = []
        self.time = 0
        self.lc = 0

    def loadJson(self, fileName):
        with open(fileName) as json_file:
            self.data = json.load(json_file)

    def startLevel(self, level):
        data = self.data[level]
        scheduledTime = self.time
        for item in data:
            for key, value in item.items():
                if key == "spawner":
                    for name, command in value.items():
                        self.que.append((scheduledTime, "add", name + ":" + str(self.lc), command))
                if key == "wait":
                    scheduledTime += value
                if key == "del":
                    for delSpawner in value:
                        self.que.append((scheduledTime, "del", delSpawner + ":" + str(self.lc)))

        # Unique identifier to prevent levels overwriting each other
        self.lc += 1
        # Sort que
        self.que.sort()

    def process(self, command):
        # command[0] is timing, often not required
        # command[1] is instruction
        # command [2] is arg1 (optional, often name)
        # command [3] is arg2 (optional)
        # etc.
        if command[1] == "add":
            self.spawners[command[2]] = self.parseSpawner(command[3])
            return True
        elif command[1] == "del":
            if self.spawners[command[2]].deleteSpawner():
                self.spawners.pop(command[2], True)
                return True
            else:
                return False
        elif command[1] == "end":
            self.spawners = {}
            return True


    def parseSpawner(self, command):
        lt = -1
        slt = -1
        bdw = 3
        if "bulletLifeTime" in command:
            lt = command["bulletLifeTime"]
        if "spawnerLifeTime" in command:
            slt = command["spawnerLifeTime"]
        if "borderWidth" in command:
            bdw = command["borderWidth"] # Borderwidth can be both a str as an int, so we assure the correct type is passed on later

        spawner = projectile.bulletSpawner(screen=self.screen, spawningDelay=command["delay"], lifeTime = lt, spawnerLT = slt)

        if command["type"] == "pointExp":
            spawner.setSpawningPointExp(coords=(command["sX"], command["sY"]), dir = command["bDir"], speed = command["speed"], size=command["size"], borderWidth=str(bdw))
        if command["type"] == "expBExp":
            spawner.setSpawningExpBexp(coords=(command["sX"], command["sY"]), bulletPattern = (command["bX"], command["bY"]), size=command["size"], borderWidth=str(bdw))
        if command["type"] == "bExpAbs":
            spawner.setSpawningBexpAbs(coords=(command["bX"], command["bY"]), size=command["size"], borderWidth=str(bdw))
        return spawner

    def add_pattern(self, pattern, name):
        spawners[name] = pattern

    def update(self, dt, player):
        self.time += dt*1000
        if len(self.que) > 0:
            while self.que[0][0] <= self.time:
                print(self.que[0])
                self.process(self.que[0])
                self.que.pop(0)
                # Stop checking the que if it is empty now
                if len(self.que) == 0:
                    break
        # Since we decided to only remove spawners once they have no more bullets left, we have to check for that
        deleteQue = set()
        for key, spawner in self.spawners.items():
            spawner.update(dt, player)
            if spawner.delete and len(spawner.bullets) == 0:
                deleteQue.add(key)
        for key in deleteQue:
            self.spawners.pop(key, True)

    def draw(self):
        for spawner in self.spawners:
            self.spawners[spawner].draw()
