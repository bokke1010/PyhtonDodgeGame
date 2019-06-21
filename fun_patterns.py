spawners = []
import projectile
from base import *
def pattern_quadFan(scr):
    spawner = {}
    spawner["fan_pattern_1/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawner["fan_pattern_1/4"].setSpawningPointExp(coords=["0", str(h/2)], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)-1)", speed="90")
    spawner["fan_pattern_2/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawner["fan_pattern_2/4"].setSpawningPointExp(coords=[str(w), str(h/2)], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)+3)", speed="90")
    spawner["fan_pattern_3/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawner["fan_pattern_3/4"].setSpawningPointExp(coords=[str(w/2), "0"], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)+1)", speed="90")
    spawner["fan_pattern_4/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawner["fan_pattern_4/4"].setSpawningPointExp(coords=[str(w/2), str(h)], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)+5)", speed="90")
    spawners.append(spawner)

def pattern_star(scr, x, y, size):
    spawner = {}
    spawner["main"] = projectile.bulletSpawner(screen = scr, spawningDelay = 5, minSize = 3, maxSize = 8, borderWidth = 1, lifeTime = size/100)
    spawner["main"].setSpawningPointExp(coords=[str(x), str(y)], dir="random.random()*2*math.pi", speed="100")
    spawners.append(spawner)

def pattern_dualFan(scr):
    spawner = {}
    spawner["fan_pattern_1/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=35, minSize=10)
    spawner["fan_pattern_1/2"].setSpawningPointExp(coords=["0", str(h/2)], dir=" 0.25 * math.pi * (math.sin(math.pi * t)-1)", speed="90")
    spawner["fan_pattern_2/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=35, minSize=10)
    spawner["fan_pattern_2/2"].setSpawningPointExp(coords=["w", str(h/2)], dir=" 0.25 * math.pi * (math.sin(math.pi * t)+3)", speed="90")
    spawners.append(spawner)



def pattern_spiral(scr, coords: tuple = ("w/2", "h/2")):
    spawner = {}
    spawner["central_spiral"] = projectile.bulletSpawner(screen=scr, spawningDelay=50, minSize=12)
    spawner["central_spiral"].setSpawningPointExp(coords=coords, dir="t*0.5*math.pi", speed="90" )
    spawners.append(spawner)

def pattern_dodgeball(scr):
    spawner = {}
    spawner["line"] = projectile.bulletSpawner(spawningDelay = 10, minSize = 20, lifeTime =w/1900, screen = scr)
    spawner["line"].setSpawningExp(["40*(c%(w/40))+10","h-40"],["0","0"])
    spawner["balls"] = projectile.bulletSpawner(spawningDelay = 120, minSize = 24, maxSize = 36, screen = scr)
    spawner["balls"].setSpawningBox([0,0,w,0],[0,60,0,80])
    spawner["invisField"] = projectile.bulletSpawner(spawningDelay = 80, minSize = 100, screen = scr, visible = False)
    spawner["invisField"].setSpawningBox([0,0,0,h-120],[100,0,100,0])
    spawners.append(spawner)

def pattern_sudden(scr, speed):
    spawner = {}
    spawner["main"] = projectile.bulletSpawner(spawningDelay = 50/speed, minSize = 32, maxSize = 36, screen = scr, preTime = 1, lifeTime = 4)
    spawner["main"].setSpawningBox([0,0,w,h],[0,0,0,0])
    spawners.append(spawner)

def pattern_enclosing_circle(scr, speed = 1):
    spawner = {}
    spawner["encl_circle"] = projectile.bulletSpawner(screen=scr, spawningDelay=80/speed, minSize=14)
    spawner["encl_circle"].setSpawningPointExp(coords=["w*0.5*(1+math.cos(t*math.pi*{}))".format(speed),"h*0.5*(1+math.sin(t*math.pi*{}))".format(speed)], dir="t*math.pi*{}+math.pi".format(speed), speed="120" )
    spawners.append(spawner)


def pattern_dual_spiral(scr, coords: tuple = ("w/2", "h/2")):
    spawner = {}
    spawner["central_spiral_1/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=90, minSize=10)
    spawner["central_spiral_1/2"].setSpawningPointExp(coords=coords, dir="t*0.35*math.pi", speed="90" )
    spawner["central_spiral_2/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=90, minSize=10)
    spawner["central_spiral_2/2"].setSpawningPointExp(coords=coords, dir="t*0.35*math.pi + math.pi", speed="90" )
    spawners.append(spawner)

def pattern_fast_spin(scr):
    pattern_enclosing_circle(scr, speed=1.8)
    pattern_star(scr, w, h, 250)
    pattern_star(scr, 0, h, 250)
    pattern_star(scr, w, 0, 250)
    pattern_star(scr, 0, 0, 250)

def add_pattern(pattern):
    spawners.append({1:pattern})

def updateDraw(dt, player):
    for spawner in spawners:
        for pat in spawner:
            spawner[pat].draw()
            spawner[pat].update(dt, player)
def draw():
    for spawner in spawners:
        for pat in spawner:
            spawner[pat].draw()
