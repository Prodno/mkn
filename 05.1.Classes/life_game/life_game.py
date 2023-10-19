class LifeGame(object):
    """
    Class for Game life
    """

    def __init__(self, matrix):  # type: ignore
        self.cell = []
        for i in range(len(matrix)):
            self.cell.append([])
            for j in range(len(matrix[i])):
                self.cell[i].append(matrix[i][j])

    def _get_neighbours(self, i, j):  # type: ignore
        fish = 0
        shrimp = 0
        i1 = [i - 1, i, i + 1]
        j1 = [j - 1, j, j + 1]
        if i1[0] < 0:
            i1.remove(i1[0])
        if i1[-1] >= len(self.cell):
            i1.remove(i1[-1])
        if j1[0] < 0:
            j1.remove(j1[0])
        if j1[-1] >= len(self.cell[0]):
            j1.remove(j1[-1])
        for k in i1:
            for m in j1:
                if (k, m) != (i, j):
                    if self.cell[k][m] == 2:
                        fish += 1
                    if self.cell[k][m] == 3:
                        shrimp += 1
        return fish, shrimp

    @staticmethod
    def _get_next_state(cur, fish, shrimp):  # type: ignore
        if cur == 0:
            if fish == 3:
                return 2
            elif shrimp == 3:
                return 3
            else:
                return 0

        if cur == 2:
            if fish >= 4:
                return 0
            elif fish <= 1:
                return 0
            return 2

        if cur == 3:
            if shrimp >= 4:
                return 0
            elif shrimp <= 1:
                return 0
            else:
                return 3

        if cur == 1:
            return 1

    def get_next_generation(self):  # type: ignore
        new_field = []
        for i in range(len(self.cell)):
            new_field.append([])
            for j in range(len(self.cell[i])):
                fish_n, shrimp_n = self._get_neighbours(i, j)
                new_field[i].append(self._get_next_state(self.cell[i][j], fish_n, shrimp_n))
        self.cell = new_field
        return self.cell
