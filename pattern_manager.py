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
        self.spawner = projectile.bulletSpawner(screen = screen, spawning = False)


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
                if key == "bullet":
                    for command in value:
                        self.que.append((scheduledTime, "bul", command))
                if key == "wait":
                    scheduledTime += value
                if key == "del":
                    for delItem in value:
                        self.que.append((scheduledTime, "del", delItem + ":" + str(self.lc)))

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
        elif command[1] == "bul":
            bullet = self.parseBullet(command[2])
            self.spawner.addBullet(bullet)
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

    def parseBullet(self, command):
        preTime = 0
        if "preTime" in command:
            preTime = command["preTime"]
        lifeTime = -1
        if "lifeTime" in command:
            lifeTime = command["lifeTime"]
        bdw = 3
        if "borderWidth" in command:
            bdw = command["borderWidth"]
        bullet = projectile.Bullet(preTime = preTime, lifeTime = lifeTime)
        if command["type"] == "line":
            bullet.setBulletPatternLine(pos = (command["x"], command["y"]), vel = (command["dx"], command["dy"]), size = command["size"], borderWidth = int(bdw))
        if command["type"] == "expRel":
            bullet.setBulletPatternExpRel(pos = (command["x"], command["y"]), vel = (command["dx"], command["dy"]), size = command["size"], borderWidth = str(bdw))
        if command["type"] == "expAbs":
            bullet.setBulletPatternExpAbs(pos = (command["x"], command["y"]), size = command["size"], borderWidth = str(bdw))

        return bullet

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

        # Update the integrated spawner used as parent for bullets created by a bullet command
        self.spawner.update(dt, player)
        # Since we decided to only remove spawners once they have no more bullets left, we have to check for that
        deleteQue = set()
        for key, spawner in self.spawners.items():
            spawner.update(dt, player)
            if spawner.delete and len(spawner.bullets) == 0:
                deleteQue.add(key)
        for key in deleteQue:
            self.spawners.pop(key, True)

    def draw(self):
        self.spawner.draw()
        for spawner in self.spawners:
            self.spawners[spawner].draw()
