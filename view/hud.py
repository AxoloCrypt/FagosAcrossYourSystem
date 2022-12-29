import pyxel
from enums.enums import GameState


# param: string, int, char_width default pyxel font width
# Helper function for calculating the start x value for right aligned text.
def right_text(text, page_width, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return page_width - (text_width + char_width)


# Hud class handles drawing text and scores
def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return (page_width - text_width) / 2


class Hud:
    def __init__(self, screen_height, screen_width):
        self.score_text = ""
        self.score_text_x = 0
        self.score_text_y = 0
        self.lives_text = ""
        self.lives_text_x = 20
        self.paused = "PAUSED"
        self.paused_x = 10
        self.enter = "PRESS ENTER TO CONTINUE"
        self.enter_x = center_text(self.enter, screen_width)
        self.enter_y = center_text(self.enter, screen_height)

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
