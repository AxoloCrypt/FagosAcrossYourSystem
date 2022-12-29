from enums.enums import Directions
from random import random
import pyxel
from entities.bullet import Bullet


# Support bacteria class from the final boss
class Bacteria:
    def __init__(self, x, y, direction=Directions.UP):
        self.x = x
        self.y = y
        self.direction = direction
        self.health = 60
        self.alive = True
        self.w = -24
        self.h = 16
        self.offset = int(random() * 120)

    def update(self, boss_bullet_list):
        # print((pyxel.frame_count + self.offset) % 96)
        # Bacteria movement in the x coordinate
        if (pyxel.frame_count + self.offset) % 96 < 60:
            self.x -= 1.0
        else:
            self.x += 1.0

        if self.x < pyxel.width / 2:
            self.x = (pyxel.width / 2)
        elif self.x > pyxel.width:
            self.x = pyxel.width

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.direction == Directions.DOWN:
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y, is_bacteria=True, is_diagonal_up=True
                    )
                )
            else:
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y, is_bacteria=True, is_diagonal_down=True
                    )
                )

            if self.health == 0:
                self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 112, 88, self.w, self.h)
