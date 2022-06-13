import pyxel
from entities.bullet import Bullet
from enums import *

FAGO_SPEED = 1.0


# Player class
class Fago:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.direction = None
        self.speed = FAGO_SPEED

    def draw(self, current_level, game_state):
        width = self.w
        height = self.h
        sprite_x = 0  # Variable to implement the sprite asset location x
        sprite_y = 0  # Variable to implement the sprite asset location y
        # The sprite_x and sprite_y values will change depending the direction of the player

        # Select the sprite_x and sprite_x depending of the direction, current level and game state
        # If else yanderev style
        # My future me it's gonna hate this but it works
        if current_level == 0 and (game_state == GameState.RUNNING or game_state == GameState.PAUSED):
            sprite_x = 136
            sprite_y = 0
        elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
            sprite_x = 0
            sprite_y = 64
        if current_level == 1 and (game_state == GameState.RUNNING or game_state == GameState.PAUSED):
            sprite_x = 48
            sprite_y = 40
        elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
            sprite_x = 120
            sprite_y = 64
        if current_level == 2 and (game_state == GameState.RUNNING or game_state == GameState.PAUSED):
            sprite_x = 64
            sprite_y = 112
        elif current_level == 2 and game_state == GameState.BOSS_FIGHT:
            sprite_x = 80
            sprite_y = 112

        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, width, height)  # Draw player

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
            self.direction = Directions.UP
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
            self.direction = Directions.DOWN
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.direction = Directions.LEFT
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.direction = Directions.RIGHT

        # Define max and min values for coordinates x,y
        # Check if the character it's out of bounces
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 8.0)
        self.y = min(self.y, 104.0)

        # Change player state
        if pyxel.btnp(pyxel.KEY_SPACE, hold=0, repeat=10):
            pyxel.play(3, 4)
            Bullet(
                self.x + (self.w + 8) / 2, self.y + 8 / 2
            )  # Instantiate a Bullet class object

    def get_pos(self):
        return self.x, self.y
