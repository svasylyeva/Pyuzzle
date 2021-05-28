import pandas as pd
import os
import numpy
from charles.generation import remove_blank_spaces, generate_random_solution
# easy: 38,35
# medium: 30,28
# dificult: 26,25

# Dimension of the standard sudoku game = 9 (9*9)
Dim = 9

# Upload sudoku_1000.csv file to dataframe
# sudoku_100.csv - first 1000 sudoku quizzes from 1 million sudoku games:
# Link - https://www.kaggle.com/bryanpark/sudoku
root_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(root_dir, 'sudoku.csv')
df = pd.read_csv(path)

# Take first quizz, will be changed to a random quizz from df afterwards

quizz = " ".join(df['quizzes'].iloc[0])
solution = " ".join(df['solutions'].iloc[0])
quizz = quizz.replace('.','0')


# All next examples are left here for debugging

quizz = numpy.fromstring(quizz, dtype = int, sep = ' ')
quizz = (remove_blank_spaces(quizz))
count = len([i for i in quizz if i!=0])

solution = numpy.fromstring(solution, dtype = int, sep = ' ')
solution = (remove_blank_spaces(solution))

wrong_solution_with_f_49 = numpy.asarray([5, 5, 4, 3, 7, 1, 2, 5, 5, 3, 5, 5, 8, 4, 9, 6, 5, 5, 9, 7, 1, 2,
       6, 5, 8, 4, 3, 4, 5, 5, 1, 9, 2, 5, 8, 7, 1, 9, 8, 6, 5, 7, 4, 3,
       2, 2, 5, 7, 4, 4, 4, 4, 4, 6, 6, 8, 9, 7, 3, 4, 1, 2, 5, 7, 1, 3,
       5, 8, 8, 2, 9, 4, 5, 4, 5, 9, 5, 5, 3, 7, 8])
wrong_solution_with_f_49 = (remove_blank_spaces(wrong_solution_with_f_49))

#popul = generate_random_solution(remove_blank_spaces(quizz))

