import time
from random import random
import pyxel
import enum

# Const values
SCREEN_WIDTH = 192
SCREEN_HEIGHT = 128

FAGO_SPEED = 2.0
BULLET_SPEED = 2.5
BOSS_BULLET_SPEED = 2.0
ENEMY_SPEED = 1.5
BOSS_SPEED = 2.0
LEVEL_SPEED = 0.1
bullet_list = []
boss_bullet_list = []
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


# State of the player during the game
class FagoState(enum.Enum):
    MOVING = 0,
    ATTACKING = 1,


# Different game states during the game
class GameState(enum.Enum):
    RUNNING = 0,
    GAMEOVER = 1,
    TITTLE = 2,
    BOSS_FIGHT = 3,
    COMPLETED = 4,
    TRANSITION = 5,
    PAUSED = 6,
    LEVEL_COMPLETE = 7


# param: list
# draw the elements of the given list
def draw_list(list):
    for elem in list:
        elem.draw()


# param: list, int, enum
# draw the elements of the bullet_list
def draw_bullet_list(list, current_level, game_state):
    for elem in list:
        elem.draw(current_level, game_state)


# param: list
# update the elements of the given list
def update_list(list):
    for elem in list:
        elem.update()


# param: list
# update the elements of the enemy_list depending on the level
def update_enemy_list(list, current_level):
    for elem in list:
        elem.update(current_level)


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


# Hud class handles drawing text and scores
def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
    text_witdh = len(text) * char_width
    return (page_width - text_witdh) / 2


# param: int
# Select the sound of the boss depending on the current level
def select_boss_sound(current_level):
    switch = {
        0: 8,
        1: 2,
        2: 1
    }

    return switch.get(current_level, 0)


def select_scene_music(game_state):
    switch = {
        GameState.TITTLE: 1,
        GameState.RUNNING: 2,
        GameState.BOSS_FIGHT: 3
    }
    return switch.get(game_state, 0)


