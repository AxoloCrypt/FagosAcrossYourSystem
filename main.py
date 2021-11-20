import collections
import time
from random import random
import pyxel
import enum

# Const values
SCREEN_WIDTH = 192
SCREEN_HEIGHT = 128

FAGO_SPEED = 2.0
BULLET_SPEED = 1.5
ENEMY_SPEED = 1.5
LEVEL_SPEED = 0.1
bullet_list = []
enemy_list = []
blast_list = []


# Enums to enumerate different states in the game
# Directions for player movement
# State of the player during the game
# State of the game while running
class Directions(enum.Enum):
    RIGHT = 0
    LEFT = 1
    DOWN = 2
    UP = 3


class FagoState(enum.Enum):
    MOVING = 0,
    ATTACKING = 1,


class GameState(enum.Enum):
    RUNNING = 0,
    GAMEOVER = 1


# param: list
# draw the elements of the given list
def draw_list(list):
    for elem in list:
        elem.draw()


# param: list
# update the elements of the given list
def update_list(list):
    for elem in list:
        elem.update()


# param: list
# remove the elements of the given list if they are not alive in game
def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


# param: string, int, char_width default pyxel font width
# Helper function for calculating the start x value for right aligned text.
def right_text(text, page_width, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return page_width - (text_width + char_width)


# Player class
class Fago:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.direction = None
        self.state = FagoState.MOVING
        self.speed = FAGO_SPEED

    def draw(self):
        width = self.w
        height = self.h
        sprite_x = 208  # Variable to implement the sprite asset location x
        sprite_y = 0  # Variable to implement the sprite asset location y
        # The sprite_x and sprite_y values will change depending the direction of the player

        if self.state == FagoState.MOVING:
            if self.direction == Directions.DOWN:
                sprite_x = 208
                sprite_y = 0
                height = height * -1
            if self.direction == Directions.UP:
                sprite_x = 208
                sprite_y = 0
            if self.direction == Directions.RIGHT:
                sprite_x = 184
                sprite_y = 0
                width = width * - 1
            if self.direction == Directions.LEFT:
                sprite_x = 184
                sprite_y = 0
        elif self.state == FagoState.ATTACKING:
            sprite_x = 136
            sprite_y = 0
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

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        # Change player state
        if pyxel.btnp(pyxel.KEY_X):
            if self.state == FagoState.MOVING:
                self.state = FagoState.ATTACKING
                self.speed -= 1
            else:
                self.state = FagoState.MOVING
                self.speed += 1
        if self.state == FagoState.ATTACKING:
            if pyxel.btnp(pyxel.KEY_SPACE):
                Bullet(
                    self.x + (self.w + 8) / 2, self.y + 8 / 2
                )  # Instantiate a Bullet class object

    def get_pos(self):
        return self.x, self.y


class Bullet:
    def __init__(self, x, y, is_enemy=False):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.alive = True
        self.is_enemy = is_enemy
        bullet_list.append(self)

    def update(self):
        self.x += BULLET_SPEED

        if self.is_enemy:
            self.x -= BULLET_SPEED

        if self.x + self.w + 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 64, 8, self.w, self.h)

        if self.is_enemy:
            pyxel.blt(self.x, self.y, 0, 40, 0, self.w, self.h)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        # self.dir = Directions.LEFT
        self.alive = True
        self.offset = int(random() * 60)
        self.sprite_x = 0
        self.sprite_y = 0

        enemy_list.append(self)

    # Move the enemy up and down while moving to -x coordinates
    # set if it is alive or not
    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.y -= ENEMY_SPEED
            self.sprite_x = 64
            self.sprite_y = 24
        else:
            self.y += ENEMY_SPEED
            self.sprite_x = 104
            self.sprite_y = 0

        self.x -= ENEMY_SPEED

        if self.x < 0:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.sprite_x, self.sprite_y, self.w, self.h)


class Blast:
    def __init__(self, x, y):
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
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)


class Level:
    def __init__(self):
        self.x = 0
        self.tm = 0
        self.u = 0
        self.v = 0
        self.w = 72
        self.h = 16

    def update(self):
        self.x -= LEVEL_SPEED
        # startPos_x = 0
        repeat_width = self.w / 2
        if 0 - self.x > repeat_width:
            self.x = 0

    def draw(self):
        pyxel.bltm(self.x, 0, self.tm, self.u, self.v, self.w, self.h)


class Hud:
    def __init__(self):
        self.score_text = ""
        self.score_text_x = 0

    def draw_score(self, score):
        self.score_text = str(score)
        self.score_text_x = right_text(self.score_text, 192)
        pyxel.text(self.score_text_x - 10, 1, self.score_text, 8)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Fagos", fps=60, fullscreen=False)
        pyxel.load("assets/pyxres.resources.pyxres")
        self.level = Level()
        self.hud = Hud()
        self.fago = Fago(32, 32)
        self.fago_direction = Directions.DOWN
        self.flying_enemies_on_screen = 0
        self.time_last_frame = time.time()
        self.dt = 0
        self.time_since_last_move = 0
        self.input_queue = collections.deque()  # Store direction changes
        self.score = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_play_scene()

    def update_play_scene(self):
        self.level.update()
        # Spawn 10 enemies on screen
        if pyxel.frame_count % 6 == 0:
            if len(enemy_list) < 15:
                Enemy(pyxel.width, random() * (pyxel.height - 10))

        # print(len(enemy_list))
        # Check if elements of bullet_list and enemy_list intersect each other
        # If the intersection is true, set the current enemy and bullet alive variable to False
        for a in enemy_list:
            for b in bullet_list:
                if (
                        a.x + a.w > b.x
                        and b.x + b.w > a.x
                        and a.y + a.h > b.y
                        and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + 16 / 2, a.y + 16 / 2)
                    )
                    self.score += 10

        # Check if the current enemy intersects with the player
        # If it is true, set the current enemy alive variable to False
        for enemy in enemy_list:
            if (
                    self.fago.x + self.fago.w > enemy.x
                    and enemy.x + enemy.w > self.fago.x
                    and self.fago.y + self.fago.h > enemy.y
                    and enemy.y + enemy.h > self.fago.y
            ):
                enemy.alive = False

                blast_list.append(
                    Blast(
                        self.fago.x + self.fago.w / 2,
                        self.fago.y + self.fago.h / 2
                    )
                )

        # Update player, bullet_list and enemy_list
        self.fago.update()
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)

        # Clean up lists
        cleanup_list(bullet_list)
        cleanup_list(enemy_list)
        cleanup_list(blast_list)

    def draw(self):
        pyxel.cls(0)
        self.level.draw()
        self.hud.draw_score(self.score)
        self.fago.draw()
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)


App()
