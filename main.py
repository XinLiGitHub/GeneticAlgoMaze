
import pygame as pg
import sys
from os import path
from settings import *
import math
from sprites import *
from tilemap import *
from population import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        # img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map5.txt'))

    def new(self):
        # initialize all variables and do all the setup for a new game

        # global temp_col, temp_row
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.objective = pg.sprite.Group()
        # for i in range(50):
        # self.population = Population(
        #     size=1,
        #     crossover_rate=0.8,
        #     mutation_rate=0.02,
        #     fitness_func=self.calculate_fitness,
        #     mob_generator=self.generate_mob
        # )
        # for i in self.population.individuals:
        #     # print(i)
        #     print(len(i.chromosome))
        #     print(i.chromosome_index)
        #     if len(i.chromosome) == i.chromosome_index:
        #
        #         self.population.evolve()
        #         print("evolving..")

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == "O":
                    self.objective = Objective(self, col, row)
                if tile == "M":
                    START_X = col
                    START_Y = row
                    print(START_X, START_Y)
                # if tile == 'P':
                #     self.player = Player(self, col, row)
        list_of_mobs = []
        for i in range(100):
            Mob(self, START_X, START_Y)
            list_of_mobs.append(Mob(self, START_X, START_Y))

    # def generate_mob(self, col, row, chromosome_length):
    #     mob = Mob(self, col, row, chromosome_length=chromosome_length)
    #     return mob

    def calculate_fitness(self, mob):
        # Calculate the Euclidean distance between the mob and the objective
        distance = ((mob.pos.x - self.objective.pos.x) ** 2 + (mob.pos.y - self.objective.pos.y) ** 2) ** 0.5
        if distance == 0:  # Prevent division by zero
            return float('inf')
        else:
            return 1 / distance - len(mob.chromosome) * 0.001

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # avg = 0
        # avg_list = []
        # fitness_dict = {}
        top_list = [] # lower the better
        for mob in self.mobs:
            mob.fitness = self.calculate_fitness(mob)
            if len(top_list) < 50:
                top_list.append(mob) # gonna do mob
            else:

                worst_top = min(top_list, key=lambda x: x.fitness)
                if mob.fitness > worst_top.fitness:
                    top_list.remove(worst_top)
                    top_list.append(mob)

        for mob in self.mobs:
            if mob.chromosome_index >= 499:
                # Select a random individual from top_10
                temp = random.choice(top_list)
                # Ensure deep copy of the chromosome
                mob.chromosome = temp.chromosome.copy()
                # Shuffle and mutate the new chromosome
                random.shuffle(mob.chromosome)
                mob.mutate(mob.chromosome)
                mob.chromosome_index = 0

                # mob.x = START_X
                # mob.y = START_Y
                mob.pos = vec(120, 1) * TILESIZE
                mob.vel = vec(0, 0)
                # print(mob.pos)
            # break



        # print(avg/len(self.mobs))
        # print(avg)
        # print(len(self.mobs))
        # print("")
        # self.calculate_fitness(self.mobs)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        # for sprite in self.all_sprites:
        #     self.screen.blit(sprite.image)
        self.all_sprites.draw(self.screen)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        # catch all events here

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()