def select_level_music(level):
    switch = {
        0: 2,
        1: 2,
        2: 4
    }

    return switch.get(level, 0)


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

    def draw(self, current_level, game_state):
        width = self.w
        height = self.h
        sprite_x = 208  # Variable to implement the sprite asset location x
        sprite_y = 0  # Variable to implement the sprite asset location y
        # The sprite_x and sprite_y values will change depending the direction of the player

        # Select the sprite_x and sprite_x depending of the direction, current level and game state
        # If else yanderev style
        # My future me it's gonna hate this but it works
        if self.state == FagoState.MOVING:
            if self.direction == Directions.DOWN:
                if current_level == 0 and game_state == GameState.RUNNING:
                    sprite_x = 208
                    sprite_y = 0
                elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 48
                    sprite_y = 64
                if current_level == 1 and game_state == GameState.RUNNING:
                    sprite_x = 96
                    sprite_y = 40
                elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 128
                    sprite_y = 40
                if current_level == 2 and game_state == GameState.RUNNING:
                    sprite_x = 64
                    sprite_y = 128
                elif current_level == 2 and GameState.BOSS_FIGHT:
                    sprite_x = 80
                    sprite_y = 128
                height = height * -1
            if self.direction == Directions.UP:
                if current_level == 0 and GameState.RUNNING == game_state:
                    sprite_x = 208
                    sprite_y = 0
                elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 48
                    sprite_y = 64
                if not (not (current_level == 1) or not (game_state == GameState.RUNNING)):  # De Morgan's law
                    sprite_x = 96
                    sprite_y = 40
                elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 128
                    sprite_y = 40
                if current_level == 2 and game_state == GameState.RUNNING:
                    sprite_x = 64
                    sprite_y = 128
                elif current_level == 2 and GameState.BOSS_FIGHT:
                    sprite_x = 80
                    sprite_y = 128
            if self.direction == Directions.RIGHT:
                if current_level == 0 and game_state == GameState.RUNNING:
                    sprite_x = 184
                    sprite_y = 0
                elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 24
                    sprite_y = 64
                if current_level == 1 and game_state == GameState.RUNNING:
                    sprite_x = 72
                    sprite_y = 40
                elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 112
                    sprite_y = 40
                if current_level == 2 and game_state == GameState.RUNNING:
                    sprite_x = 96
                    sprite_y = 128
                elif current_level == 2 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 112
                    sprite_y = 128
                width = width * - 1
            if self.direction == Directions.LEFT:
                if current_level == 0 and GameState.RUNNING == game_state:
                    sprite_x = 184
                    sprite_y = 0
                elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 24
                    sprite_y = 64
                if not (not (current_level == 1) or not (game_state == GameState.RUNNING)):  # De Morgan's law
                    sprite_x = 72
                    sprite_y = 40
                elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 112
                    sprite_y = 40
                if current_level == 2 and game_state == GameState.RUNNING:
                    sprite_x = 96
                    sprite_y = 128
                elif current_level == 2 and game_state == GameState.BOSS_FIGHT:
                    sprite_x = 112
                    sprite_y = 128
        elif self.state == FagoState.ATTACKING:
            if current_level == 0 and game_state == GameState.RUNNING:
                sprite_x = 136
                sprite_y = 0
            elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
                sprite_x = 0
                sprite_y = 64
            if current_level == 1 and game_state == GameState.RUNNING:
                sprite_x = 48
                sprite_y = 40
            elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
                sprite_x = 120
                sprite_y = 64
            if current_level == 2 and game_state == GameState.RUNNING:
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
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        # Check if the character it's out of bounces
        # if True keep the character in the selected position
        if self.y < 8.0:
            self.y = 8.0
        elif self.y > 104.0:
            self.y = 104.0

        # Change player state
        if pyxel.btnp(pyxel.KEY_X):
            if self.state == FagoState.MOVING:
                pyxel.play(3, 3)
                self.state = FagoState.ATTACKING
                self.speed -= 1
            else:
                pyxel.play(3, 3)
                self.state = FagoState.MOVING
                self.speed += 1
        if self.state == FagoState.ATTACKING:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(3, 4)
                Bullet(
                    self.x + (self.w + 8) / 2, self.y + 8 / 2
                )  # Instantiate a Bullet class object

    def get_pos(self):
        return self.x, self.y


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

        if self.is_boss or self.is_bacteria:
            boss_bullet_list.append(self)
        else:
            bullet_list.append(self)

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
            self.x -= BOSS_BULLET_SPEED
            if self.x + self.w + 1 < 0:
                self.alive = False
        elif self.is_boss and self.is_vertical:
            self.y += 1.0
            if self.y > 104.0:
                self.alive = False
        else:
            self.x += BULLET_SPEED
            if self.x + self.w + 1 > SCREEN_WIDTH:
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
    def update(self, current_level):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.y -= ENEMY_SPEED

            if current_level == 0:
                self.sprite_x = 64
                self.sprite_y = 24
            elif current_level == 1:
                self.sprite_x = 0
                self.sprite_y = 40
            elif current_level == 2:
                self.sprite_x = 96
                self.sprite_y = 112

        else:
            self.y += ENEMY_SPEED

            if current_level == 0:
                self.sprite_x = 104
                self.sprite_y = 0
            elif current_level == 1:
                self.sprite_x = 24
                self.sprite_y = 40
            elif current_level == 2:
                self.sprite_x = 120
                self.sprite_y = 112

        self.x -= ENEMY_SPEED

        # Check if the character it's out of bounces
        # if True keep the character in the selected position
        if self.y < 8.0:
            self.y = 8.0
        elif self.y > 104.0:
            self.y = 104.0

        if self.x < 0:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.sprite_x, self.sprite_y, self.w, self.h)


# End level Boss class
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 200
        self.alive = True
        self.w = 24
        self.h = 32
        self.offset = int(random() * 100)

    def update(self, current_level):
        # Boss movement
        if (pyxel.frame_count + self.offset) % 96 < 60:
            self.y -= BOSS_SPEED
        else:
            self.y += BOSS_SPEED

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
                        SCREEN_WIDTH / 2, 9.0, is_boss=True, is_vertical=True
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
    # draw the boss sprite depending of the current level
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

    def update(self):
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
        pyxel.circ(self.x, self.y, self.radius, 8)
        pyxel.circb(self.x, self.y, self.radius, 2)


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


