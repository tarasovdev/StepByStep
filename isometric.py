from typing import Deque
import pygame, sys, time, random
from pygame.locals import *

start_position = [110,145]

moving_right = False
moving_left = False
moving_up = False
moving_down = False
attack = False
hurt = False
died = False
spawn = True
find_key = False
find_potion = False
trap_find = False
trap_can_hurt = True
potion_can_use =  True

pygame.init()

screen = pygame.display.set_mode((750,750))
display = pygame.Surface((300, 300))

grass_img = pygame.image.load('img/grass.png').convert()
grass_img.set_colorkey((0, 0, 0))

trap_grass_img = pygame.image.load('img/grasstrap.png').convert()
trap_grass_img.set_colorkey((0, 0, 0))
trap_rect = pygame.Rect(0,0,2,2)

stair_img = pygame.image.load('img/stair.png').convert()
stair_img.set_colorkey((0,0,0))
stair_rect =pygame.Rect(0,0,stair_img.get_width() - 18,stair_img.get_height()-22)

shield_img = pygame.image.load('img/shield.png').convert()
shield_img.set_colorkey((0,0,0))

hit_tiles = []
trap_tiles = []

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.idle_anim = [pygame.image.load('img/player/idle/i_1.png').convert(), 
            pygame.image.load('img/player/idle/i_2.png').convert(), 
            pygame.image.load('img/player/idle/i_3.png').convert(), 
            pygame.image.load('img/player/idle/i_4.png').convert()]
        self.attack_anim = [pygame.image.load('img/player/attack/a_1.png').convert(),
            pygame.image.load('img/player/attack/a_2.png').convert(),
            pygame.image.load('img/player/attack/a_3.png').convert(),
            pygame.image.load('img/player/attack/a_4.png').convert(),
            pygame.image.load('img/player/attack/a_5.png').convert(),
            pygame.image.load('img/player/attack/a_6.png').convert(),
            pygame.image.load('img/player/attack/a_7.png').convert(),
            pygame.image.load('img/player/attack/a_8.png').convert(),
            pygame.image.load('img/player/attack/a_9.png').convert(),
            pygame.image.load('img/player/attack/a_10.png').convert(),
            pygame.image.load('img/player/attack/a_11.png').convert(),
            pygame.image.load('img/player/attack/a_12.png').convert(),
            pygame.image.load('img/player/attack/a_13.png').convert(),]
        self.hurt_anim = [pygame.image.load('img/player/hurt/h_1.png').convert(),
            pygame.image.load('img/player/hurt/h_2.png').convert()]
        self.current_sprite = 0
        self.sprite = self.idle_anim[self.current_sprite]
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.right_step = 10
        self.left_step = 5
        self.health = 3

    def update(self, delta):
        global attack, hurt, died
        if attack:
            self.current_sprite += 0.25 * delta

            if self.current_sprite >= len(self.attack_anim):
                attack = False
                self.current_sprite = 0
            
            self.sprite = self.attack_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)
        elif hurt:
            print('hurt')
            self.current_sprite += 0.1 * delta
            hurt = False

            if self.current_sprite > len(self.hurt_anim):
                self.current_sprite = 0

            if self.health > 0:
                self.health -= 1
                print(self.health)
                self.sprite = self.hurt_anim[int(self.current_sprite)]
                self.sprite.set_colorkey((0,0,0))
                display.blit(self.sprite, self.rect)
            else:
                print('died')
                died = True
        else:
            self.current_sprite += 0.15 * delta

            if self.current_sprite >= len(self.idle_anim):
                self.current_sprite = 0

            self.sprite = self.idle_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)

    def move(self, move_sound):
        global moving_right, moving_left, moving_up, moving_down, attack
        if not attack:
            if moving_right:
                self.rect.x += self.right_step
                self.rect.y -= self.left_step
                moving_right = not moving_right
                move_sound.play()
            if moving_left:
                self.rect.x -= self.right_step
                self.rect.y += self.left_step
                moving_left = not moving_left
                move_sound.play()
            if moving_up:
                self.rect.x -= self.right_step 
                self.rect.y -= self.left_step
                moving_up = not moving_up
                move_sound.play()
            if moving_down:
                self.rect.x += self.right_step
                self.rect.y += self.left_step
                moving_down = not moving_down
                move_sound.play()

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.idle_anim = [pygame.image.load('img/boss/idle/i_1.png').convert(), 
            pygame.image.load('img/boss/idle/i_2.png').convert(), 
            pygame.image.load('img/boss/idle/i_3.png').convert(), 
            pygame.image.load('img/boss/idle/i_4.png').convert(),
            pygame.image.load('img/boss/idle/i_5.png').convert(),
            pygame.image.load('img/boss/idle/i_6.png').convert(),
            pygame.image.load('img/boss/idle/i_7.png').convert(),
            pygame.image.load('img/boss/idle/i_8.png').convert()]
        self.attack_anim = [pygame.image.load('img/enemies/rhino/attack/a_1.png').convert(),
            pygame.image.load('img/enemies/rhino/attack/a_2.png').convert(),
            pygame.image.load('img/enemies/rhino/attack/a_3.png').convert(),
            pygame.image.load('img/enemies/rhino/attack/a_4.png').convert()]
        self.current_sprite = 0
        self.sprite = self.idle_anim[self.current_sprite].convert()
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.enemy_attack = False

    def update(self, delta):
        if self.enemy_attack:
            self.current_sprite += 0.10 * delta
            if self.current_sprite >= len(self.attack_anim):
                self.current_sprite = 0
                self.enemy_attack = False

            self.sprite = self.attack_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)
        else:
            self.current_sprite += 0.15 * delta
            if self.current_sprite >= len(self.idle_anim):
                self.current_sprite = 0
                
            self.sprite = self.idle_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)

    def die(self):
        self.kill()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 2, 2)

    def collide_test(self, rect):
        mooseman_rect = self.get_rect()
        return mooseman_rect.colliderect(rect)


