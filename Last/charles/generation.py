import pandas as pd
import os
import numpy
import random
from random import sample

def remove_blank_spaces(quizz_to_populate):
    filtered_quizz = [x for x in quizz_to_populate if x!=" "]
    return filtered_quizz

def populate_row(row_n):
    available_numbers = [x for x in list(range(1, 10)) if x not in row_n]
    for i, n in enumerate(row_n):
        if n==0:
            random_index = random.randrange(len(available_numbers))
            row_n[i] = available_numbers[random_index]
            available_numbers.pop(random_index)
    return row_n

def generate_random_solution(quizz_to_populate):
    populated_quizz = []
    index = 0
    for i in range(9):
        populated_quizz+=populate_row(quizz_to_populate[index:index+9])
        index+=9
    return populated_quizz

def sudoku_representation(quizz):
    index = 0
    matrix = []
    for i in range(9):
        print(f'                    ', quizz[index:index+9])
        index+=9

if __name__ == '__main__':
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root_dir, '../data/sudoku1000.csv')
    df = pd.read_csv(path)

    random_index = 0
    # Take a random quiz from the file
    quizz_temp = remove_blank_spaces(" ".join(df['quizzes'].iloc[random_index]))
    quizz = [int(string) for string in quizz_temp]
    solution_temp = remove_blank_spaces(" ".join(df['solutions'].iloc[random_index]))
    solution = [int(string) for string in solution_temp]

    print("Starting quizz:")
    print(quizz)
    print("Randomly populated quizz:")
    print(generate_random_solution(quizz))

    