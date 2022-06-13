import pyxel
from hud.hud import Hud


# param: string, int, char_width default pyxel font width
# Helper function for calculating the start x value for right aligned text.
def right_text(text, page_width, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return page_width - (text_width + char_width)


# Hud class handles drawing text and scores
def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
    text_witdh = len(text) * char_width
    return (page_width - text_witdh) / 2
