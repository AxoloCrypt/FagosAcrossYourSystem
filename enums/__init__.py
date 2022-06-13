import enum


# Enums to enumerate different states in the game
# Directions for player movement
# State of the player during the game
# State of the game while running
class Directions(enum.Enum):
    RIGHT = 0
    LEFT = 1
    DOWN = 2
    UP = 3


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


globals().update(Directions.__members__)
globals().update(GameState.__members__)
