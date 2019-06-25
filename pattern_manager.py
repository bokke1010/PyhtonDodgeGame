import json
import projectile
from base import *
from collections import deque

class PatternManager():

    def __init__(self, screen):
        self.screen = screen
        self.bulletManagers = {}
        self.que = deque()
        self.time = 0
        self.lc = 0
        self.bulletManager = projectile.BulletManager(screen = screen)


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
                        self.que.append((scheduledTime, "spw", name + ":" + str(self.lc), command))
                if key == "bullet":
                    for command in value:
                        self._queAppend((scheduledTime, "bul", command))
                if key == "pattern":
                    for name, command in value.items():
                        self._queAppend((scheduledTime, "pat", name + ":" + str(self.lc), command))
                if key == "trigger":
                    for command in value:
                        self._queAppend((scheduledTime, "trg", name + ":" + str(self.lc)))
                if key == "wait":
                    scheduledTime += value
                if key == "del":
                    for delItem in value:
                        self._queAppend((scheduledTime, "del", delItem + ":" + str(self.lc)))

        # Unique identifier to prevent levels overwriting each other
        self.lc += 1

    def _queAppend(self, command):
        if len(self.que) > 0 and self.que[-1][0] > command[0]:
            i = len(self.que) - 1
            while (self.que[i][0] > command[0]):
                i -= 1
            self.que.insert(i+1, command)
        else:
            self.que.append(command)

    def process(self, command):
        # command[0] is timing, often not required
        # command[1] is instruction
        # command [2] is arg1 (optional, often name)
        # command [3] is arg2 (optional)
        # etc.
        if command[1] == "spw":
            spawner = self.parseSpawner(command[3])
            self.bulletManagers[command[2]] = spawner
        elif command[1] == "bul":
            # Bullets do not have a name, so command[2] contains their parameters
            bullet = self.parseBullet(command[2])
            self.bulletManager.addBullet(bullet)
        elif command[1] == "pat":
            pattern = self.parsePattern(command[3])
            self.bulletManagers[command[2]] = pattern
        elif command[1] == "trg":
            self.bulletManagers[command[2]].trigger()
        elif command[1] == "del":
            if self.bulletManagers[command[2]].deleteManager():
                self.bulletManagers.pop(command[2], True)
                return True
            else:
                return False
        elif command[1] == "end":
            self.bulletManagers = {}
            return True


    def parseSpawner(self, command):
        lt = -1
        slt = -1
        pt = 0
        bdw = 3
        if "bulletLifeTime" in command:
            lt = command["bulletLifeTime"]
        if "preTime" in command:
            pt = command["preTime"]
        if "spawnerLifeTime" in command:
            slt = command["spawnerLifeTime"]
        if "borderWidth" in command:
            bdw = command["borderWidth"] # Borderwidth can be both a str as an int, so we assure the correct type is passed on later

        spawner = projectile.BulletSpawner(screen=self.screen, spawningDelay=command["delay"], lifeTime = lt, spawnerLT = slt)

        if command["type"] == "pointExp":
            spawner.setSpawningPointExp(coords=(command["sX"], command["sY"]), dir = command["bDir"], speed = command["speed"], size=command["size"], borderWidth=str(bdw))
        if command["type"] == "expBExp":
            spawner.setSpawningExpBexp(coords=(command["sX"], command["sY"]), bulletPath = (command["bX"], command["bY"]), size=command["size"], borderWidth=str(bdw))
        if command["type"] == "bExpAbs":
            spawner.setSpawningBexpAbs(coords=(command["bX"], command["bY"]), size=command["size"], borderWidth=str(bdw))
        return spawner

    def parseBullet(self, command):
        lt = -1
        pt = 0
        bdw = 3
        if "bulletLifeTime" in command:
            lt = command["bulletLifeTime"]
        if "preTime" in command:
            pt = command["preTime"]
        if "borderWidth" in command:
            bdw = command["borderWidth"]

        bullet = projectile.Bullet(screen=self.screen, preTime = pt, lifeTime = lt)
        if command["type"] == "line":
            bullet.setBulletPathLine(pos = (command["x"], command["y"]), vel = (command["dx"], command["dy"]), size = command["size"], borderWidth = int(bdw))
        if command["type"] == "expRel":
            bullet.setBulletPathExpRel(pos = (command["x"], command["y"]), vel = (command["dx"], command["dy"]), size = command["size"], borderWidth = str(bdw))
        if command["type"] == "expAbs":
            bullet.setBulletPathExpAbs(pos = (command["x"], command["y"]), size = command["size"], borderWidth = str(bdw))

        return bullet

    def parsePattern(self, command):
        lt = -1
        pt = 0
        bdw = 3
        if "bulletLifeTime" in command:
            lt = command["bulletLifeTime"]
        if "preTime" in command:
            pt = command["preTime"]
        if "spawnerLifeTime" in command:
            slt = command["spawnerLifeTime"]

        pattern = projectile.BulletPattern(screen = self.screen, patternSize = command["count"])

        if command["type"] == "pointExp":
            pattern.setSpawningPointExp(coords=(command["sX"], command["sY"]), dir = command["bDir"], speed = command["speed"], size=command["size"], borderWidth=str(bdw))
        elif command["type"] == "expBExp":
            pattern.setSpawningExpBexp(coords=(command["sX"], command["sY"]), bulletPath = (command["bX"], command["bY"]), size=command["size"], borderWidth=str(bdw))
        elif command["type"] == "bExpAbs":
            pattern.setSpawningBexpAbs(coords=(command["bX"], command["bY"]), size=command["size"], borderWidth=str(bdw))

        return pattern

    def add_pattern(self, pattern, name):
        bulletManagers[name] = pattern

    def update(self, dt, player):
        self.time += dt*1000
        if len(self.que) > 0:
            while self.que[0][0] <= self.time:
                print(self.que[0])
                self.process(self.que[0])
                self.que.popleft()
                # Stop checking the que if it is empty now
                if len(self.que) == 0:
                    break

        # Update the integrated bulletManager used as parent for bullets created by a bullet command
        self.bulletManager.update(dt, player)
        # Since we decided to only remove bulletManagers once they have no more bullets left, we have to check for that
        deleteQue = set()
        for key, manager in self.bulletManagers.items():
            manager.update(dt, player)
            if manager.delete and len(manager.bullets) == 0:
                deleteQue.add(key)
        for item in deleteQue:
            self.bulletManagers.pop(item, True)

    def draw(self):
        self.bulletManager.draw()
        for key, manager in self.bulletManagers.items():
            manager.draw()