class Troll(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.idle_anim = [pygame.image.load('img/enemies/troll/idle/i_1.png').convert(), 
            pygame.image.load('img/enemies/troll/idle/i_2.png').convert(), 
            pygame.image.load('img/enemies/troll/idle/i_3.png').convert(), 
            pygame.image.load('img/enemies/troll/idle/i_4.png').convert()]
        self.attack_anim = [pygame.image.load('img/enemies/troll/attack/a_1.png').convert(),
            pygame.image.load('img/enemies/troll/attack/a_2.png').convert(),
            pygame.image.load('img/enemies/troll/attack/a_3.png').convert(),
            pygame.image.load('img/enemies/troll/attack/a_4.png').convert()]
        self.current_sprite = 0
        self.sprite = self.idle_anim[self.current_sprite].convert()
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.enemy_attack = False

    def update(self, delta):
        if self.enemy_attack:
            self.current_sprite += 0.10 * delta
            if self.current_sprite >= len(self.attack_anim):
                self.current_sprite = 0
                self.enemy_attack = False

            self.sprite = self.attack_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)
        else:
            self.current_sprite += 0.15 * delta
            if self.current_sprite >= len(self.idle_anim):
                self.current_sprite = 0
                
            self.sprite = self.idle_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)

    def die(self):
        self.kill()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 2, 2)

    def collide_test(self, rect):
        mooseman_rect = self.get_rect()
        return mooseman_rect.colliderect(rect)


class MooseMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.idle_anim = [pygame.image.load('img/enemies/mooseman/idle/i_1.png').convert(), 
            pygame.image.load('img/enemies/mooseman/idle/i_2.png').convert(), 
            pygame.image.load('img/enemies/mooseman/idle/i_3.png').convert(), 
            pygame.image.load('img/enemies/mooseman/idle/i_4.png').convert()]
        self.attack_anim = [pygame.image.load('img/enemies/mooseman/attack/a_1.png').convert(),
            pygame.image.load('img/enemies/mooseman/attack/a_2.png').convert(),
            pygame.image.load('img/enemies/mooseman/attack/a_3.png').convert(),
            pygame.image.load('img/enemies/mooseman/attack/a_4.png').convert(),
            pygame.image.load('img/enemies/mooseman/attack/a_5.png').convert(),
            pygame.image.load('img/enemies/mooseman/attack/a_6.png').convert(),]
        self.current_sprite = 0
        self.sprite = self.idle_anim[self.current_sprite]
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.enemy_attack = False

    def update(self, delta):
        if self.enemy_attack:
            self.current_sprite += 0.15 * delta
            if self.current_sprite >= len(self.attack_anim):
                self.current_sprite = 0
                self.enemy_attack = False

            self.sprite = self.attack_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)

        else:
            self.current_sprite += 0.15 * delta
            if self.current_sprite >= len(self.idle_anim):
                self.current_sprite = 0
                
            self.sprite = self.idle_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)

    def die(self):
        self.kill()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 2, 2)

    def collide_test(self, rect):
        mooseman_rect = self.get_rect()
        return mooseman_rect.colliderect(rect)


