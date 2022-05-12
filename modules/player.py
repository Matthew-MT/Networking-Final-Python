from time import time
from random import randint
from modules.networking import networking
from modules.screen import TileMap

class Player:
    name: str = ""
    pos: tuple # (x, y)
    size: tuple # (w, h)
    otherPlayers: dict # {"<id0>": {"name": str, "position": (float, float)}, ...}
    network: networking
    tileMap: TileMap
    lastTime: int = time()
    score: int = 0

    xv: float = 0.0
    yv: float = 0.0
    mv: float = 768.0
    tv: float = 2048.0

    xa: float = 0.0
    ya: float = 1536.0
    ma: float = 1024.0

    def __init__(self, initSize, initNetwork, initTileMap) -> None:
        self.otherPlayers = {}
        self.size = initSize
        self.network = initNetwork
        self.otherPlayers = self.network.playerdata(self)
        self.tileMap = initTileMap
        self.respawn()
        pass

    def getView(self, scrW, scrH):
        center = (
            self.pos[0] + (self.size[0] / 2),
            self.pos[1] + (self.size[1] / 2)
        )
        origin = (center[0] - (scrW / 2), center[1] - (scrH / 2))
        return (origin[0], origin[1], origin[0] + scrW, origin[1] + scrH)

    def gameTick(self, curTime, up, left, right):
        self.network.playerdata(self)
        self.updateVelAndAcc(curTime, up, left, right)
        return

    def updateVelAndAcc(self, nextTime, up, left, right):
        scalar = nextTime - self.lastTime
        self.lastTime = nextTime
        mv = self.mv
        ma = self.ma
        tv = self.tv
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

        if up:
            ground = self.checkIfGround()
            if ground[0]:
                self.yv = -mv
            elif ground[1]:
                self.yv = -mv / 2.0
                self.xv = mv / 8.0
            elif ground[2]:
                self.yv = -mv / 2.0
                self.xv = -mv / 8.0
        
        self.yv = self.yv + (scalar * ya)

        xv = self.xv
        yv = self.yv

        if xv > mv:
            self.xv = mv
        elif xv < -mv:
            self.xv = -mv
        
        if yv > mv:
            self.yv = mv
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
