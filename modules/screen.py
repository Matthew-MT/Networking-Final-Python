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

        if self.matrix[tileIdx[0][0]][tileIdx[0][1]]\
        or self.matrix[tileIdx[0][0]][tileIdx[1][1]]\
        or self.matrix[tileIdx[1][0]][tileIdx[0][1]]\
        or self.matrix[tileIdx[1][0]][tileIdx[1][1]]:
            return True
        return False
