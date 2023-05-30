# import pygame as pg
# from settings import *
# from sprites import *
from tilemap import collide_hit_rect
# vec = pg.math.Vector2
import random

class Population:
    def __init__(self, size, crossover_rate, mutation_rate, fitness_func, mob_generator):
        self.size = size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.fitness_func = fitness_func
        self.mob_generator = mob_generator


        # Initialize population with random individuals
        self.individuals = [self.mob_generator(0, 0, chromosome_length=100) for _ in range(self.size)]

    def evaluate_fitness(self):
        for individual in self.individuals:
            individual.fitness = self.fitness_func(individual)

    def evolve(self):
        self.evaluate_fitness()

        new_individuals = []

        for _ in range(self.size):
            parent1 = self.select_parent()
            parent2 = self.select_parent()

            child = parent1.crossover(parent2)

            child.mutate(self.mutation_rate)
            # new_individuals.append(0)
            # new_individuals.append(0)
            new_individuals.append(child)

        self.individuals = new_individuals

    def select_parent(self):
        # Tournament selection
        contenders = random.sample(self.individuals, k=5)  # Select 5 random individuals
        return max(contenders, key=lambda individual: individual.fitness)
