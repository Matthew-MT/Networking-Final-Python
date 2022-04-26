from ast import MatchOr


class TileMap:
    def __init__(self, width, height) -> None:
        self.matrix = []
        temp: list = []
        for i in range(0, height):
            temp.insert(i, 0)
        for i in range(0, width):
            self.matrix.insert(i, temp.copy())
        return
    matrix: list = []
