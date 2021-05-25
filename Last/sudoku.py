from charles.charles_sudoku import Individual, Population
from data.sudoku_data import quizz, Dim
from charles.selection import fps, tournament, rank
from charles.mutation import mutation, swap_mutation, inversion_mutation, scramble_mutation
from charles.crossovers import single_point_co, two_points_co, uniform_co
from copy import deepcopy
from charles.mutation1 import mutate_column_row


#from random import random, choices
#from operator import  attrgetter
#import csv
#import numpy


def evaluate(self):
     """A fitness function 

    Returns:
        int: sum
    """

     fitness = 0

     # Fitness function for now only penalizes violation of the rules 1-3
     #  of rules ( rules of the game - link https://www.sudokuonline.io/tips/sudoku-rules )
     # Adding some penalty scores for violation (assuming that it will be a minimization problem )
     rows = [list() for _ in range(Dim)]
     #print(rows)
     columns = [list() for _ in range(Dim)]
     #print(columns)
     blocks = [list() for _ in range(Dim)]
     #print(blocks)
     for row in range(Dim):
          
          for column in range(Dim):
               
               value = self.representation[row * Dim + column]
               rows[row].append(value)
               columns[column].append(value)
               blocks[(row //3)*3 + (column//3)].append(value)
               
     set_r = sum(abs(len(set(row)) - Dim) for row in rows)
     set_c = sum(abs(len(set(column)) - Dim) for column in columns)
     set_b = sum(abs(len(set(block)) - Dim) for block in blocks)
    
     fitness = set_r + set_c + set_b
     # This fitness function maybe will be edited in the future
     return fitness




def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n

Individual.evaluate = evaluate
Individual.get_neighbours = get_neighbours

#print(Individual(popul))

pop = Population(

    size=1000,
    optim="min",
)

pop.evolve(
    gens=50, 
    select= rank,
    crossover= single_point_co,
    mutation=mutate_column_row,
    mutations=mutation,
    mutation_type=swap_mutation,
    what='columns',
    co_p=0.7,
    mu_p=0.3,
    quizz = quizz,
    elitism=True
)

