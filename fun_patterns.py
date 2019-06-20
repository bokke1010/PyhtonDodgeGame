spawners = {}
import projectile
def pattern_quadFan(scr):
    spawners["fan_pattern_1/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawners["fan_pattern_1/4"].setSpawningPointExp(coords=["0", "h/2"], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)-1)", speed="90")
    spawners["fan_pattern_2/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawners["fan_pattern_2/4"].setSpawningPointExp(coords=["w", "h/2"], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)+3)", speed="90")
    spawners["fan_pattern_3/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawners["fan_pattern_3/4"].setSpawningPointExp(coords=["w/2", "0"], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)+1)", speed="90")
    spawners["fan_pattern_4/4"] = projectile.bulletSpawner(screen=scr, spawningDelay=30, minSize=8)
    spawners["fan_pattern_4/4"].setSpawningPointExp(coords=["w/2", "h"], dir=" 0.25 * math.pi * (math.sin(math.pi * t * 0.7)+5)", speed="90")

def pattern_dualFan(scr):
    spawners["fan_pattern_1/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=35, minSize=10)
    spawners["fan_pattern_1/2"].setSpawningPointExp(coords=["0", "h/2"], dir=" 0.25 * math.pi * (math.sin(math.pi * t)-1)", speed="90")
    spawners["fan_pattern_2/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=35, minSize=10)
    spawners["fan_pattern_2/2"].setSpawningPointExp(coords=["w", "h/2"], dir=" 0.25 * math.pi * (math.sin(math.pi * t)+3)", speed="90")


def pattern_central_spiral(scr):
    spawners["central_spiral"] = projectile.bulletSpawner(screen=scr, spawningDelay=50, minSize=12)
    spawners["central_spiral"].setSpawningPointExp(coords=["w/2","h/2"], dir="t*0.5*math.pi", speed="90" )

def pattern_enclosing_circle(scr):
    spawners["encl_circle"] = projectile.bulletSpawner(screen=scr, spawningDelay=80, minSize=14)
    spawners["encl_circle"].setSpawningPointExp(coords=["w*0.5*(1+math.cos(t*math.pi*1))","h*0.5*(1+math.sin(t*math.pi*1))"], dir="t*math.pi*1+math.pi", speed="120" )

def pattern_dual_central_spiral(scr):
    spawners["central_spiral_1/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=90, minSize=10)
    spawners["central_spiral_1/2"].setSpawningPointExp(coords=["w/2","h/2"], dir="t*0.35*math.pi", speed="90" )
    spawners["central_spiral_2/2"] = projectile.bulletSpawner(screen=scr, spawningDelay=90, minSize=10)
    spawners["central_spiral_2/2"].setSpawningPointExp(coords=["w/2","h/2"], dir="t*0.35*math.pi + math.pi", speed="90" )


def updateDraw(dt, player):
    for pat in spawners:
        spawners[pat].draw()
        spawners[pat].update(dt, player)
def draw():
    for pat in spawners:
        spawners[pat].draw()
