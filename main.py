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
TILE_WIDTH, TILE_HEIGHT = 70, 70


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class TouchableObject(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, scale_x, scale_y):
        super().__init__(all_sprites)
        tile_filename = name + '.png'
        self.image = pygame.transform.scale(load_image(tile_filename), (scale_x, scale_y))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(TILE_WIDTH * x, TILE_HEIGHT * y)
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
        if self.cnt == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.cnt = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.x, self.y = pos_x, pos_y

    def move(self, key):
        delta_x, delta_y = None, None
        if key == pygame.K_RIGHT:
            delta_x, delta_y = 10, 0
        if key == pygame.K_LEFT:
            delta_x, delta_y = -10, 0
        self.rect = self.rect.move(self.x + delta_x, self.y + delta_y)
        #if pygame.sprite.spritecollideany(player, all_sprites):
           # self.rect = self.rect.move(-delta_x, -delta_y)


def generate_level(level):
    new_player, x, y = None, None, None
    player_x, player_y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                continue
            elif level[y][x] == '#':
                TouchableObject('brick', x, y, 70, 70)
            elif level[y][x] == '-':
                TouchableObject('floating_land', x, y, 120, 60)
            elif level[y][x] == '&':
                TouchableObject('cloud', x, y, 200, 70)
            elif level[y][x] == '@':
                player_x, player_y = x, y
            elif level[y][x] == '*':
                AnimatedSprite(pygame.transform.scale(load_image('animated_coin.png'), (420, 210)),
                               6, 1, x, y)
    new_player = Player(player_x, player_y)
    return new_player, x, y


def start_screen():
    intro_text = ["NotMario", "",
                  "Начать игру",]
    fon = pygame.transform.scale(load_image('starterscreen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/Font.otf", 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
#player_image = load_image('tempplayer.png')
player_image = pygame.transform.scale(load_image('player_stand.png'), (50, 70))

#cloud = TouchableObject('cloud', 0, 0, 200, 70)
#brick = TouchableObject('brick', 300, 0, 70, 70)
#powerup = TouchableObject('powerup_brick', 300, 70, 70, 70)
#float_land = TouchableObject('floating_land', 0, 300, 120, 60)
#wall = TouchableObject('wall', 300, 140, 70, 70)
#heart = TouchableObject('heart', 0, 500, 50, 50)
#coin = AnimatedSprite(pygame.transform.scale(load_image('animated_coin.png'), (420, 210)), 6, 1, 50, 50)

player, level_x, level_y = generate_level(load_level('map.txt'))

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('NotMario')
running = True
clock = pygame.time.Clock()

start_screen()
background = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_group.update(pygame.K_LEFT)
    if keys[pygame.K_RIGHT]:
        player_group.update(pygame.K_RIGHT)
    for event in pygame.event.get():
        running = not event.type == pygame.QUIT
    screen.blit(background, (0, 0))
    #screen.fill(WHITE)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()