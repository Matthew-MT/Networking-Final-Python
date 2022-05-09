from curses import initscr
from math import floor
from random import randint
from networking import networking
from screen import TileMap

class Player:
    name: str = ""
    rect: tuple # (x, y, w, h)
    otherPlayers: dict # {"<id0>": {"name": str, "position": (float, float)}, ...}
    network: networking
    tileMap: TileMap
    def __init__(self, initSize, initNetwork, initTileMap) -> None:
        self.rect = (0, 0, initSize[0], initSize[1])
        self.respawn()
        self.network = initNetwork
        self.otherPlayers = self.network.receivePlayerData()
        self.tileMap = initTileMap
        pass

    def getView(self, scrW, scrH):
        center = (self.rect[0] + (self.rect[2] / 2), self.rect[1] + (self.rect[3] / 2))
        origin = (center[0] - (scrW / 2), center[1] - (scrH / 2))
        return (origin[0], origin[1], origin[0] + scrW, origin[1] + scrH)

    def gameTick(self):
        self.network.playerdata(self)
        return

    def respawn(self):
        openTiles = self.tileMap.openTiles
        tile = openTiles[randint(0, len(openTiles) - 1)]
        self.rect = (tile[0], tile[1], self.rect[2], self.rect[3])
