import pygame
import sys
import scripts.entities as entities
import scripts.tile as tile
import scripts.ui as ui
import scripts.tools as tools
import random
import os
import importlib
from _thread import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.width = 800
        self.height = 600

        self.win = pygame.display.set_mode((self.width, self.height))
        self.disp = pygame.Surface((self.width // 2, self.height // 2))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('8523-24a')

        self.assets = {
            'player': pygame.image.load('res/images/entities/player-tmp.png').convert(),
            'grass': pygame.image.load('res/images/tiles/grass1.png').convert(),
            'stone': pygame.image.load('res/images/tiles/stone.png').convert(),
            'slime': pygame.image.load('res/images/entities/slime.png').convert(),
            'key': pygame.image.load('res/images/ui/key2.png').convert(),
            'debug': pygame.image.load('res/images/shop/DEBUG.png').convert(),
            'player2': pygame.image.load('res/images/entities/player-tmp-pink.png').convert(),
            'play': pygame.image.load('res/images/ui/play.png').convert(),
            'exit': pygame.image.load('res/images/ui/exit.png').convert(),
            'return': pygame.image.load('res/images/ui/return.png').convert(),
            'sword': pygame.image.load('res/images/tools/sword.png').convert(),
            'axe': pygame.image.load('res/images/tools/axe.png').convert()
        }

        self.tile_manager = tile.TileManager(self)
        self.player = entities.Player(self.tile_manager, self, [15, 15])
        #self.enemy = entities.Slime(self.tile_manager, self, [400, 15])

        self.enemies = [entities.Slime(self.tile_manager, self, [400, 15]),
                        entities.Slime(self.tile_manager, self, [200, 15]),
                        entities.Slime(self.tile_manager, self, [500, 15]),]

        self.game_state = 0
        self.play_state = 1
        self.die_state = 2
        self.shop_state = 3
        self.title_state = 4
        self.paused_state = 5

        self.game_state = self.title_state

        self.moving_right = False
        self.moving_left = False
        self.jumping = False

        self.ui = ui.UI(self)

        self.coins = 0

        self.debug_button = ui.Button(20, 20, pygame.image.load('res/images/shop/DEBUG.png'), 2)
        self.frame_count = 0

        self.key_img = self.assets['key']
        self.key_img.set_colorkey((0, 0, 0))

        self.tool_img = 'sword'

        self.tool = tools.Tool(self, self.tool_img)
        self.tool_dir = 0

        self.current_slime_level = 1

        self.assets['axe'].set_colorkey((0, 0, 0))
        self.assets['sword'].set_colorkey((0, 0, 0))
        self.upgrade_axe = ui.Button(40, 60, self.assets['axe'], 2)
        self.upgrade_sword = ui.Button(36, 100, self.assets['sword'], 2)

        self.tool_level_sword = 1
        self.tool_level_axe = 1

        self.tool_price = 5

        self.respawn_button = ui.Button(self.disp.get_width() // 2 - 16 * 2, 200, self.assets['play'], 2)

        self.music_count = 0
        self.music = [pygame.mixer.Sound('res/audio/detective.wav'),
                      pygame.mixer.Sound('res/audio/obfuscation.wav'),
                      pygame.mixer.Sound('res/audio/test.wav')]
        self.random_time = random.randint(60 * 60, (60 * 60) + 20)

        self.offset = [0, 0]

        self.mods = os.listdir('res/mods')

    def kill_enemy(self, index):
        if index <= len(self.enemies) - 1:
            self.enemies.pop(index)

    def play_music(self):
        music = self.music[1]
        music.play(-1)

    def run(self):

        while True:

            for mod in self.mods:
                if '.py' in mod:
                    m = importlib.import_module('res.mods.' + mod.replace('.py', ''))
                    m.update(self)

            self.disp.fill((0, 0, 0))

            if self.game_state != self.title_state:
                self.tile_manager.draw(self.disp, self.offset)

                for enemy in self.enemies:
                    enemy.draw(self.disp)

                self.player.draw(self.disp, self.offset)
            
            if self.game_state == self.title_state:
                self.ui.draw_text("IDHANY", (150, 100), self.disp)
                play_button = ui.Button(150, 130, self.assets['play'], 2)
                exit_button = ui.Button(180, 130, self.assets['exit'], 2)

                if play_button.draw(self.disp) == True:
                    self.game_state = self.play_state
                    self.play_music()
                if exit_button.draw(self.disp) == True:
                    pygame.quit()
                    sys.exit()
            
            if self.game_state == self.paused_state:
                self.disp.fill((0, 0, 0))

                self.ui.draw_text("PAUSED", (150, 100), self.disp)
                play_button = ui.Button(150, 130, self.assets['return'], 2)
                exit_button = ui.Button(180, 130, self.assets['exit'], 2)

                if play_button.draw(self.disp) == True:
                    self.game_state = self.play_state
                if exit_button.draw(self.disp) == True:
                    pygame.quit()
                    sys.exit()

            if self.game_state == self.play_state:
                self.frame_count += 1
                self.music_count += 1

                if self.frame_count == 600:
                    self.current_slime_level += 1
                    self.enemies.append(entities.Slime(self.tile_manager, self, [200, 15], self.current_slime_level))
                    self.enemies.append(entities.Slime(self.tile_manager, self, [300, 15], self.current_slime_level))
                    self.frame_count = 0

                for i in self.enemies:
                    i.update(self.tile_manager.tiles, player_pos=self.player.pos)

                if self.moving_left == True:
                    self.tool_dir = -1
                elif self.moving_right == True:
                    self.tool_dir = 1

                self.player.update(self.tile_manager.tiles, self.enemies)
                self.tool.draw(self.disp, self.tool_dir)
            elif self.game_state == self.die_state:
                textFont = pygame.font.SysFont("arial", 50)
                text_rendered = textFont.render("YOU DIED!", 1, (255, 0, 0))
                self.disp.blit(text_rendered, (80, 100))

                if self.respawn_button.draw(self.disp) == True:
                    self.game_state = self.play_state
                    
                    self.enemies = [entities.Slime(self.tile_manager, self, [400, 15]),
                                    entities.Slime(self.tile_manager, self, [200, 15]),
                                    entities.Slime(self.tile_manager, self, [500, 15]),]
                    
                    self.current_slime_level = 1

                    self.tool_level_sword = 1
                    self.tool_level_axe = 1

                    self.tool_price = 5

                    self.coins = 0

                    self.player.pos = [15, 15]

                    self.frame_count = 0
            elif self.game_state == self.shop_state:
                self.ui.draw_background((10, 10), self.disp, (380, 240))
                self.ui.draw_text("Upgrade price: " + str(self.tool_price), (100, 20), self.disp)

                if self.upgrade_axe.draw(self.disp) == True and self.coins >= self.tool_price:
                    self.tool_level_axe += 1
                    self.coins -= self.tool_price
                    self.tool_price += 3
                if self.upgrade_sword.draw(self.disp) == True and self.coins >= self.tool_price:
                    self.tool_level_sword += 1
                    self.coins -= self.tool_price
                    self.tool_price += 3

            if self.game_state == self.play_state or self.game_state == self.shop_state:
                self.disp.blit(self.key_img, (5, 5))
                self.ui.draw_text(': ' + str(self.coins), (20, 5), self.disp)

                self.disp.blit(self.assets['sword'], (5, 20))
                self.assets['sword'].set_colorkey((0, 0, 0))
                self.ui.draw_text(': ' + str(self.tool_level_sword), (20, 20), self.disp)

                self.disp.blit(self.assets['axe'], (5, 40))
                self.assets['axe'].set_colorkey((0, 0, 0))
                self.ui.draw_text(': ' + str(self.tool_level_axe), (20, 40), self.disp)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.moving_right = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.moving_left = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP: self.jumping = True
                    if event.key == pygame.K_RETURN:
                        if self.game_state == self.play_state:
                            self.game_state = self.shop_state
                        elif self.game_state == self.shop_state:
                            self.game_state = self.play_state
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == self.play_state:
                            self.game_state = self.paused_state
                        elif self.game_state == self.paused_state:
                            self.game_state = self.play_state
                    if event.key == pygame.K_1: self.tool.img = self.tool = tools.Tool(self, 'sword', self.tool_level_sword)
                    if event.key == pygame.K_2: self.tool.img = self.tool = tools.Tool(self, 'axe', self.tool_level_axe)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.moving_right = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.moving_left = False
                    if event.key == pygame.K_w or event.key == pygame.K_UP: self.jumping = False

            self.win.blit(pygame.transform.scale(self.disp, (self.width, self.height)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    app = Game()
    app.run()