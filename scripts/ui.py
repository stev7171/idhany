import pygame

class UI:
    def __init__(self, game):
        pygame.font.init()
        self.game = game
        self.comic_sans = pygame.font.SysFont("arial", 15)

    def draw_text(self, text, pos, win):
        text_render = self.comic_sans.render(text, False, (255, 255, 255))
        win.blit(text_render, pos)
    
    def draw_background(self, pos, win, scale):
        pygame.draw.rect(win, (180, 180, 180), (pos, scale))

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, win):
        action = False

        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check mouse over && click
        if self.rect.collidepoint(pos[0] // 2, pos[1] // 2):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False

        win.blit(self.image, (self.rect.x, self.rect.y))

        return action