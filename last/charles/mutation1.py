import random
from pandas.core.common import flatten
from random import shuffle
from random import sample
from charles.generation import generate_random_solution

def non_fixed_index(quizz):

    # Find non fixed values index
    lista = []
    for q in quizz:
        v_n_fixed_index = []
        for x in range(len(q)):
            # Non fixed values are defined by 0 in the imported quizz
            if q[x] == 0:
                v_n_fixed_index = v_n_fixed_index + [x]
        #print('v_n_fixed_index:', v_n_fixed_index)
        lista.append(v_n_fixed_index)
    #print(lista)

    return lista

# New list for change values
def new_list(quizz, individual):
    
    # Find non fixed values index
    lista = non_fixed_index(quizz)
    #print(lista)
    
    # Create new list with the values for mutation
    lista_mutate = []
    for l,i in zip(lista,individual):
        #print(l)
        new = []
        for n in l:
            new.append(i[n])
        #print('new list for mutate values:', new)
        lista_mutate.append(new)
    #print(lista_mutate)

    # Append mutated list to non fixed spaces
    #for i,n in zip(v_n_fixed_index, new):
    #    quizz[i] = n
    #print('result:', quizz)

    return lista_mutate

# Define column list
def row_column(quizz, what):

    Dim = 9
    rows = [list() for _ in range(Dim)]
    #print(rows)
    columns = [list() for _ in range(Dim)]
    #print(columns)
    blocks = [list() for _ in range(Dim)]
    #print(blocks)
    for row in range(Dim):
        for column in range(Dim):      
            value = quizz[row * Dim + column]
            rows[row].append(value)
            columns[column].append(value)
            blocks[(row //3)*3 + (column//3)].append(value)
    
    if what == 'columns':
        return columns
    elif what == 'rows':
        return rows
    else:
        return blocks

def mutate_column_row(quizz, parent, what):
    
    # FUNCTION ROW_COLUMN
    quizz1 = row_column(quizz, what)
    #print(quizz1)
    parent1 = row_column(parent, what)
    #print(parent1)

    if what=='rows':
        index = sample(range(len(quizz1)), 9)
        index.sort()
        #print(index)

    else:
        index = sample(range(len(quizz1)), 2)
        index.sort()
        #print(index)
    
    quizz1_column = []
    for i in index:
        a = quizz1[i]
        quizz1_column.append(a)
    #print(quizz1_column)
    
    parent1_column = []
    for i in index:
        a = parent1[i]
        parent1_column.append(a)
    #print(parent1_column)

    # FUNCTION NEW_LIST
    parent1_list = new_list(quizz1_column, parent1_column)
    #print(parent1_list)

    # Change duplicate by 0
    for p in parent1_list:
        seen = set()
        for i, e in enumerate(p):
            if e in seen:
                p[i] = 0
            else:
                seen.add(e)
    #print(parent1_list)

    for p,q in zip(parent1_list,quizz1_column):
        seen = set(q)
        for i, e in enumerate(p):
            if e in seen:
                p[i] = 0
            else:
                seen.add(e)
    #print(parent1_list)

    # FUNCTION NON_FIXED_INDEX
    n_fixed_index = non_fixed_index(quizz1_column)

    join_mutate = []
    for n, p, q in zip(n_fixed_index, parent1_list, quizz1_column):
        for x, z in zip(n, p):
            q[x] = z
        join_mutate.append(q)
    #print(join_mutate)

    # FUNCTION GENERATE_RANDOM_SOLUTION
    random_solution = []
    for i in join_mutate:
        a = generate_random_solution(i)
        random_solution.append(a)
    #print(random_solution)

    # Change in the string subgroup by the mutated
    for i,x in zip(index, range(len(random_solution))):
        parent1[i] = random_solution[x]
    #print(parent1)

    if what == 'columns':
        # Join the string in 81 elements
        string = []
        for a in range(len(parent1)):
            for i in parent1:
                r = i[a]
                string.append(r)
        #print(string)
        return string

    elif what == 'rows':
        # Join the string in 81 elements
        parent = list(flatten(parent1))
        #quizz = list(flatten(slpit_quizz))

    else:
        parent = []
        for x,y,z in zip(parent1[0:1],parent1[1:2],parent1[2:3]):
            parent += (x[0:3]) + (y[0:3]) + (z[0:3])
            parent += (x[3:6]) + (y[3:6]) + (z[3:6])
            parent += (x[6:9]) + (y[6:9]) + (z[6:9])

        for x,y,z in zip(parent1[3:4],parent1[4:5],parent1[5:6]):
            parent += (x[0:3]) + (y[0:3]) + (z[0:3])
            parent += (x[3:6]) + (y[3:6]) + (z[3:6])
            parent += (x[6:9]) + (y[6:9]) + (z[6:9])

        for x,y,z in zip(parent1[6:7],parent1[7:8],parent1[8:9]):
            parent += (x[0:3]) + (y[0:3]) + (z[0:3])
            parent += (x[3:6]) + (y[3:6]) + (z[3:6])
            parent += (x[6:9]) + (y[6:9]) + (z[6:9])

        return parent




if __name__ == '__main__':
        
    quizz = [0,0,4,3,0,0,2,0,9,
            0,0,5,0,0,9,0,0,1,
            0,7,0,0,6,0,0,4,3,
            0,0,6,0,0,2,0,8,7,
            1,9,0,0,0,7,4,0,0,
            0,5,0,0,8,3,0,0,0,
            6,0,0,0,0,0,1,0,5,
            0,0,3,5,0,8,6,9,0,
            0,4,2,9,1,0,3,0,0]

    parent = [1, 8, 4, 3, 5, 6, 2, 7, 9, 
              3, 4, 5, 2, 8, 9, 7, 6, 1, 
              2, 7, 9, 1, 6, 5, 8, 4, 3, 
              4, 5, 6, 1, 3, 2, 9, 8, 7, 
              1, 9, 8, 6, 2, 7, 4, 3, 5, 
              1, 5, 4, 9, 8, 3, 7, 6, 2, 
              6, 3, 8, 7, 9, 4, 1, 2, 5, 
              1, 7, 3, 5, 2, 8, 6, 9, 4, 
              5, 4, 2, 9, 1, 6, 3, 7, 8]

    parent1 = [9, 8, 4, 3, 5, 6, 2, 7, 9,
              3, 4, 5, 2, 4, 9, 7, 6, 1, 
              2, 7, 9, 1, 6, 5, 8, 4, 3, 
              4, 5, 6, 1, 3, 2, 9, 8, 7, 
              1, 9, 8, 6, 2, 7, 4, 3, 5, 
              7, 5, 4, 9, 8, 3, 7, 6, 2, 
              6, 3, 8, 7, 9, 4, 1, 2, 5, 
              8, 7, 3, 5, 7, 8, 6, 9, 4, 
              5, 4, 2, 9, 1, 6, 3, 7, 8]


    #print(row_column(parent, 'columns'))
    #print(row_column(quizz, 'columns'))


    print(mutate_column_row(quizz, parent, 'b'))
    #print(mutate_column_row(quizz, mutate_column_row(quizz, parent1, 'columns'), 'rows'))



