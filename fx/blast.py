import pyxel


class Blast:
    def __init__(self, x, y, blast_list=None):
        self.x = x
        self.y = y
        self.radius = 1
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1
        if self.radius > 8:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 8)
        pyxel.circb(self.x, self.y, self.radius, 2)
