from random import random
from entities import *
from entities.bullet import bullet_list, boss_bullet_list
from entities.enemy import enemy_list
from enums import *
from effects import *
from hud import *

# Const values
SCREEN_WIDTH = 192
SCREEN_HEIGHT = 128
blast_list = []


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


class App:
    def __init__(self):
        # Init screen
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Fagos Across Your System", fps=60)
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
        if pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.play(3, 9)
            self.game_state = self.previous_game_state
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.play(3, 9)
            pyxel.quit()

    def update_tittle_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.stop()
            pyxel.play(3, 9)
            self.game_state = GameState.RUNNING
            pyxel.playm(2, loop=True)

    def update_gameover_scene(self):
        boss_bullet_list.clear()
        bullet_list.clear()
        blast_list.clear()

        if pyxel.btnp(pyxel.KEY_RETURN):
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

        if pyxel.btnp(pyxel.KEY_RETURN):
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
        if pyxel.btnp(pyxel.KEY_RETURN):
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
        self.bacterias = []
        self.bacterias.append(Bacteria((SCREEN_WIDTH / 2) + 24, 8.0))
        self.bacterias.append(Bacteria((SCREEN_WIDTH / 2) + 24, 104, Directions.DOWN))
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

                self.fago.draw(self.current_level, self.game_state)
                draw_bullet_list(bullet_list, self.current_level, self.previous_game_state)
                draw_list(enemy_list)
                draw_list(blast_list)

                self.hud.draw_score(self.score, self.current_level)
                self.hud.draw_pause()

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
