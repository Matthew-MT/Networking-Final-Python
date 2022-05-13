from math import floor, ceil
from modules.networking import networking

class TileMap:
    tileSize: float
    matrix: list
    network: networking
    openTiles: list
    def __init__(self, initNetwork, initTileSize) -> None:
        self.tileSize = initTileSize
        self.network = initNetwork
        self.matrix = self.network.receivemap()
        self.openTiles = []
        for x in range(0, len(self.matrix)):
            for y in range(0, len(self.matrix[0])):
                if not self.matrix[x][y]:
                    self.openTiles.append((x, y))
        pass
    
    def checkCollision(self, pos: tuple, size: tuple) -> bool:
        tileIdx = (
            (
                floor(pos[0] / self.tileSize),
                floor(pos[1] / self.tileSize)
            ),
            (
                floor((pos[0] + size[0]) / self.tileSize),
                floor((pos[1] + size[1]) / self.tileSize)
            )
        )

        return tileIdx[0][0] < 0\
            or tileIdx[0][1] < 0\
            or tileIdx[1][0] > len(self.matrix) - 1\
            or tileIdx[1][1] > len(self.matrix[0]) - 1\
            or self.matrix[tileIdx[0][0]][tileIdx[0][1]]\
            or self.matrix[tileIdx[0][0]][tileIdx[1][1]]\
            or self.matrix[tileIdx[1][0]][tileIdx[0][1]]\
            or self.matrix[tileIdx[1][0]][tileIdx[1][1]]
    
    def getDrawScreen(self, rect: tuple):
        offset = (
            rect[0] % self.tileSize,
            rect[1] % self.tileSize
        )

        tileBounds = [
            [
                floor(rect[0] / self.tileSize),
                floor(rect[1] / self.tileSize)
            ],
            [
                ceil(rect[2] / self.tileSize),
                ceil(rect[3] / self.tileSize)
            ]
        ]

        drawMatrix: list = []

        minX = tileBounds[0][0]
        minY = tileBounds[0][1]

        bounds = (
            (
                max(minX, 0),
                min(tileBounds[1][0], len(self.matrix))
            ),
            (
                max(minY, 0),
                min(tileBounds[1][1], len(self.matrix[0]))
            )
        )

        for x in range(bounds[0][0], bounds[0][1]):
            drawMatrix.append([])
            for y in range(bounds[1][0], bounds[1][1]):
                fill: str = ""
                if self.matrix[x][y] == 1:
                    fill = "black"
                elif self.matrix[x][y] == 0:
                    fill = "white"
                
                normX = x - minX
                normY = y - minY

                drawMatrix[min(x, normX)].append((
                    (normX * self.tileSize) - offset[0],
                    (normY * self.tileSize) - offset[1],
                    ((normX + 1) * self.tileSize) - offset[0],
                    ((normY + 1) * self.tileSize) - offset[1],
                    fill
                ))
        return drawMatrix
