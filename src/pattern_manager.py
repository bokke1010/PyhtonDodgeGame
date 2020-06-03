import json
import projectile
from base import *
from collections import deque

#TODO: So I really need to implement a area/formula bullet time to prevent
#      needing to close in borders with 100s of expAbs bullets (which all require
#      their position to be recalculated each frame)

class PatternManager():

    def __init__(self, screen):
        self.screen = screen
        self.bulletManagers = {}
        self.que = deque()
        self.time = 0
        self.lc = 0

    def loadJson(self, fileName):
        with open(fileName) as json_file:
            self.data = json.load(json_file)
        self.levelNames = list(self.data)
        self.levelCount = len(self.data)
        return self.levelNames

    def startLevel(self, level):
        data = self.data[level]
        scheduledTime = self.time
        for item in data:
            for key, value in item.items():
                if key == "spawner":
                    for name, command in value.items():
                        self._queAppend(Data("spw", time = scheduledTime, name = self._formatName(name), command = command))
                elif key == "pattern":
                    for name, command in value.items():
                        self._queAppend(Data("pat", time = scheduledTime, name = self._formatName(name), command = command))
                elif key == "trigger":
                    for name in value:
                        self._queAppend(Data("trg", time = scheduledTime, name = self._formatName(name)))
                elif key == "wait":
                    scheduledTime += value
                elif key == "del":
                    for name in value:
                        self._queAppend(Data("del", time = scheduledTime, name = self._formatName(name)))

        # Unique identifier to prevent levels overwriting each other
        self.lc += 1

    def _formatName(self, name: str):
        # lc is a attribute, and should still be the correct value when this is called
        return name + ":" + str(self.lc)

    def _queAppend(self, command: Data):
        """Internal function to append items to the que"""
        if len(self.que) > 0:
            # Add a item inside the que by looping back through the que
            # We want to work with index, so we take lenght - 1
            # since the if statement already checks for the last item, we subtract 1 more
            i = len(self.que)

            # If the trigger timestamp of our item is lower than the earlier que
            # item, we decrease the index to match that item
            while (i > 0 and command.time < self.que[i-1].time):
                i -= 1
            self.que.insert(i, command)
        else:
            self.que.append(command)

    def process(self, command):
        # command.time is timing, often not required
        # command.type is instruction
        # command.name, command.command etc. provide extra information
        # etc.
        if command.type == "spw":
            spawner = self.parseSpawner(command.command)
            self.bulletManagers[command.name] = spawner
        elif command.type == "pat":
            pattern = self.parsePattern(command.command)
            self.bulletManagers[command.name] = pattern
        elif command.type == "trg":
            self.bulletManagers[command.name].trigger()
        elif command.type == "del":
            self.bulletManagers[command.name].setDelete()
        elif command.type == "end":
            self.bulletManagers = {}
            return True
        else:
            print("command <" + command.type + "> not recognized")


    def parseSpawner(self, command):
        shape = BULLETSHAPE.BALL if "size" in command else BULLETSHAPE.BOX
        spawner = projectile.BulletSpawner(screen=self.screen, spawningDelay=command["delay"]).setBulletPattern(shape, **command)
        spawner.setBulletStyle(**command)
        return spawner

    def parsePattern(self, command):
        shape = BULLETSHAPE.BALL if "size" in command else BULLETSHAPE.BOX
        pattern = projectile.BulletPattern(screen = self.screen).setBulletPattern(shape, **command)
        pattern.setBulletStyle(**command)
        return pattern

    def add_pattern(self, pattern, name):
        bulletManagers[name] = pattern

    def update(self, dt, player):
        self.time += dt
        while len(self.que) > 0:
            if self.que[0].time <= self.time:
                print(self.que[0])
                self.process(self.que[0])
                self.que.popleft()
            else:
                break

        # Since we decided to only remove bulletManagers once they have no more bullets left, we have to check for that
        deleteQue = set()
        events = Que()
        for key, manager in self.bulletManagers.items():
            events.merge(manager.update(dt, player))
            log(events)
            if manager.getDelete():
                deleteQue.add(key)
        for key in deleteQue:
            self.bulletManagers.pop(key, True)
        return events

    def draw(self):
        for key, manager in self.bulletManagers.items():
            manager.draw()
