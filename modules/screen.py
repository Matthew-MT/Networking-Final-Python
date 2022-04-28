from math import floor
from networking import networking

class TileMap:
    tileSize: float
    matrix: list
    network: networking
    def __init__(self, initNetwork, initTileSize) -> None:
        self.tileSize = initTileSize
        self.network = initNetwork
        self.matrix = self.network.receivemap().tolist()
        return
    
    def checkCollision(self, rect: tuple) -> bool:
        offset = (
            rect[0] % self.tileSize,
            rect[1] % self.tileSize,
            (rect[0] + rect[2]) % self.tileSize,
            (rect[1] + rect[3]) % self.tileSize
        )

        tileIdx = (
            (
                floor((rect[0] - offset[0]) / self.tileSize),
                floor((rect[1] - offset[1]) / self.tileSize)
            ),
            (
                floor(((rect[0] + rect[2]) - offset[0]) / self.tileSize),
                floor(((rect[1] + rect[3]) - offset[0]) / self.tileSize)
            )
        )

        for idx in tileIdx:
            x, y = idx
            if self.matrix[x][y]:
                return True
        return False
