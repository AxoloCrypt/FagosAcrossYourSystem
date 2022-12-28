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
        self.y = max(self.y, 8.0)
        self.y = min(self.y, 104.0)

        if self.x < 0:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.sprite_x, self.sprite_y, self.w, self.h)
