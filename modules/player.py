from curses import initscr
from math import floor
from random import randint
from networking import networking
from screen import TileMap

class Player:
    rect: tuple
    otherPlayers: dict
    network: networking
    tileMap: TileMap
    def __init__(self, initSize, initNetwork, initTileMap) -> None:
        self.rect = (0, 0, initSize[0], initSize[1])
        self.respawn()
        self.network = initNetwork
        self.otherPlayers = self.network.receivePlayerData()
        self.tileMap = initTileMap
        pass

    def gameTick(self):
        self.network.playerdata(self)
        return

    def respawn(self):
        openTiles = self.tileMap.openTiles
        tile = openTiles[randint(0, len(openTiles) - 1)]
        self.rect = (tile[0], tile[1], self.rect[2], self.rect[3])
