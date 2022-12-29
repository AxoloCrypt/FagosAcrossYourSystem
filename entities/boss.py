from random import random
import pyxel
from entities.bullet import Bullet
import time


# End level Boss class
class Boss:
    def __init__(self, x, y, speed=0):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = 200
        self.alive = True
        self.w = 24
        self.h = 32
        self.offset = int(random() * 100)

    def update(self, current_level, boss_bullet_list, screen_width=0):
        # Boss movement
        if (pyxel.frame_count + self.offset) % 96 < 60:
            self.y -= self.speed
        else:
            self.y += self.speed

        # Boss attacks
        if current_level == 0:
            # Shoot two bullets when the player shoots
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(2, 24)
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 48 / 2, is_boss=True
                    )
                )
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 8 / 2, is_boss=True
                    )
                )
        if current_level == 1:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(2, 24)
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 48 / 2, is_boss=True
                    )
                )
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 8 / 2, is_boss=True
                    )
                )
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 72 / 2, is_boss=True
                    )
                )

                boss_bullet_list.append(
                    Bullet(
                        screen_width / 2, 9.0, is_boss=True, is_vertical=True
                    )
                )
                boss_bullet_list.append(
                    Bullet(
                        5.0, 9.0, is_boss=True, is_vertical=True
                    )
                )
        if current_level == 2:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(2, 24)
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 48 / 2, is_boss=True
                    )
                )
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 9 / 2, is_boss=True
                    )
                )
                boss_bullet_list.append(
                    Bullet(
                        self.x + (self.w + 8) / 2, self.y + 72 / 2, is_boss=True
                    )
                )

                boss_bullet_list.append(
                    Bullet(
                        5.0, 9.0, is_boss=True, is_vertical=True
                    )
                )

        if self.health == 0:
            time.sleep(1)
            self.health = -10

        if self.health == -10:
            self.alive = False

        # Check if the character it's out of bounces
        # if True keep the character in the selected position
        if self.y < 8.0:
            self.y = 8.0
        elif self.y > 96.0:
            self.y = 96.0

    # param: int
    # draw the boss sprite depending on the current level
    def draw(self, current_level):
        sprite_x = 0
        sprite_y = 0
        if current_level == 0:
            sprite_x = 232
            sprite_y = 24
        if current_level == 1:
            sprite_x = 144
            sprite_y = 40
            self.h = 24
        if current_level == 2:
            sprite_x = 216
            sprite_y = 112
            self.w = 16
        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, self.w, self.h)

        if self.health == 0:
            if current_level == 0:
                pyxel.blt(self.x, self.y, 0, 0, 152, 16, 32)
            elif current_level == 1:
                pyxel.blt(self.x, self.y, 0, 216, 192, 16, 32)
            elif current_level == 2:
                pyxel.blt(self.x, self.y, 0, 240, 192, 16, 32)
