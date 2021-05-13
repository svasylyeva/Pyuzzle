from charles.charles_sudoku import Individual
#from charles.selection import fps, tournament, rank
#from charles.mutation import swap_mutation
#from charles.crossover import cycle_co, pmx_co
from random import choices

from data.sudoku_data import quizz, Dim, solution
#from charles.selection import fps, tournament, rank
#from charles.mutation import binary_mutation
#from charles.crossover import single_point_co
from random import random
from operator import  attrgetter
import csv


def evaluate(self):
     """A fitness function 

    Returns:
        int: sum
    """
     fitness = 0
     # First attempt - DEPRECATED
     # rows = [set() for _ in range(Dim)]
     # columns = [set() for _ in range(Dim)]
     # sections = [set() for _ in range(Dim)]
     # for row in range(Dim):
     #      for column in range(Dim):
     #           value = self.representation[row * Dim + column]
     #           rows[row].add(value)
     #           columns[column].add(value)
     #           sections[(row //3)*3 + (column//3)].add(value)
     # fitness = sum(len(row) == Dim for row in rows) + sum(len(column) == Dim for column in columns) + sum(len(section) == Dim for section in sections)
     
     fitness = 0

     # Fitness function for now only penalizes violation of the rules 1-3
     #  of rules ( rules of the game - link https://www.sudokuonline.io/tips/sudoku-rules )
     # Adding some penalty scores for violation (assuming that it will ne minimization problem )
     rows = [list() for _ in range(Dim)]
     columns = [list() for _ in range(Dim)]
     blocks = [list() for _ in range(Dim)]
     for row in range(Dim):
          for column in range(Dim):
               value = self.representation[row * Dim + column]
               rows[row].append(value)
               columns[column].append(value)
               blocks[(row //3)*3 + (column//3)].append(value)
               
     set_r = sum(abs(len(set(row)) - 9) for row in rows)
     set_c = sum(abs(len(set(column)) - 9) for column in columns)
     set_b = sum(abs(len(set(block)) - 9) for block in blocks)
    
     fitness = set_r + set_c + set_b
     # Fitness function will be edited in the future
     return fitness
     
     
     return fitness

# Monkey Patching
Individual.evaluate = evaluate
