from cmath import sqrt
from time import time
from random import randint
from modules.networking import networking
from modules.screen import TileMap

class Player:
    name: str = ""
    pos: tuple # (x, y)
    size: tuple # (w, h)
    otherPlayers: dict # {"<id0>": {"name": str, "position": (float, float)}, ...}
    bullets: list # [{"pos": (x, y), "vel": (xv, yv)}, ...]
    network: networking
    tileMap: TileMap
    lastTime: int = time()
    score: int = 0
    cooldown: int = 200
    remCool: int = 0

    xv: float = 0.0
    yv: float = 0.0
    mv: float = 512.0
    tv: float = 1536.0

    xa: float = 0.0
    ya: float = 1536.0
    ma: float = 1024.0

    def __init__(self, initSize, initNetwork, initTileMap) -> None:
        self.otherPlayers = {}
        self.size = initSize
        self.network = initNetwork
        self.tileMap = initTileMap
        self.respawn()
        self.network.playerdata(self)
        pass

    def getView(self, scrW, scrH):
        center = (
            self.pos[0] + (self.size[0] / 2),
            self.pos[1] + (self.size[1] / 2)
        )
        origin = (center[0] - (scrW / 2), center[1] - (scrH / 2))
        return (origin[0], origin[1], origin[0] + scrW, origin[1] + scrH)

    def gameTick(self, curTime, up, left, right, click, target):
        self.network.playerdata(self)
        self.updateVelAndAcc(curTime, up, left, right)
        if self.remCool <= 0 and click:
            self.shoot(target)
            self.remCool = self.cooldown
        elif self.remCool > 0:
            self.remCool = self.remCool - (curTime - self.lastTime) * 1000
        self.lastTime = curTime
        return

    def updateVelAndAcc(self, nextTime, up, left, right):
        scalar = nextTime - self.lastTime
        mv = self.mv
        ma = self.ma
        tv = self.tv
        jv = tv / 1.84
        fa = ma * scalar

        if left and not right:
            self.xa = -ma
        elif right and not left:
            self.xa = ma
        else:
            self.xa = 0.0
            if self.xv > fa:
                self.xv = self.xv - fa
            elif self.xv > 0.0:
                self.xv = 0.0
            elif self.xv < -fa:
                self.xv = self.xv + fa
            elif self.xv < 0.0:
                self.xv = 0.0

        xa = self.xa
        ya = self.ya

        self.xv = self.xv + (scalar * xa)

        re = True
        if up:
            ground = self.checkIfGround()
            if ground[0]:
                self.yv = -jv
                re = False
            elif ground[1]:
                self.yv = -jv / 1.6
                self.xv = mv / 2.4
                re = False
            elif ground[2]:
                self.yv = -jv / 1.6
                self.xv = -mv / 2.4
                re = False
        
        if re:
            self.yv = self.yv + (scalar * ya)

        xv = self.xv
        yv = self.yv

        if xv > mv:
            self.xv = mv
        elif xv < -mv:
            self.xv = -mv
        
        if yv > jv:
            self.yv = jv
        elif yv < -tv:
            self.yv = -tv
        
        xv = (self.xv * scalar)
        yv = (self.yv * scalar)

        newX = [self.pos[0] + xv, self.pos[1]]
        newY = [self.pos[0], self.pos[1] + yv]
        
        while self.tileMap.checkCollision(newX, self.size)\
        and abs(xv) > 0.001:
            xv = xv / 2.0
            self.xv = self.xv / 2.0
            newX[0] = newX[0] - xv

        if abs(xv) <= 0.001:
            self.xv = 0.0
            newX[0] = self.pos[0]

        while self.tileMap.checkCollision(newY, self.size)\
        and abs(yv) > 0.001:
            yv = yv / 2.0
            self.yv = self.yv / 2.0
            newY[1] = newY[1] - yv

        if abs(yv) <= 0.001:
            self.yv = 0.0
            newY[1] = self.pos[1]

        self.pos = (newX[0], newY[1])
        return
    
    def shoot(self, target):
        if len(self.bullets) >= 256:
            return
        normVect = (target / sqrt((target[0] * target[0]) + (target[1] + target[1]))) * 4096
        self.bullets.append({
            "pos": self.pos,
            "vel": normVect
        })
        return
    
    def updateBullets(self):
        for bullet in self.bullets:
            pos = bullet["pos"]
            vel = bullet["vel"]

        return
    
    def checkIfGround(self):
        return (
            self.tileMap.checkCollision(self.pos, (self.size[0], self.size[1] + 1)),
            self.tileMap.checkCollision((self.pos[0] - 1, self.pos[1]), (self.size[0] + 1, self.size[1])),
            self.tileMap.checkCollision(self.pos, (self.size[0] + 1, self.size[1]))
        )

    def respawn(self):
        openTiles = self.tileMap.openTiles
        tileSize = self.tileMap.tileSize
        tile = openTiles[randint(0, len(openTiles) - 1)]
        tile = (0, 0)
        self.pos = (
            (tile[0] * tileSize) + ((tileSize - self.size[0]) / 2),
            (tile[1] * tileSize) + ((tileSize - self.size[1]) / 2)
        )
        return
