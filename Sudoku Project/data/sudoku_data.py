import pandas as pd
import os
import numpy
from charles.generation import remove_blank_spaces, generate_random_solution


# Dimension of the standard sudoku game = 9 (9*9)
Dim = 9

# Upload sudoku_1000.csv file to dataframe
# Quizzes selected form kaggle and random generator 
# Links - https://www.kaggle.com/bryanpark/sudoku, https://sudoku.com/
root_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(root_dir, 'sudoku.csv')
df = pd.read_csv(path)


# easy: 38 givens (first one in sudoku.csv)
# medium: 33 givens (second one in sudoku.csv)
# dificult: 30 givens (third one in sudoku.csv)
quizz = " ".join(df['quizzes'].iloc[0])
solution = " ".join(df['solutions'].iloc[0])

# quizz to list
quizz = numpy.fromstring(quizz, dtype = int, sep = ' ')
# separate integers by ','
quizz = (remove_blank_spaces(quizz))
# count givens integers
count = len([i for i in quizz if i!=0])


# All next examples are left here for debugging


solution = numpy.fromstring(solution, dtype = int, sep = ' ')
solution = (remove_blank_spaces(solution))

wrong_solution_with_f_49 = numpy.asarray([5, 5, 4, 3, 7, 1, 2, 5, 5, 3, 5, 5, 8, 4, 9, 6, 5, 5, 9, 7, 1, 2,
       6, 5, 8, 4, 3, 4, 5, 5, 1, 9, 2, 5, 8, 7, 1, 9, 8, 6, 5, 7, 4, 3,
       2, 2, 5, 7, 4, 4, 4, 4, 4, 6, 6, 8, 9, 7, 3, 4, 1, 2, 5, 7, 1, 3,
       5, 8, 8, 2, 9, 4, 5, 4, 5, 9, 5, 5, 3, 7, 8])
wrong_solution_with_f_49 = (remove_blank_spaces(wrong_solution_with_f_49))


