from random import shuffle, choice, sample, random
from operator import  attrgetter
import numpy as np
from copy import deepcopy
import csv
import time

from numpy.core.fromnumeric import sort
from charles.generation import generate_random_solution, sudoku_representation
from data.sudoku_data import quizz, count
#import sys

from timeit import default_timer as timer
from datetime import timedelta

start = timer()
end = []


class Individual:
    def __init__(
        self,
        representation=None,
        #size=None,
        valid_set=[i for i in range(10)],
    ):
        if representation == None:
            self.representation = generate_random_solution(quizz)
        else:
            self.representation = representation

        self.fitness = self.evaluate()
        #self.representation = None
        

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

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, total_gens, select_type, crossover_type, mutation_type):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.gen = 1
        self.givens = count
        self.total_gens = total_gens
        self.select_type = select_type
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.timestamp = int(time.time())

        for _ in range(size):
            self.individuals.append(
                Individual(representation = generate_random_solution(quizz))
            )

        
    def evolve(self, gens, select, crossover, mutations, mutation_type, co_p, mu_p,  quizz, elitism):

        for gen in range(gens):
            
            best_fitness = min(self, key=attrgetter("fitness"))
            
            # Create new individuals for diversificate population
            #if gen >= 1:
            #    new_random_pop = []
            #    old_population = []
            #    for i in range(int((self.size)/2)):
            #        new = Individual(representation = generate_random_solution(quizz))
            #        new_random_pop.append(new)
            #        old_population.append(self.individuals[i])
                
            #    self.individuals = new_random_pop + old_population


            # If not find solution
            if best_fitness.fitness != 0:
                
                new_pop = []
 
                if elitism == True:
                    if self.optim == "max":
                        elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                    elif self.optim == "min":
                        elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))
                
                while len(new_pop) < self.size:
                    parent1 = select(self)
                    #self.individuals = sorted(self,reverse=False, key=attrgetter('fitness'))
                    parent2 = select(self)
                    #while parent1==parent2:
                    #    parent2 = select(self)
                    # Crossover
                    if random() < co_p:
                        offspring1, offspring2 = crossover(parent1.representation, parent2.representation)
                    else:
                        offspring1, offspring2 = parent1.representation, parent2.representation
                    # Mutation
                    if random() < mu_p:
                        offspring1 = mutations(quizz, offspring1, mutation_type, 2)

                    if random() < mu_p:
                        offspring2 = mutations(quizz, offspring2, mutation_type, 2)

                    new_pop.append(Individual(representation=offspring1))
                    if len(new_pop) < self.size:
                        new_pop.append(Individual(representation=offspring2))

                if elitism == True:
                    if self.optim == "max":
                        least = min(new_pop, key=attrgetter("fitness"))
                    elif self.optim == "min":
                        least = max(new_pop, key=attrgetter("fitness"))
                    new_pop.pop(new_pop.index(least))
                
                    best = deepcopy(min(new_pop, key=attrgetter("fitness")))
                    if elite.fitness == best.fitness:
                        elite.fitness += 1
                    else:
                        pass
                    new_pop.append(elite)

                #self.log()
                self.individuals = new_pop
                # sort before add new population
                #self.individuals = sorted(new_pop,reverse=False, key=attrgetter('fitness'))
                self.gen += 1
 
                if self.optim == "max":
                    print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
                elif self.optim == "min":
                    print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
        
            # If find solution
            else:        
                
                if self.optim == "max":
                    solution = max(self, key=attrgetter("fitness"))
                    print(f'Solved SUDOKU:', sudoku_representation(solution))
                    
                elif self.optim == "min":
                    
                    solution = min(self, key=attrgetter("fitness"))
                    print(" ")
                    print('SOLVED SUDOKU:')
                    sudoku_representation(solution)
                    print("")
                    print(f'Solve in {self.gen-1} generations!')

                break
            
        end1 = timer()
        end.append(end1)
        self.save()
        print(" ")
        print(timedelta(seconds=end[0]-start))
    

    def log(self):
        with open(f'run_{self.timestamp}.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for i in self:
                writer.writerow([self.gen, i.representation, i.fitness])
 

    def save(self):
        with open(f'fitness_easy.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            best = min(self, key=attrgetter("fitness"))
            writer.writerow([self.total_gens, self.size, self.givens, self.gen-1, best.fitness, self.select_type, self.crossover_type, self.mutation_type, timedelta(seconds=end[0]-start)])




    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
