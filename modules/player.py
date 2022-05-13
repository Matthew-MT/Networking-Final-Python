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
    bullets: list = [] # [{"pos": (x, y), "vel": (xv, yv)}, ...]
    otherBullets: list # [(x, y), ...]
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
            self.pos[0] + (self.size[0] / 2.0),
            self.pos[1] + (self.size[1] / 2.0)
        )
        origin = (center[0] - (scrW / 2.0), center[1] - (scrH / 2.0))
        return (origin[0], origin[1], origin[0] + scrW, origin[1] + scrH)
    
    def getDrawnBullets(self, scrW, scrH):
        center = (
            self.pos[0] + (self.size[0] / 2.0),
            self.pos[1] + (self.size[1] / 2.0)
        )
        origin = (center[0] - (scrW / 2.0), center[1] - (scrH / 2.0))
        alter = (origin[0] + scrW, origin[1] + scrH)
        bullets: list = []
        for bulletData in self.bullets:
            bullet = bulletData["pos"]
            if origin[0] < bullet[0] and bullet[0] < alter[0]\
            and origin[1] < bullet[1] and bullet[1] < alter[1]:
                bullets.append((bullet[0] - origin[0], bullet[1] - origin[1]))
        for bullet in self.otherBullets:
            if origin[0] < bullet[0] and bullet[0] < alter[0]\
            and origin[1] < bullet[1] and bullet[1] < alter[1]:
                bullets.append((bullet[0] - origin[0], bullet[1] - origin[1]))
        return bullets
    
    def getDrawnOtherPlayers(self, scrW, scrH):
        center = (
            self.pos[0] + (self.size[0] / 2.0),
            self.pos[1] + (self.size[1] / 2.0)
        )
        origin = (center[0] - (scrW / 2.0), center[1] - (scrH / 2.0))
        alter = (origin[0] + scrW, origin[1] + scrH)
        players: list = []
        for player in self.otherPlayers.values():
            pos: tuple
            try:
                pos = player["pos"]
            except:
                pos = (0.0, 0.0)
            if origin[0] - self.size[0] <= pos[0] and pos[0] <= alter[0]\
            and origin[1] - self.size[1] <= pos[1] and pos[1] <= alter[1]:
                players.append({
                    "pos": (
                        pos[0] - origin[0],
                        pos[1] - origin[1]
                    ),
                    "name": player["name"]
                })
        return players

    def gameTick(self, curTime, up, left, right, click, target, scrW, scrH):
        self.network.playerdata(self)
        self.updateVelAndAcc(curTime, up, left, right)
        self.updateBullets(curTime)
        if self.remCool <= 0 and click:
            self.shoot((target[0] - (scrW / 2.0), target[1] - (scrH / 2.0)))
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
        norm = sqrt((target[0] * target[0]) + (target[1] * target[1])).real
        normVect = ((target[0] / norm) * 1024, (target[1] / norm) * 1024)
        self.bullets.append({
            "pos": (self.pos[0] + (self.size[0] / 2.0), self.pos[1] + (self.size[1] / 2.0)),
            "vel": normVect
        })
        return
    
    def updateBullets(self, nextTime):
        scalar = nextTime - self.lastTime
        r: float = (self.size[0] * self.size[0]) + (self.size[1] * self.size[1])
        sx, sy = self.size
        ox = sx / 2.0
        oy = sy / 2.0

        toDel: list = []

        for i in range(0, len(self.bullets)):
            bullet = self.bullets[i]
            collided = False
            bx, by = bullet["pos"]
            vx, vy = bullet["vel"]
            vx = vx * scalar
            vy = vy * scalar
            traveled = (vx * vx) + (vy * vy)
            for id in self.otherPlayers.keys():
                player = self.otherPlayers[id]
                px, py = player["pos"]
                cx = px + ox
                cy = py + oy
                ax = px + sx
                ay = py + sy
                dist = ((cx - bx) * (cx - bx)) + ((cy - by) * (cy - by))
                if dist <= traveled + r:
                    if (-0.1 <= vx and vx <= 0.1) or (-0.1 <= vy and vy <= 0.1):
                        if abs(bx - cx) <= ox and abs(by - cy) < oy:
                            self.network.sendkillsignal(id)
                            self.score += 1
                            collided = True
                    else:
                        x = (((((vy * bx) / vx) + ((vx * cx) / vy)) - by) + cy)\
                            / ((vy / vx) + (vx / vy))
                        y = ((vy / vx) * (x - bx)) + by

                        if px <= x and x <= ax\
                        and py <= y and y <= ay:
                            self.network.sendkillsignal(id)
                            self.score += 1
                            collided = True
            
            if self.tileMap.checkCollision((bx, by), (0.0, 0.0)):
                collided = True

            if collided:
                toDel.append(i)
            else:
                self.bullets[i]["pos"] = (bx + vx, by + vy)
        
        if len(toDel) > 0:
            c = 0
            newBullets: list = []
            for i in range(0, len(self.bullets)):
                if c < len(toDel):
                    if i < toDel[c]:
                        newBullets.append(self.bullets[i])
                    elif i >= toDel[c]:
                        c += 1
                else:
                    newBullets.append(self.bullets[i])
            self.bullets = newBullets

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
        self.pos = (
            (tile[0] * tileSize) + ((tileSize - self.size[0]) / 2),
            (tile[1] * tileSize) + ((tileSize - self.size[1]) / 2)
        )
        return
