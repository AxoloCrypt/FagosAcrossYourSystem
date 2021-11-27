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
    def __init__(self, x, y, is_enemy=False, is_boss=False, is_vertical=False):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.alive = True
        self.is_enemy = is_enemy
        self.is_boss = is_boss
        self.is_vertical = is_vertical

        if self.is_boss:
            boss_bullet_list.append(self)
        else:
            bullet_list.append(self)

    def update(self):
        if self.is_enemy:
            self.x -= BULLET_SPEED
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
            if self.x + self.w + 1 < 0:
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
        if self.is_enemy:
            pyxel.blt(self.x, self.y, 0, 40, 0, self.w, self.h)
        if self.is_boss:
            pyxel.blt(self.x, self.y, 0, 40, 0, self.w, self.h)
            if current_level == 1:
                pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h)


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

        if current_level == 0:
            # Shoot two bullets when the player shoots
            if pyxel.btnp(pyxel.KEY_SPACE):
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

        if self.health == 0:
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
        if state != GameState.BOSS_FIGHT:
            self.x -= LEVEL_SPEED
            repeat_width = self.w / 2
            if 0 - self.x > repeat_width:
                self.x = 0

    def draw(self, level, state):

        if state == GameState.RUNNING:
            pyxel.bltm(self.x, 0, level, self.u, self.v, self.w, self.h)
        elif state == GameState.TITTLE:
            pyxel.bltm(0, 0, 3, self.u, self.v, 16, 16)

        if state == GameState.BOSS_FIGHT:
            pyxel.bltm(0, 0, level, 72, 0, self.w, self.h)
        elif level == 1 and state == GameState.BOSS_FIGHT:
            pyxel.bltm(0, 0, level, 96, 0, self.w, self.h)


class Hud:
    def __init__(self):
        self.score_text = ""
        self.score_text_x = 0
        self.lives_text = ""
        self.lives_text_x = 20

    def draw_score(self, score, level):
        self.score_text = str(score)
        self.score_text_x = right_text(self.score_text, 192)
        pyxel.text(self.score_text_x - 10, 1, self.score_text, 8)

        if level == 1:
            pyxel.text(self.score_text_x - 10, 1, self.score_text, 5)

    # Draw the number of lives in the upper right corner
    def draw_lives(self, lives, current_level, game_state):
        self.lives_text = str(lives)
        pyxel.text(self.lives_text_x, 1, self.lives_text, 8)
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


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Fagos Across Your System", fps=60, fullscreen=False)
        pyxel.load("assets/pyxres.resources.pyxres")
        self.level = Level()
        self.hud = Hud()
        self.transition_blast = TransitionBlast(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.fago = Fago(32, 32)
        self.bosses = []
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.bosses.append(Boss(SCREEN_WIDTH - 24, SCREEN_HEIGHT / 2 - 16))
        self.fago_direction = Directions.DOWN
        self.lives = 10
        self.enemies_killed = 0
        self.score = 0
        self.game_state = GameState.TITTLE
        self.previous_game_state = None
        self.current_level = 0
        pyxel.run(self.update, self.draw)

    def update(self):
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

    def update_play_scene(self):
        self.level.update(self.game_state)
        if pyxel.btnp(pyxel.KEY_TAB):
            self.previous_game_state = self.game_state
            self.game_state = GameState.PAUSED

        if self.lives <= 0:
            self.game_state = GameState.GAMEOVER

        if self.current_level == 0 and self.score >= 300 and self.game_state == GameState.RUNNING:
            pyxel.play(3, 6)
            self.game_state = GameState.TRANSITION
        if self.current_level == 1 and self.score >= 2500 and self.game_state == GameState.RUNNING:
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
                self.lives -= 1

            if not self.bosses[self.current_level].alive:
                self.game_state = GameState.LEVEL_COMPLETE
                self.score += 500

            # Update lists
            update_list(bullet_list)
            update_list(boss_bullet_list)
            update_list(blast_list)

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

    def update_paused_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.game_state = self.previous_game_state

    def update_tittle_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.game_state = GameState.RUNNING

    def update_gameover_scene(self):
        boss_bullet_list.clear()
        bullet_list.clear()
        blast_list.clear()

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.start_new_game()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def update_level_completed_scene(self):
        boss_bullet_list.clear()
        bullet_list.clear()
        blast_list.clear()

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.start_new_level()

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
        self.game_state = GameState.RUNNING
        self.previous_game_state = None
        self.current_level += 1
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

        if self.game_state == GameState.BOSS_FIGHT:
            self.level.draw(self.current_level, self.game_state)

            self.hud.draw_score(self.score, self.current_level)
            self.hud.draw_lives(self.lives, self.current_level, self.game_state)

            self.fago.draw(self.current_level, self.game_state)

            self.bosses[self.current_level].draw(self.current_level)  # Draw current boss
            draw_bullet_list(bullet_list, self.current_level, self.game_state)
            draw_bullet_list(boss_bullet_list, self.current_level, self.game_state)
            draw_list(blast_list)


App()  # Kickstart program
