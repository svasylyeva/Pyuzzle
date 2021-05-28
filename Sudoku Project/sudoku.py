from charles.generation import sudoku_representation
from charles.charles_sudoku import Individual, Population
from data.sudoku_data import quizz, Dim, count
from charles.selection import fps, tournament, rank
from charles.mutation import mutation, swap_mutation, inversion_mutation, scramble_mutation
from charles.crossovers import single_point_co, two_points_co, uniform_co
from copy import deepcopy


def evaluate(self):
     """A fitness function 

    Returns:
        int: sum
    """

     fitness = 0

     # Fitness function for now only penalizes violation of the rules 1-3
     # of rules ( rules of the game - link https://www.sudokuonline.io/tips/sudoku-rules )
     # Adding some penalty scores for violation (assuming that it will be a minimization problem )
     rows = [list() for _ in range(Dim)]
     #print(rows)
     columns = [list() for _ in range(Dim)]
     #print(columns)
     blocks = [list() for _ in range(Dim)]
     #print(blocks)

     # Set each value in the 81-string to the respective row set, column set and block set
     for row in range(Dim):
          
          for column in range(Dim):
               
               value = self.representation[row * Dim + column]
               # Row set
               rows[row].append(value)
               # Column set
               columns[column].append(value)
               # Block set
               blocks[(row //3)*3 + (column//3)].append(value)

     # Calculate a sum of missing digits in each row set
     set_r = sum(abs(len(set(row)) - Dim) for row in rows)
     # Calculate a sum of missing digits in each column set
     set_c = sum(abs(len(set(column)) - Dim) for column in columns)
     # Calculate a sum of missing digits in each block set
     set_b = sum(abs(len(set(block)) - Dim) for block in blocks)
     
     # Calculate the fitness
     fitness = set_r + set_c + set_b
     
     return fitness



print("")
print('Givens: ', count)
print("")
print("SUDOKU TO BE SOLVED:")
sudoku_representation(quizz)
print("")


Individual.evaluate = evaluate

pop = Population(
    size=1000,
    optim="min",
    total_gens='250', 
    select_type= 'rank',
    crossover_type= 'single_point_co',
    mutation_type='swap_mutation',

)

pop.evolve(
    gens=250, 
    select= rank,
    crossover= single_point_co,
    mutations=mutation,
    mutation_type=swap_mutation,
    co_p=0.7,
    mu_p=0.3,
    quizz = quizz,
    elitism=True
)



