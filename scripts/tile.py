import pygame

class Tile:
    def __init__(self, type_, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.type = type_
        self.tile_size = 16

        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 16, 16)

    def draw(self, win, offset=[0, 0]):
        win.blit(self.game.assets[self.type], (self.x * self.tile_size - offset[0], self.y * self.tile_size - offset[1]))

class TileManager:
    def __init__(self, game):
        self.tiles = []
        self.game = game
        for y in range(3):
            for x in range((self.game.width // 2)):
                if y == 0:
                    self.tiles.append(Tile('grass', self.game, x, y + 16))
                else:
                    self.tiles.append(Tile('stone', self.game, x, y + 16))
    
    def draw(self, win, offset=[0, 0]):
        for i in self.tiles:
            i.draw(win, offset)