import pygame as pg
from random import uniform
import math
import random
from settings import *
from tilemap import collide_hit_rect
import os

vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if dir == 'x':
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.player_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.rot = 0
        self.last_shot = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        # if keys[pg.K_SPACE]:
        #     now = pg.time.get_ticks()
        #     if now - self.last_shot > BULLET_RATE:
        #         self.last_shot = now
        #         dir = vec(1, 0).rotate(-self.rot)
        #         pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
        #         self.vel = vec(-KICKBACK, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    ACTIONS = ['up', 'down', 'left', 'right', 'still']

    def __init__(self, game, x, y, fitness = -100, chromesone = []):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.chromosome = [random.choice(Mob.ACTIONS) for _ in range(500)]
        self.chromosome_index = 0
        self.fitness = 0
        # self.rot = 0
        # self.up_count = 0
        # self.down_count = 0
        # self.left_count = 0
        # self.right_count = 0
        # self.still_count = 0

    def update(self):

        # if self.chromosome_index > len(self.chromosome):
        #     child = Mob(self.game, self.rect.centerx, self.rect.centery, )
        #     return child
            # self.pos = vec(x, y) * TILESIZE
        #     rand_choice = random.choice(self.chromosone)
        # else:
        #     rand_choice = random.choice(self.chromosome)
        # print()
        rand_choice = self.chromosome[self.chromosome_index]
        # print(rand_choice)
        # print(self.chromosome)
        # print(self.chromosome_index)
        # print()
        # self.chromosome[self.chromosome_index] = rand_choice
        # print(len(self.chromosome))
        self.chromosome_index += 1

        if rand_choice == "up":
            self.vel += (0, .1)  # increasing vel is just to get collision to work
            self.pos += (0, 1)
            # self.up_count+=1
        if rand_choice == "down":
            self.vel += (0, -.1)
            self.pos += (0, -1)
            # self.down_count+=1
        if rand_choice == "left":
            self.vel += (-.1, 0)
            self.pos += (-1, 0)
            # self.left_count+=1
        if rand_choice == "right":
            self.vel += (.1, 0)
            self.pos += (1, 0)
            # self.right_count+=1
        if rand_choice == "still":
            # self.vel = (0, 0)
            # self.still_count+=1
            pass
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.vel.x = 0
        self.vel.y = 0

    def crossover(self, other):
        child = Mob(self.game, self.rect.centerx, self.rect.centery, 0)  # initialize with no genes
        crossover_point = random.randint(0, min(len(self.chromosome), len(other.chromosome)) - 1)
        child.chromosome = self.chromosome[:crossover_point] + other.chromosome[crossover_point:]
        return child

    def mutate(self, chromosome, mutation_rate=0.01):
        """Mutate a chromosome with given mutation rate.

        Args:
            chromosome (list): The chromosome to mutate.
            mutation_rate (float): The probability of each gene to mutate.
        """
        # List of possible directions and states
        directions = ['up', 'down', 'left', 'right', 'still']

        for i in range(len(chromosome)):
            if random.random() < mutation_rate:
                # Select a new random direction/state, different from the current one
                new_direction = random.choice([d for d in directions if d != chromosome[i]])
                # Mutate the gene
                chromosome[i] = new_direction

        return chromosome


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.wall_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Objective(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.wall_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
