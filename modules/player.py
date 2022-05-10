from time import time
from random import randint
from networking import networking
from screen import TileMap

class Player:
    name: str = ""
    pos: tuple # (x, y)
    size: tuple # (w, h)
    otherPlayers: dict # {"<id0>": {"name": str, "position": (float, float)}, ...}
    network: networking
    tileMap: TileMap
    lastTime: int = time()

    xv: float = 0.0
    yv: float = 0.0
    mv: float = 10.0

    xa: float = 0.0
    ya: float = 0.0
    ma: float = 2.0

    def __init__(self, initSize, initNetwork, initTileMap) -> None:
        self.pos = (0, 0)
        self.size = (initSize[0], initSize[1])
        self.respawn()
        self.network = initNetwork
        self.otherPlayers = self.network.receivePlayerData()
        self.tileMap = initTileMap
        pass

    def getView(self, scrW, scrH):
        center = (self.pos[0] + (self.size[0] / 2), self.pos[1] + (self.size[1] / 2))
        origin = (center[0] - (scrW / 2), center[1] - (scrH / 2))
        return (origin[0], origin[1], origin[0] + scrW, origin[1] + scrH)

    def gameTick(self, curTime, up, left, right):
        self.network.playerdata(self)
        self.updateVelAndAcc(curTime, up, left, right)
        return

    def updateVelAndAcc(self, nextTime, up, left, right):
        scalar = nextTime - self.lastTime
        if not (left and right):
            if left:
                self.xa = -self.ma
            elif right:
                self.xa = self.ma
            else:
                self.xa = 0
        if up and self.checkIfGround():
            self.ya = -self.ma
        else:
            self.ya = self.ma

        self.xv = self.xv + self.xa
        self.yv = self.yv + self.ya

        xv = self.xv
        yv = self.yv
        mv = self.mv

        if xv > mv:
            self.xv = mv
        elif xv < -mv:
            self.xv = -mv
        
        if yv > mv:
            self.yv = mv
        elif yv < -mv:
            self.yv = -mv
        
        newPos = [self.pos[0] + self.xv, self.pos[1] + self.yv]
        
        while self.tileMap.checkCollision(newPos)\
        and abs(self.xv) > 0.1:
            self.xv = self.xv / 2.0
            newPos[0] = newPos[0] - self.xv

        while self.tileMap.checkCollision(newPos)\
        and abs(self.yv) > 0.1:
            self.yv = self.yv / 2.0
            newPos[1] = newPos[1] - self.yv

        if abs(self.xv) <= 0.1:
            newPos[0] = 0.0
        if abs(self.yv) <= 0.1:
            newPos[1] = 0.0

        self.pos = newPos
        return
    
    def checkIfGround(self):
        return self.tileMap.checkCollision((self.pos[0], self.pos[1] + 1, self.size[0], self.size[1]))

    def respawn(self):
        openTiles = self.tileMap.openTiles
        tile = openTiles[randint(0, len(openTiles) - 1)]
        self.pos = (tile[0], tile[1])
        return
