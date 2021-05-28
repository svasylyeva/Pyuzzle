from random import random
from operator import  attrgetter
from copy import deepcopy
import csv
import time
from charles.generation import generate_random_solution, sudoku_representation
from data.sudoku_data import quizz, count
from timeit import default_timer as timer
from datetime import timedelta

# Start count the time
start = timer()
# For append the ending time
end = []


class Individual:
    def __init__(
        self,
        representation=None,
    ):
        if representation == None:
            # Create individual with random values in non fixed values
            self.representation = generate_random_solution(quizz)
        else:
            self.representation = representation

        self.fitness = self.evaluate()

    def evaluate(self):
        raise Exception("You need to monkey patch the fitness function.")

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
        # Some information only for save results
        self.givens = count
        self.total_gens = total_gens
        self.select_type = select_type
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.timestamp = int(time.time())

        for _ in range(size):
            # Create random n individuals for the population
            self.individuals.append(
                Individual(representation = generate_random_solution(quizz))
            )

        
    def evolve(self, gens, select, crossover, mutations, mutation_type, co_p, mu_p,  quizz, elitism):

        for gen in range(gens):
            
            # Find individual with best fitness (minimum, in this problem)
            best_fitness = min(self, key=attrgetter("fitness"))
            

            #To avoid earlier convergence, however it not help to solve faster the quizz:
            # Create new individuals for diversificate the population
            #if gen >= 1:
            #    new_random_pop = []
            #    old_population = []
            #    for i in range(int((self.size)/2)):
            #        new = Individual(representation = generate_random_solution(quizz))
            #        new_random_pop.append(new)
            #        old_population.append(self.individuals[i])
            #    self.individuals = new_random_pop + old_population'''



            # If not find solution
            if best_fitness.fitness != 0:
                
                new_pop = []
 
                if elitism == True:
                    # Define the elite
                    if self.optim == "max":
                        elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                    elif self.optim == "min":
                        elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))
                
                while len(new_pop) < self.size:
                    parent1 = select(self)
                    parent2 = select(self)

                    # Crossover
                    if random() < co_p:
                        offspring1, offspring2 = crossover(parent1.representation, parent2.representation)
                    else:
                        offspring1, offspring2 = parent1.representation, parent2.representation
                    # Mutation
                    if random() < mu_p:
                        # Mutate 2 subgroups
                        offspring1 = mutations(quizz, offspring1, mutation_type, 2)
                    if random() < mu_p:
                        # Mutate 2 subgroups
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
                
                    # To avoid early convergence
                    # Define the best individual created with crossover and mutation
                    best = deepcopy(min(new_pop, key=attrgetter("fitness")))
                    if elite.fitness == best.fitness:
                        # Add 1 to divercificate individuals in population
                        elite.fitness += 1
                    else:
                        pass
                    # append the elite to the population
                    new_pop.append(elite)

                #self.log()
                self.individuals = new_pop

                #If new population is created:
                # sort before add new population
                #self.individuals = sorted(new_pop,reverse=False, key=attrgetter('fitness'))

                # Next generation 
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
                    # Save the individual that has the minimum fitness(zero)
                    solution = min(self, key=attrgetter("fitness"))
                    print(" ")
                    print('SOLVED SUDOKU:')
                    sudoku_representation(solution)
                    print("")
                    print(f'Solve in {self.gen-1} generations!')

                break

        # End time
        end1 = timer()
        end.append(end1)

        # Save all results
        self.save()
        print(" ")
        # How mutch time the quizz take to be solved
        print(timedelta(seconds=end[0]-start))
    

    # Save all individuals created in the population on all generations
    def log(self):
        with open(f'run_{self.timestamp}.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for i in self:
                writer.writerow([self.gen, i.representation, i.fitness])
 

    # Save results for analysis
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
