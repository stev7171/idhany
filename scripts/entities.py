import pygame, random

class Entity:
    def __init__(self, type_, tile_manager, game, pos, size=[16, 16], offset=[0, 0]):
        self.pos = pos
        self.game = game
        self.offset = offset
        self.size = size
        self.t_man = tile_manager
        self.type = type_

        self.img = self.game.assets[self.type]
        self.img.set_colorkey((0, 0, 0))

        self.velocity = [0, 0]
        self.collided_down = False
        self.collided_left = False
        self.collided_right = False

        self.can_jump = False

    def collision_test(self, tiles):
        collision = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                collision.append(tile.rect)
        return collision

    def update(self, tiles, movement=[0, 0]):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.rect.x += self.frame_movement[0]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if self.frame_movement[0] > 0:
                self.rect.right = tile.left
            if self.frame_movement[0] < 0:
                self.rect.left = tile.right
        self.pos[0] = self.rect.x
        
        self.rect.y += self.frame_movement[1]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if self.frame_movement[1] > 0:
                self.rect.bottom = tile.top
                self.velocity[1] = 0
                self.can_jump = True
            if self.frame_movement[1] < 0:
                self.rect.top = tile.bottom
                self.velocity[1] = 0
        self.pos[1] = self.rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collided_down == True:
            self.velocity[1] = 0
    
    def draw(self, win, offset=[0, 0]):
        win.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Slime(Entity):
    def __init__(self, tile_manager, game, pos, level=1, size=[16, 16], offset=[0, 0]):
        super().__init__('slime', tile_manager, game, pos, size, offset)
        self.level = level
    
    def update(self, tiles, movement=[0, 0], player_pos=[0, 0]):
        super().update(tiles, movement)
        
        player = player_pos

        text = "lvl " + str(self.level)
        self.game.ui.draw_text(text, (self.pos[0], self.pos[1] - 20), self.game.disp)

        if player[0] > self.pos[0]:
            self.pos[0] += 1
        if player[0] < self.pos[0]:
            self.pos[0] -= 1
    
    def draw(self, win, offset=[0, 0]):
        super().draw(win, offset)

class Player(Entity):
    def __init__(self,  tile_manager, game, pos, size=[16, 16], offset=[0, 0]):
        super().__init__('player', tile_manager, game, pos, size, offset)

    def update(self, tiles, enemies, movement=[0, 0]):
        super().update(tiles, movement)

        if self.game.moving_right == True and self.collided_right == False:
            self.pos[0] += 2
        if self.game.moving_left == True and self.collided_left == False:
            self.pos[0] -= 2
        if self.game.jumping == True and self.can_jump == True:
            self.collided_down = False
            self.velocity[1] = -3
            self.can_jump = False

        count = 0
        for i in enemies:
            if self.rect.colliderect(i.rect):
                if self.rect.y >= i.rect.y:
                    self.game.game_state = self.game.die_state
##                if self.rect.y < i.rect.y and i.level < 3:
##                    self.rect.bottom = i.rect.top
##                    self.game.kill_enemy(count)
##                    self.game.coins += 5
            
            if i.rect.colliderect(self.game.tool.rect):
                enemies.pop(count)
                self.game.coins += 5 + (i.level * self.game.tool.level)
            count += 1

class Shopkeeper(Entity):
    def __init__(self, type_, tile_manager, game, pos, size=[16, 16], offset=[0, 0]):
        super().__init__(type_, tile_manager, game, pos, size, offset)
    
    def update(self, tiles, movement=[0, 0]):
        super().update(tiles, movement)