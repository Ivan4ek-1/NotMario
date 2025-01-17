import pygame
import os
import sys

BLACK = pygame.Color("#000000")
WHITE = pygame.Color("#ffffff")
RED = pygame.Color("#ff0000")
GREEN = pygame.Color("#00ff00")
BLUE = pygame.Color("#0000ff")
SIZE = WIDTH, HEIGHT = (1000, 700)
FPS = 60

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class TouchableObject(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, scale_x, scale_y):
        super().__init__(all_sprites)
        tile_filename = name + '.png'
        self.image = pygame.transform.scale(load_image(tile_filename), (scale_x, scale_y))
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.cnt = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cnt += 1
        if self.cnt == 4:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.cnt = 0


all_sprites = pygame.sprite.Group()
cloud = TouchableObject('cloud', 0, 0, 200, 70)
brick = TouchableObject('brick', 300, 0, 70, 70)
powerup = TouchableObject('powerup_brick', 300, 70, 70, 70)
float_land = TouchableObject('floating_land', 0, 300, 120, 60)
wall = TouchableObject('wall', 300, 140, 70, 70)
#coin = TouchableObject('animated_coin', 0, 400, 420, 210)
heart = TouchableObject('heart', 0, 500, 50, 50)

coin = AnimatedSprite(load_image('animated_coin.png'), 6, 1, 50, 50)

pygame.init()
screen = pygame.display.set_mode(SIZE)
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        running = not event.type == pygame.QUIT
    pygame.display.flip()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    all_sprites.update()

pygame.quit()