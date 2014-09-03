Class SmoothWalls:

    def __init__(self, base):
        self.base = base
        self.walls = []
        self._findWalls

    def _findWalls(self):
        relevant = ["45 tile", "315 tile", "135 tile", "225 tile", "wall"]
        for i in range(len(base)):
            y_cor = i
            for j in range(len(base)):
                x_cor = j
                if base[i][j] in relevant:
                    self.walls.append((base[i][j], x_cor, y_cor))




















