class Level:
    def __init__(self):
        self.x = 0
        self.tm = 0
        self.u = 0
        self.v = 0
        self.w = 64
        self.h = 16

    def update(self, state):
        # Move the level tilemap and repeat it constantly while the game is in GameState.Running
        if state != GameState.BOSS_FIGHT and state == GameState.RUNNING:
            self.x -= LEVEL_SPEED
            repeat_width = self.w / 2
            if 0 - self.x > repeat_width:
                self.x = 0

    def draw(self, level, state):

        if state == GameState.RUNNING:
            pyxel.bltm(self.x, 0, level, self.u, self.v, self.w, self.h)
        elif state == GameState.TITTLE:
            pyxel.bltm(0, 0, 3, self.u, self.v, 64, 16)
        elif level == 0 and state == GameState.LEVEL_COMPLETE:
            pyxel.bltm(0, 0, 4, self.u, self.v, 64, 16)
        elif level == 1 and state == GameState.LEVEL_COMPLETE:
            pyxel.bltm(0, 0, 5, self.u, self.v, 64, 16)
        elif state == GameState.GAMEOVER:
            pyxel.bltm(0, 0, 6, self.u, self.v, 64, 16)
        elif state == GameState.COMPLETED:
            pyxel.bltm(0, 0, 7, self.u, self.v, 64, 16)

        if state == GameState.BOSS_FIGHT:
            pyxel.bltm(0, 0, level, 72, 0, self.w, self.h)
        elif level == 1 and state == GameState.BOSS_FIGHT:
            pyxel.bltm(0, 0, level, 96, 0, self.w, self.h)


class Hud:
    def __init__(self):
        self.score_text = ""
        self.score_text_x = 0
        self.score_text_y = 0
        self.lives_text = ""
        self.lives_text_x = 20
        self.paused = "PAUSED"
        self.paused_x = 10
        self.enter = "PRESS ENTER TO CONTINUE"
        self.enter_x = center_text(self.enter, SCREEN_WIDTH)
        self.enter_y = center_text(self.enter, SCREEN_HEIGHT)

    def draw_score(self, score, level):
        self.score_text = str(score)
        self.score_text_x = right_text(self.score_text, 192)
        pyxel.text(self.score_text_x - 10, 1, self.score_text, 8)

        if level == 1:
            pyxel.text(self.score_text_x - 10, 1, self.score_text, 5)

    def draw_final_score(self, score):
        self.score_text = str(score)
        self.score_text_x = center_text(self.score_text, 192)
        self.score_text_y = center_text(self.score_text, 126)

        pyxel.text(self.score_text_x + 20, self.score_text_y + 19, self.score_text, pyxel.frame_count % 16)

    # Draw the number of lives in the upper right corner
    def draw_lives(self, lives, current_level, game_state):
        self.lives_text = str(lives)
        pyxel.text(self.lives_text_x, 1, self.lives_text, 8)
        # Another if else yanderev style to draw the mini fago on the upper left
        if current_level == 0 and game_state == GameState.RUNNING:
            pyxel.blt(self.lives_text_x - 10, 1, 0, 8, 16, 8, 8)
        elif current_level == 0 and game_state == GameState.BOSS_FIGHT:
            pyxel.blt(self.lives_text_x - 10, 1, 0, 200, 48, 8, 8)
        if current_level == 1 and game_state == GameState.RUNNING:
            pyxel.blt(self.lives_text_x - 10, 1, 0, 184, 48, 8, 8)
        elif current_level == 1 and game_state == GameState.BOSS_FIGHT:
            pyxel.text(self.lives_text_x, 1, self.lives_text, 5)
            pyxel.blt(self.lives_text_x - 10, 1, 0, 192, 48, 8, 8)
        if current_level == 2 and game_state == GameState.RUNNING:
            pyxel.blt(self.lives_text_x - 10, 1, 0, 48, 128, 8, 8)
        elif current_level == 2 and game_state == GameState.BOSS_FIGHT:
            pyxel.blt(self.lives_text_x - 10, 1, 0, 56, 128, 8, 8)

    def draw_pause(self):
        pyxel.rect(self.paused_x - 1, 0, len(self.paused) * pyxel.FONT_WIDTH + 1, pyxel.FONT_HEIGHT + 1, 1)
        pyxel.text(self.paused_x, 1, self.paused, 3)
        pyxel.text(self.enter_x, self.enter_y, self.enter, pyxel.frame_count % 16)
        pyxel.text(self.enter_x + 15, self.enter_y + 20, "PRESS Q TO QUIT", pyxel.frame_count % 16)


