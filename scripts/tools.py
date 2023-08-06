import pygame

class Tool:
    def __init__(self, game, img, level=1):
        self.game = game
        self.img = self.game.assets[img]
        self.img.set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(self.game.player.pos[0] + 15, self.game.player.pos[1] - 5, self.img.get_width(), self.img.get_height())
        self.level = level

    def draw(self, win, direction):
        if direction < 0:
            self.rect.x = self.game.player.pos[0] - 15
            self.flipped_img = pygame.transform.flip(self.img, True, False)
        elif direction >= 0:
            self.rect.x = self.game.player.pos[0] + 15
            self.flipped_img = self.img

        self.rect.y = self.game.player.pos[1] - 5
        win.blit(self.flipped_img, (self.rect.x, self.rect.y))

    def level_up(self, img):
        self.img = self.game.assets[img]
        self.level += 1

class Sword(Tool):
    def __init__(self, game, img):
        super().__init__(game, img)

    def draw(self, win):
        super().draw(win)