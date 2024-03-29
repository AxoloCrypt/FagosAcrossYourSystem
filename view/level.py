import pyxel
from enums.enums import GameState


class Level:
    def __init__(self, screen_width, screen_height, speed=0):
        self.x = 0
        self.tm = 0
        self.u = 0
        self.v = 0
        self.w = screen_width
        self.h = screen_height
        self.speed = speed

    def update(self, state):
        # Move the level tilemap and repeat it constantly while the game is in GameState.Running
        if state != GameState.BOSS_FIGHT and state == GameState.RUNNING:
            self.x -= self.speed
            repeat_width = self.w / 2
            if 0 - self.x > repeat_width:
                self.x = 0

    def draw(self, level, state):

        if state == GameState.RUNNING:
            pyxel.bltm(self.x, 0, level, self.u, self.v, self.w * 2, self.h)
        elif state == GameState.TITTLE:
            pyxel.bltm(0, 0, 3, self.u, self.v, self.w, self.h)
        elif level == 0 and state == GameState.LEVEL_COMPLETE:
            pyxel.bltm(0, 0, 4, self.u, self.v, self.w, self.h)
        elif level == 1 and state == GameState.LEVEL_COMPLETE:
            pyxel.bltm(0, 0, 5, self.u, self.v, self.w, self.h)
        elif state == GameState.GAME_OVER:
            pyxel.bltm(0, 0, 6, self.u, self.v, self.w, self.h)
        elif state == GameState.COMPLETED:
            pyxel.bltm(0, 0, 7, self.u, self.v, self.w, self.h)

        if state == GameState.BOSS_FIGHT:
            pyxel.bltm(0, 0, level, 580, 0, self.w, self.h)
        elif level == 1 and state == GameState.BOSS_FIGHT:
            pyxel.bltm(72, 0, level, 96, 0, self.w, self.h)