class Rhino(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.idle_anim = [pygame.image.load('img/enemies/rhino/idle/i_1.png').convert(), 
            pygame.image.load('img/enemies/rhino/idle/i_2.png').convert(), 
            pygame.image.load('img/enemies/rhino/idle/i_3.png').convert(), 
            pygame.image.load('img/enemies/rhino/idle/i_4.png').convert()]
        self.attack_anim = [pygame.image.load('img/enemies/rhino/attack/a_1.png').convert(),
            pygame.image.load('img/enemies/rhino/attack/a_2.png').convert(),
            pygame.image.load('img/enemies/rhino/attack/a_3.png').convert(),
            pygame.image.load('img/enemies/rhino/attack/a_4.png').convert()]
        self.current_sprite = 0
        self.sprite = self.idle_anim[self.current_sprite].convert()
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.enemy_attack = False

    def update(self, delta):
        if self.enemy_attack:
            self.current_sprite += 0.10 * delta
            if self.current_sprite >= len(self.attack_anim):
                self.current_sprite = 0
                self.enemy_attack = False

            self.sprite = self.attack_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)
        else:
            self.current_sprite += 0.15 * delta
            if self.current_sprite >= len(self.idle_anim):
                self.current_sprite = 0
                
            self.sprite = self.idle_anim[int(self.current_sprite)]
            self.sprite.set_colorkey((0,0,0))
            display.blit(self.sprite, self.rect)

    def die(self):
        self.kill()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 2, 2)

    def collide_test(self, rect):
        mooseman_rect = self.get_rect()
        return mooseman_rect.colliderect(rect)


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sprite = pygame.image.load('img/key.png').convert()
        self.sprite.set_colorkey((0,0,0))
        self.rect = pygame.Rect(self.x, self.y, 1,1)
        self.rect.center = (x, y)

    def update(self):
        global find_key
        if find_key != True:
            display.blit(self.sprite, self.rect)


class Potion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sprite = pygame.image.load('img/health_potion.png').convert()
        self.sprite.set_colorkey((0,0,0))
        self.rect = pygame.Rect(self.x, self.y, 1,1)
        self.rect.center = (x, y)

    def update(self):
        global find_potion
        if find_potion != True:
            display.blit(self.sprite, self.rect)


def draw_tiles(map_data):
    for y,row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == 1:
                display.blit(grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5))
            if tile == 2:
                finish_location = [159 + x * 10 - y * 10, 100 + x * 5 + y * 5]
                display.blit(stair_img,(150 + x * 10 - y * 10, 100 + x * 5 + y * 5))
                stair_rect.x = finish_location[0]
                stair_rect.y = finish_location[1]
            if tile == 3:
                hit_tiles.append(pygame.Rect(159 + x * 10 - y * 10, 100 + x * 5 + y * 5, 2,2))
            if tile == 4 and trap_find == False:
                display.blit(grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5))
                trap_rect.x = (150 + x * 10 - y * 10 + 10)
                trap_rect.y = (100 + x * 5 + y * 5)
            if tile == 4 and trap_find == True:
                display.blit(trap_grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5))


def check_hit_tile(player, hit_sound):
    global hurt, died
    for tile in hit_tiles:
        if player.rect.colliderect(tile) and died != True:
            hit_sound.play()
            hurt = True
            player.rect = player.sprite.get_rect()
            player.rect.center = (110, 145)
        elif player.rect.colliderect(tile) and died == True:
            died = False
            player.health += 3
            player.rect = player.sprite.get_rect()
            player.rect.center = (110, 145)

def load_map(level):
    f = open('maps/map'+str(level)+'.txt')
    map_data = [[int(c) for c in row] for row in f.read().split('\n')]
    f.close()
    return map_data


current_enemies_obj = []
enemies_obj_lvl2 = [MooseMan(160,130)]
enemies_obj_lvl3 = [MooseMan(170,155), MooseMan(140,140)]
enemies_obj_lvl4 = [MooseMan(110,155), Troll(150,125),MooseMan(240,170), Troll(150,185)]
enemies_obj_lvl5 = [Boss(180,100)]
last_enemies_obj = []

levels = {
    2:enemies_obj_lvl2,
    3:enemies_obj_lvl3,
    4:enemies_obj_lvl4,
    5:enemies_obj_lvl5
}

keys_levels = {
    1:Key(190,145),
    2:Key(180,140),
    3:Key(210,145),
    4:Key(260,170),
    5:Key(260,170)
}

potion_levels = {
    1:Potion(-10, -10),
    2:Potion(-10, -10),
    3:Potion(-10, -10),
    4:Potion(170, 115),
    5:Potion(-10, -10),
}

