import pyxel
from enums.enums import GameState

BULLET_SPEED = 2.5
BOSS_BULLET_SPEED = 2.0
SCREEN_WIDTH = 192


class Bullet:
    def __init__(self, x, y, is_bacteria=False,
                 is_boss=False, is_vertical=False, is_diagonal_up=False, is_diagonal_down=False):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.alive = True
        self.is_bacteria = is_bacteria
        self.is_boss = is_boss
        self.is_vertical = is_vertical
        self.is_diagonal_up = is_diagonal_up
        self.is_diagonal_down = is_diagonal_down
        self.bullet_speed = BOSS_BULLET_SPEED if self.is_boss else BULLET_SPEED
        self.SCREEN_WIDTH = SCREEN_WIDTH

    def update(self):
        if self.is_bacteria and self.is_diagonal_up:
            self.x -= 1.0
            self.y -= 1.0

            if self.x + self.w + 1 < 0:
                self.alive = False
        elif self.is_bacteria and self.is_diagonal_down:
            self.x -= 1.0
            self.y += 1.0

            if self.x + self.w + 1 < 0:
                self.alive = False

        elif self.is_boss and not self.is_vertical:
            self.x -= self.bullet_speed
            if self.x + self.w + 1 < 0:
                self.alive = False
        elif self.is_boss and self.is_vertical:
            self.y += 1.0
            if self.y > 104.0:
                self.alive = False
        else:
            self.x += self.bullet_speed
            if self.x + self.w + 1 > self.SCREEN_WIDTH:
                self.alive = False

    # param: int, enum
    # draw the bullet sprite depending on the current level and game state
    def draw(self, current_level, game_state):
        sprite_x = 0
        sprite_y = 0

        if current_level == 0 and game_state == GameState.RUNNING:
            sprite_x = 208
            sprite_y = 56
        elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
            sprite_x = 216
            sprite_y = 56
        if current_level == 1 and game_state == GameState.RUNNING:
            sprite_x = 208
            sprite_y = 64
        elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
            sprite_x = 216
            sprite_y = 64
        if current_level == 2 and game_state == GameState.RUNNING:
            sprite_x = 224
            sprite_y = 64
        elif current_level == 2 and game_state == GameState.BOSS_FIGHT:
            sprite_x = 224
            sprite_y = 56

        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, self.w, self.h)
        if self.is_bacteria:
            pyxel.blt(self.x, self.y, 0, 48, 8, self.w, self.h)
        if self.is_boss:
            pyxel.blt(self.x, self.y, 0, 40, 0, self.w, self.h)
            if current_level == 1:
                pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h)
            if current_level == 2:
                pyxel.blt(self.x, self.y, 0, 48, 8, self.w, self.h)
