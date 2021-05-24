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
    #def __repr__(self):
    #    return f"Individual: {self.representation}; Fitness: {self.fitness}"

class Population:
    def __init__(self, size, optim):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.gen = 1
        self.timestamp = int(time.time())
        for _ in range(size):
            self.individuals.append(
                Individual(representation = generate_random_solution(quizz))
            )

        

    def evolve(self, gens, select, crossover, mutation, mutations, mutation_type, co_p, mu_p,  quizz, elitism, what):
        count = 0

        for gen in range(gens):
            new_pop = []
            new_elitesi = []
            
 
            if elitism == True:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

                # Find best individual
                best = deepcopy(min(self.individuals, key=attrgetter("fitness")))
                if elite.fitness == best.fitness:
                    new_elite =  mutation(quizz, mutation(quizz, elite.representation, 'columns'), 'rows')
                    new_elite = Individual(new_elite)
                    if new_elite.fitness < elite.fitness:
                        elite = new_elite
                

                
                #if elite.fitness >= best.fitness:
                 #   new_elites = mutations(quizz, best.representation, mutation_type, 1)
                    #new_elites = mutation(quizz, mutation(quizz, best.representation, 'columns'), 'rows')
                 #   new_elitesi = Individual(representation = new_elites)
                    
                  #  elite = new_elitesi


        
            while len(new_pop) < self.size:
                parent1 = select(self)
                parent2 = select(self)
                while parent1==parent2:
                    parent2 = select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1.representation, parent2.representation)
                else:
                    offspring1, offspring2 = parent1.representation, parent2.representation
                # Mutation
                if random() < mu_p:
                    offspring1 = mutations(quizz, offspring1, mutation_type, 4)
                    #offspring1 = mutation(quizz, mutation(quizz, offspring1, 'columns'), 'rows')

                if random() < mu_p:
                    offspring2 = mutations(quizz, offspring2, mutation_type, 4)
                    #offspring2 = mutation(quizz, mutation(quizz, offspring2, 'columns'), 'rows')

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
                    count +=1
                    if count==5:
                        elite.fitness += 1
                        count = 0
                    else:
                        pass
                else:
                    count = 0
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
        
        
