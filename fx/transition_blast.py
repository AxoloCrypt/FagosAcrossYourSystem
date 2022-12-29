import pyxel


class TransitionBlast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1

    def update_blast(self):

        self.radius += 1

        if self.radius >= 100:
            self.radius = 0

        if self.radius == 0:
            return self.radius

        return 1

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)