def check_trap(player, attack_sound):
    global trap_find, hurt, trap_can_hurt
    if player.rect.colliderect(trap_rect) and trap_can_hurt:
        attack_sound.play()
        trap_find = True
        hurt = True
        trap_can_hurt = False

def spawn_enemies(player,next_level, delta, hit_sound):
    global current_enemies_obj, last_enemies_obj, spawn, hurt
    if spawn:
        print('lalaland')
        for enemy in next_level:
            current_enemies_obj.append(enemy)
            last_enemies_obj.append(enemy)
        spawn = False
    else:
        for enemy in current_enemies_obj:
            enemy.update(delta)
            if enemy.collide_test(player.rect) and enemy.enemy_attack != True:
                hit_sound.play()
                enemy.enemy_attack = True
                hurt = True
            elif enemy.collide_test(player.rect) and attack:
                enemy.die()
                del current_enemies_obj[current_enemies_obj.index(enemy)]


def reload_scene(player):
    global died, current_enemies_obj, last_enemies_obj, spawn, find_key, potion_can_use, find_potion, trap_find, trap_can_hurt
    died = False
    find_key = False
    player.health = 3
    player.rect = player.sprite.get_rect()
    player.rect.center = (110, 145)
    current_enemies_obj = []
    trap_find = False
    trap_can_hurt = True
    find_potion = False
    potion_can_use = True
    spawn = True
    return current_enemies_obj

def draw_ui(base_font, health,current_level):
    armor_text = str(health)
    level_text = 'lvl '+ str(current_level) + '/10'
    armor_surface = base_font.render(armor_text, True, (255,255,255))
    level_surface = base_font.render(level_text, True, (255,255,255))
    display.blit(shield_img, (0,0))
    display.blit(armor_surface,(18,2))
    display.blit(level_surface,(120,2))

def main():
    global moving_left, moving_right, moving_up, moving_down, attack, hit_tiles, potion_can_use, spawn, current_enemies_obj, find_key, trap_find, trap_can_hurt, find_potion

    pygame.mixer.pre_init(44100,-16,2,512)
    pygame.init()
    pygame.display.set_caption('step by step')
    
    base_font = pygame.font.Font('fonts/Font.TTF',10)

    main_clock = pygame.time.Clock()
    framerate = 60
    last_time = time.time()

    move_sound = pygame.mixer.Sound('sounds/step.wav')
    move_sound.set_volume(0.15)
    attack_sound = pygame.mixer.Sound('sounds/attack.wav')
    attack_sound.set_volume(0.15)
    pygame.mixer.music.load('sounds/theme.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    current_level = 4
    next_level = []
    map_data = load_map(current_level)

    background_offset = 0

    player = Player(110, 145)

    while True:
        delta = time.time() - last_time
        delta *= 60
        last_time = time.time()

        display.fill((30,30,30))
        background_offset = (background_offset + 0.5) % 30

        for i in range(16):
            pygame.draw.line(display, (20, 20, 20), (-10, int(i * 30 + background_offset - 10)), (display.get_width() + 25, int(i * 30 - 200 + background_offset)), 5)

        draw_tiles(map_data)
        player.update(delta)
        keys_levels[current_level].update()
        potion_levels[current_level].update()

        if player.rect.colliderect(keys_levels[current_level].rect):
            find_key = True
        if player.rect.colliderect(potion_levels[current_level].rect) and potion_can_use:
            find_potion = True
            potion_can_use = False
            player.health += 1
        if player.rect.colliderect(stair_rect) and find_key == True:
            player.health = 3
            current_level += 1
            hit_tiles = []
            map_data = load_map(current_level)
            current_enemies_obj = []
            next_level = levels.get(current_level, [])
            player.rect = player.sprite.get_rect()
            player.rect.center = (110, 145)
            spawn = True
            find_key = False
            trap_find = False
            find_potion = False
            potion_can_use = True
            trap_can_hurt = True

        spawn_enemies(player, next_level, delta, attack_sound)
        draw_ui(base_font, player.health,current_level)
        check_hit_tile(player, attack_sound)
        check_trap(player, attack_sound)

        if died:
            reload_scene(player)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                    player.move(move_sound)
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                    player.move(move_sound)
                if event.key == K_UP or event.key == K_w:
                    moving_up = True
                    player.move(move_sound)
                if event.key == K_DOWN or event.key == K_s:
                    moving_down = True
                    player.move(move_sound)
                if event.key == K_SPACE:
                    attack_sound.play()
                    attack = True

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        main_clock.tick(framerate)


if __name__ == '__main__':
    main()
