import pygame
import os
import sys

#main

BLACK = pygame.Color("#000000")
WHITE = pygame.Color("#ffffff")
RED = pygame.Color("#ff0000")
GREEN = pygame.Color("#00ff00")
BLUE = pygame.Color("#0000ff")
SIZE = WIDTH, HEIGHT = (1000, 700)
FPS = 60
TILE_WIDTH, TILE_HEIGHT = 70, 70
score = 1000


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


class LevelButton:
    def __init__(self, level):
        self.level = level
        self.rect = pygame.Rect(50, 300 + (60 * (level - 1)), 250, 45)

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        font = pygame.font.Font("data/Font.otf", 22)
        text = font.render(f"Уровень {'A' if self.level == 1 else 'B' if self.level == 2 else 'C'}", True, BLACK)
        surface.blit(text, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, scale_x, scale_y):
        super().__init__(all_sprites, enemy_group)
        enemy_filename = name + '.png'
        self.image = pygame.transform.scale(load_image(enemy_filename), (scale_x, scale_y))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.speed = 0.5
        self.direction = 1
        self.bounds = (TILE_WIDTH * pos_x - 100, TILE_WIDTH * pos_x + 100)

    def update(self):
        global score
        self.rect.x += self.speed * self.direction
        if self.rect.left <= self.bounds[0] or self.rect.right >= self.bounds[1]:
            self.direction *= -1
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            score += 500


class TouchableObject(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, scale_x, scale_y):
        super().__init__(all_sprites, platform_group)
        tile_filename = name + '.png'
        self.name = name
        self.image = pygame.transform.scale(load_image(tile_filename), (scale_x, scale_y))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Flag(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, scale_x, scale_y):
        super().__init__(all_sprites, flag_group)
        tile_filename = name + '.png'
        self.name = name
        self.image = pygame.transform.scale(load_image(tile_filename), (scale_x, scale_y))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y - 80)

    def update(self):
        pass
        #if pygame.sprite.spritecollideany(self, player_group):
            #end_screen()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(collectible_group, all_sprites)
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
        global score
        self.cnt += 1
        if self.cnt == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.cnt = 0
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            score += 100


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2) + 140


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.do_jump = False
        self.jump_speed = -20
        self.jump_direction = True
        self.down = 1
        self.collide_flag = True
        self.flag = True

    def update(self, key=None):
        delta_x, delta_y = 0, 5
        if self.do_jump:
            if self.jump_direction:
                self.jump_speed += 1
            else:
                self.jump_speed -= 1
            if self.flag:
                delta_y = self.jump_speed
        if self.jump_speed == 0:
            self.flag = False
            self.jump_direction = not self.jump_direction
        if self.jump_speed < -20:
            self.jump_direction = not self.jump_direction
            self.do_jump = False
            self.jump_speed = -20
            self.flag = True
        if key:
            if key == pygame.K_SPACE and self.collide_flag:
                self.do_jump = True
                self.collide_flag = False
            if key == pygame.K_a:
                delta_x, delta_y = -5, 0
            if key == pygame.K_d:
                delta_x, delta_y = 5, 0

        self.rect = self.rect.move(delta_x, delta_y)
        if pygame.sprite.spritecollideany(self, platform_group):
            self.rect = self.rect.move(-delta_x, -delta_y)
            self.collide_flag = True


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
            elif level[y][x] == '0':
                Enemy('turtle', x, y, 70, 70)
            elif level[y][x] == '1':
                Flag('flag', x, y, 200, 160)
            elif level[y][x] == '*':
                AnimatedSprite(pygame.transform.scale(load_image('animated_coin.png'), (420, 210)),
                               6, 1, x, y)
    new_player = Player(player_x, player_y)
    return new_player, x, y


def start_screen():
    intro_text = ["NotMario", "",
                  "Добро пожаловать", ]
    fon = pygame.transform.scale(load_image('starterscreen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/Font.otf", 30)
    text_coord = 50
    level_buttons = [LevelButton(i) for i in range(1, 4)]
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in level_buttons:
                    if button.is_clicked(event.pos):
                        return button.level
        for button in level_buttons:
            button.draw(screen)
        start_sprites.draw(screen)
        start_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    intro_text = ["Game Over"]
    fon = pygame.transform.scale(load_image('starterscreen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/Font.otf", 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
collectible_group = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
camera = Camera()
player_image = pygame.transform.scale(load_image('player_stand.png'), (50, 70))

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('NotMario')
running = True
clock = pygame.time.Clock()

level_num = start_screen()
if level_num == 1:
    player, level_x, level_y = generate_level(load_level('map1.txt'))
elif level_num == 2:
    player, level_x, level_y = generate_level(load_level('map2.txt'))
elif level_num == 3:
    player, level_x, level_y = generate_level(load_level('map3.txt'))

background = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
while running:
    clock.tick(FPS)
    if pygame.sprite.spritecollideany(player, flag_group):
        break
    score -= 0.01
    score = round(score, 2)
    print(score)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_group.update(pygame.K_a)
    if keys[pygame.K_d]:
        player_group.update(pygame.K_d)
    for event in pygame.event.get():
        running = not event.type == pygame.QUIT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.update(pygame.K_SPACE)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    collectible_group.draw(screen)
    all_sprites.update()
    enemy_group.update()
    player_group.update()
    collectible_group.update()
    camera.update(player)
    camera.apply(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    pygame.display.flip()

end_screen()

pygame.quit()