class App:
    def __init__(self):
        # Init screen
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Fagos Across Your System", fps=60, fullscreen=False)
        # File where the resources are loaded
        pyxel.load("assets/pyxres.resources.pyxres")
        # Initialize variables
        self.level = Level()
        self.hud = Hud()
        self.transition_blast = TransitionBlast(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.fago = Fago(32, 32)
        self.bosses = []
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bacterias = []
        self.bacterias.append(Bacteria((SCREEN_WIDTH / 2) + 24, 8.0))
        self.bacterias.append(Bacteria((SCREEN_WIDTH / 2) + 24, 104, Directions.DOWN))
        self.fago_direction = Directions.DOWN
        self.lives = 10
        self.enemies_killed = 0
        self.score = 0
        self.previous_score = 0
        self.game_state = GameState.TITTLE
        self.previous_game_state = None
        self.current_level = 0
        self.music = 0

        self.music = select_scene_music(self.game_state)
        pyxel.playm(self.music, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):

        self.music = select_scene_music(self.game_state)

        if self.game_state == GameState.RUNNING or self.game_state == GameState.BOSS_FIGHT:
            self.update_play_scene()

        if self.game_state == GameState.TRANSITION:
            self.update_transition_scene()

        if self.game_state == GameState.PAUSED:
            self.update_paused_scene()

        if self.game_state == GameState.GAMEOVER:
            self.update_gameover_scene()

        if self.game_state == GameState.LEVEL_COMPLETE:
            self.update_level_completed_scene()

        if self.game_state == GameState.TITTLE:
            self.update_tittle_scene()

        if self.game_state == GameState.COMPLETED:
            self.update_game_complete_scene()

    def update_play_scene(self):
        self.level.update(self.game_state)
        if pyxel.btnp(pyxel.KEY_TAB):
            pyxel.play(3, 9)
            self.previous_game_state = self.game_state
            self.game_state = GameState.PAUSED

        if self.lives <= 0:
            pyxel.playm(0, loop=False)
            self.game_state = GameState.GAMEOVER

        if self.current_level == 0 and self.score >= 300 and self.game_state == GameState.RUNNING:
            pyxel.stop()
            pyxel.play(3, 6)
            self.game_state = GameState.TRANSITION
        if self.current_level == 1 and self.score >= 2500 and self.game_state == GameState.RUNNING:
            pyxel.stop()
            pyxel.play(3, 6)
            self.game_state = GameState.TRANSITION
        if self.current_level == 2 and self.score >= 4500 and self.game_state == GameState.RUNNING:
            pyxel.stop()
            pyxel.play(3, 6)
            self.game_state = GameState.TRANSITION

        # if self.game_state == GameState.TRANSITION:
        # self.update_transition_scene()

        if self.game_state == GameState.RUNNING:
            # Spawn 10 enemies on screen
            if pyxel.frame_count % 6 == 0:
                if len(enemy_list) < 10:
                    Enemy(pyxel.width, random() * (pyxel.height - 10))

            if self.enemies_killed == 20:
                self.enemies_killed = 0
                pyxel.play(2, 11)
                self.lives += 1

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
                        pyxel.play(2, 5)
                        self.score += 10
                        self.enemies_killed += 1

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
                    pyxel.play(2, 14)
                    self.lives -= 1
                    blast_list.append(
                        Blast(
                            self.fago.x + self.fago.w / 2,
                            self.fago.y + self.fago.h / 2
                        )
                    )

            # Update player, bullet_list and enemy_list
            self.fago.update()
            update_list(bullet_list)
            update_enemy_list(enemy_list, self.current_level)
            update_list(blast_list)

            # Clean up lists
            cleanup_list(bullet_list)
            cleanup_list(enemy_list)
            cleanup_list(blast_list)

        # Updating when the boss fight begins
        if self.game_state == GameState.BOSS_FIGHT:
            self.fago.update()
            self.bosses[self.current_level].update(self.current_level)

            # Check collisions between player bullets and boss bullets
            for a in bullet_list:
                for b in boss_bullet_list:
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
                        pyxel.play(2, 7)

            # Check collisions between player bullets and the current boss
            for b in bullet_list:
                if (
                        b.x + b.w > self.bosses[self.current_level].x
                        and self.bosses[self.current_level].x + self.bosses[self.current_level].w > b.x
                        and b.y + b.h > self.bosses[self.current_level].y
                        and self.bosses[self.current_level].y + self.bosses[self.current_level].h > b.y
                ):
                    b.alive = False
                    blast_list.append(
                        Blast(b.x + 16 / 2, b.y + 16 / 2)
                    )
                    sound = select_boss_sound(self.current_level)
                    pyxel.play(2, sound)
                    self.bosses[self.current_level].health -= 10

            # Check collisions between the player and boss bullets
            for bb in boss_bullet_list:
                if (
                        self.fago.x + self.fago.w > bb.x
                        and bb.x + bb.w > self.fago.x
                        and self.fago.y + self.fago.h > bb.y
                        and bb.y + bb.h > self.fago.y
                ):
                    bb.alive = False
                    pyxel.play(2, 14)
                    self.lives -= 1
                    blast_list.append(
                        Blast(bb.x + 16 / 2, bb.y + 16 / 2)
                    )

            # Check collision between player and the boss
            if (
                    self.bosses[self.current_level].x + self.bosses[self.current_level].w > self.fago.x
                    and self.fago.x + self.fago.w > self.bosses[self.current_level].x
                    and self.bosses[self.current_level].y + self.bosses[self.current_level].h > self.fago.y
                    and self.fago.y + self.fago.h > self.bosses[self.current_level].y
            ):
                pyxel.play(2, 14)
                self.lives -= 1

            if not self.bosses[self.current_level].alive:
                pyxel.stop()
                pyxel.play(3, 27)
                self.game_state = GameState.LEVEL_COMPLETE
                self.score += 500
            # Update lists
            update_list(bullet_list)
            update_list(boss_bullet_list)
            update_list(blast_list)

            # Update support bacterias from the final boss
            if self.current_level == 2:
                # Check collisions between player bullets and bacteria enemies
                for b in bullet_list:
                    for ba in self.bacterias:
                        # print(f'bullet x: {b.x}, bullet w: {b.w}, b.x + b.w = {b.x + b.w} > {ba.w} ?')
                        if (
                                b.x + b.w > ba.x
                                and ba.x + ba.w < b.x
                                and b.y + b.h > b.y
                                and ba.y + ba.h > b.y
                        ):
                            b.alive = False
                            blast_list.append(
                                Blast(b.x + 16 / 2, b.y + 16 / 2)
                            )
                            ba.health -= 10
                            pyxel.play(2, 10)

                # Check collisions between the player and the bacterias
                for ba in self.bacterias:
                    if (
                            ba.x + ba.w < self.fago.x
                            and self.fago.x + self.fago.w > ba.x
                            and ba.y + ba.h > self.fago.y
                            and self.fago.y + self.fago.h > ba.y
                    ):
                        pyxel.play(2, 14)
                        self.lives -= 1

                if not self.bosses[2].alive:
                    pyxel.stop()
                    self.score += 1000
                    self.game_state = GameState.COMPLETED
                    pyxel.play(3, 30, loop=False)

                update_list(self.bacterias)
                cleanup_list(self.bacterias)

            # Cleanup lists
            cleanup_list(self.bosses)
            cleanup_list(bullet_list)
            cleanup_list(boss_bullet_list)
            cleanup_list(blast_list)

    def update_transition_scene(self):
        bullet_list.clear()
        blast_list.clear()
        enemy_list.clear()
        aux = self.transition_blast.update_blast()  # assistant variable

        #
        if aux == 0:  # When aux is 0, change the game state
            self.game_state = GameState.BOSS_FIGHT
            if self.current_level == 0 or self.current_level == 1:
                pyxel.playm(3, loop=True)
            if self.current_level == 2:
                pyxel.playm(5, loop=True)

    def update_paused_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.play(3, 9)
            self.game_state = self.previous_game_state
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.play(3, 9)
            pyxel.quit()

    def update_tittle_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.stop()
            pyxel.play(3, 9)
            self.game_state = GameState.RUNNING
            pyxel.playm(2, loop=True)

    def update_gameover_scene(self):
        boss_bullet_list.clear()
        bullet_list.clear()
        blast_list.clear()

        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.stop()
            pyxel.play(3, 9)
            if self.current_level == 2:
                self.restart_final_level()
                pyxel.playm(4, loop=True)
            else:
                self.start_new_game()
                pyxel.playm(2, loop=True)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def update_level_completed_scene(self):
        boss_bullet_list.clear()
        bullet_list.clear()
        blast_list.clear()

        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.stop()
            pyxel.play(3, 9)
            self.start_new_level()
            level_music = select_level_music(self.current_level)
            pyxel.playm(level_music, loop=True)

    def update_game_complete_scene(self):
        boss_bullet_list.clear()
        bullet_list.clear()
        blast_list.clear()
        self.bosses.clear()
        self.bacterias.clear()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.play(3, 9)
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.play(3, 9)
            self.start_new_game()

    # Reset the stats after the player it's killed
    def start_new_game(self):
        bullet_list.clear()
        enemy_list.clear()
        blast_list.clear()
        self.fago = Fago(32, 32)
        self.fago_direction = Directions.DOWN
        self.bosses = []
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.lives = 10
        self.enemies_killed = 0
        self.score = 0
        self.game_state = GameState.RUNNING
        self.previous_game_state = None
        self.current_level = 0

    # Method to start a new level once the previous level is completed
    # It keeps the previous stats
    def start_new_level(self):
        bullet_list.clear()
        enemy_list.clear()
        blast_list.clear()

        self.bosses = []
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.lives = self.lives
        self.enemies_killed = self.enemies_killed
        self.score = self.score
        self.previous_score = self.score
        self.game_state = GameState.RUNNING
        self.previous_game_state = None
        self.current_level += 1
        self.fago = Fago(32, 32)
        self.fago_direction = Directions.DOWN

    def restart_final_level(self):
        bullet_list.clear()
        boss_bullet_list.clear()
        enemy_list.clear()
        blast_list.clear()

        self.bosses = []
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bacterias = []
        self.bacterias.append(Bacteria((SCREEN_WIDTH / 2) + 24, 8.0))
        self.bacterias.append(Bacteria((SCREEN_WIDTH / 2) + 24, 104, Directions.DOWN))
        self.lives = 10
        self.enemies_killed = 0
        self.score = self.previous_score
        self.game_state = GameState.RUNNING
        self.previous_game_state = None
        self.current_level = 2
        self.fago = Fago(32, 32)
        self.fago_direction = Directions.DOWN

    def draw(self):
        pyxel.cls(0)
        if self.game_state == GameState.TITTLE:
            self.level.draw(0, self.game_state)
        if self.game_state == GameState.RUNNING:
            self.level.draw(self.current_level, self.game_state)

            self.hud.draw_score(self.score, self.current_level)
            self.hud.draw_lives(self.lives, self.current_level, self.game_state)

            self.fago.draw(self.current_level, self.game_state)

            # Draw lists
            draw_bullet_list(bullet_list, self.current_level, self.game_state)
            draw_list(enemy_list)
            draw_list(blast_list)

        if self.game_state == GameState.TRANSITION:
            self.transition_blast.draw()

        if self.game_state == GameState.PAUSED:
            if self.previous_game_state == GameState.RUNNING:
                self.level.draw(self.current_level, self.previous_game_state)

                self.hud.draw_score(self.score, self.current_level)
                self.hud.draw_pause()

                self.fago.draw(self.current_level, self.game_state)
                draw_bullet_list(bullet_list, self.current_level, self.previous_game_state)
                draw_list(enemy_list)
                draw_list(blast_list)
            elif self.previous_game_state == GameState.BOSS_FIGHT:
                self.level.draw(self.current_level, self.previous_game_state)

                self.hud.draw_score(self.score, self.current_level)
                self.hud.draw_pause()
                self.fago.draw(self.current_level, self.game_state)

                self.bosses[self.current_level].draw(self.current_level)  # Draw current boss
                draw_bullet_list(bullet_list, self.current_level, self.game_state)
                draw_bullet_list(boss_bullet_list, self.current_level, self.game_state)

        if self.game_state == GameState.LEVEL_COMPLETE:
            self.level.draw(self.current_level, self.game_state)

        if self.game_state == GameState.GAMEOVER:
            self.level.draw(self.current_level, self.game_state)

        if self.game_state == GameState.COMPLETED:
            self.level.draw(self.current_level, self.game_state)
            self.hud.draw_final_score(self.score)

        if self.game_state == GameState.BOSS_FIGHT:
            self.level.draw(self.current_level, self.game_state)

            self.hud.draw_score(self.score, self.current_level)
            self.hud.draw_lives(self.lives, self.current_level, self.game_state)

            self.fago.draw(self.current_level, self.game_state)

            self.bosses[self.current_level].draw(self.current_level)  # Draw current boss
            draw_bullet_list(bullet_list, self.current_level, self.game_state)
            draw_bullet_list(boss_bullet_list, self.current_level, self.game_state)
            draw_list(blast_list)

            # Draw boss support bacterias
            if self.current_level == 2:
                draw_list(self.bacterias)


App()  # Kickstart program
