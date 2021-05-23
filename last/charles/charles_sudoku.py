from random import shuffle, choice, sample, random
from operator import  attrgetter
import numpy as np
from copy import deepcopy
import csv
import time
from charles.generation import generate_random_solution, remove_blank_spaces
from data.sudoku_data import quizz


class Individual:
    def __init__(
        self,
        representation=None,
        #size=None,
        valid_set=[i for i in range(10)],
    ):
        self.representation = generate_random_solution(quizz)
        self.fitness = self.evaluate()

    def evaluate(self):
        raise Exception("You need to monkey patch the fitness function.")

    def get_neighbours(self, func, **kwargs):
         raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    #def __repr__(self):
    #    return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"
    def __repr__(self):
        return f"Individual: {self.representation}; Fitness: {self.fitness}"

class Population:
    def __init__(self, size, optim):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.gen = 1
        self.timestamp = int(time.time())
        for _ in range(size):
            self.individuals.append(
                Individual()
            )

        

    def evolve(self, gens, select, crossover, mutation, mutation_type, co_p, mu_p,  quizz, elitism):
        for gen in range(gens):
            new_pop = []
 
            if elitism == True:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))
 
            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1.representation, parent2.representation)
                else:
                    offspring1, offspring2 = parent1.representation, parent2.representation
                # Mutation
                if random() < mu_p:
                    offspring1 = mutation(quizz, offspring1, mutation_type)
                if random() < mu_p:
                    offspring2 = mutation(quizz, offspring2, mutation_type)
 
                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))
 
            if elitism == True:
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    least = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(least))
                new_pop.append(elite)

            self.log()
            self.individuals = new_pop
            self.gen += 1
 
            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
            elif self.optim == "min":
                print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')

    def log(self):
        with open(f'run_{self.timestamp}.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for i in self:
                writer.writerow([self.gen, i.representation, i.fitness])


    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
        
        
