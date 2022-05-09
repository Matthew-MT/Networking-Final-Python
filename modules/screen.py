from math import floor
from networking import networking

class TileMap:
    tileSize: float
    matrix: list
    network: networking
    openTiles: list
    def __init__(self, initNetwork, initTileSize) -> None:
        self.tileSize = initTileSize
        self.network = initNetwork
        self.matrix = self.network.receivemap()
        for x in range(0, len(self.matrix)):
            for y in range(0, len(self.matrix[0])):
                if not self.matrix[x][y]:
                    self.openTiles.append(tuple(x, y))
        pass
    
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
                floor(((rect[0] + rect[2]) - offset[2]) / self.tileSize),
                floor(((rect[1] + rect[3]) - offset[3]) / self.tileSize)
            )
        )

        if tileIdx[0][0] < 0 or tileIdx[0][1] < 0\
        or tileIdx[1][0] > len(self.matrix)\
        or tileIdx[1][1] > len(self.matrix[0])\
        or self.matrix[tileIdx[0][0]][tileIdx[0][1]]\
        or self.matrix[tileIdx[0][0]][tileIdx[1][1]]\
        or self.matrix[tileIdx[1][0]][tileIdx[0][1]]\
        or self.matrix[tileIdx[1][0]][tileIdx[1][1]]:
            return True
        return False
    
    def getDrawScreen(self, rect: tuple):
        offset = (
            rect[0] % self.tileSize,
            rect[1] % self.tileSize,
            (rect[0] + rect[2]) % self.tileSize,
            (rect[1] + rect[3]) % self.tileSize
        )

        tileBounds = (
            (
                floor((rect[0] - offset[0]) / self.tileSize),
                floor((rect[1] - offset[1]) / self.tileSize)
            ),
            (
                floor((rect[2] - offset[2]) / self.tileSize),
                floor((rect[3] - offset[3]) / self.tileSize)
            )
        )

        if tileBounds[0][0] < 0:
            tileBounds[0][0] = 0
        if tileBounds[0][1] < 0:
            tileBounds[0][1] = 0
        if tileBounds[1][0] >= len(self.matrix):
            tileBounds[1][0] = len(self.matrix) - 1
        if tileBounds[1][1] >= len(self.matrix[0]):
            tileBounds[1][1] = len(self.matrix[0]) - 1

        drawMatrix: list = []

        for x in range(tileBounds[0][0], tileBounds[1][0]):
            drawMatrix.append([])
            for y in range(tileBounds[0][1], tileBounds[1][1]):
                fill: str = ""
                if self.matrix[x][y] == 1:
                    fill = "black"
                elif self.matrix[x][y] == 0:
                    fill = "white"
                drawMatrix[x].append(tuple(
                    (x * self.tileSize) - offset[0],
                    (y * self.tileSize) - offset[1],
                    ((x + 1) * self.tileSize) - offset[0],
                    ((y + 1) * self.tileSize) - offset[1],
                    fill
                ))
        return drawMatrix
