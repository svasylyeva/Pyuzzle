import random
from pandas.core.common import flatten
from random import shuffle
from random import sample

def swap_mutation(individual, quizz):
    
    # Find non fixed values
    values_index = []
    for x in range(len(quizz)):
        # Non fixed values are defined by 0 in the imported quizz
        if quizz[x] == 0:
           values_index = values_index + [x]
    
    # Get two mutation points
    mut_points = sample(values_index, 2)
    # Sort the list
    #print(mut_points)

    # Rename to shorten variable name
    i = individual

    i[mut_points[0]], i[mut_points[1]] = i[mut_points[1]], i[mut_points[0]]
    
    return i

def inversion_mutation(individual, quizz):
    
    # Find non fixed values index
    v_n_fixed_index = []
    for x in range(len(quizz)):
        # Non fixed values are defined by 0 in the imported quizz
        if quizz[x] == 0:
           v_n_fixed_index = v_n_fixed_index + [x]
    #print('v_n_fixed_index:', v_n_fixed_index)

    i = individual

    # Create new list with the values for mutation
    new = []
    for n in v_n_fixed_index:
            new.append(i[n])
    #print('new list for mutate values:', new)

    # Position of the start and end of substring
    mut_points = sample(range(len(new)), 2)
    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    #print('mut_points:', mut_points)
    # Invert for the mutation
    new[mut_points[0]:mut_points[1]] = new[mut_points[0]:mut_points[1]][::-1]
    #print('mutate list:',new)

    # Append mutated list to non fixed spaces
    for i,n in zip(v_n_fixed_index, new):
        quizz[i] = n
    #print('result:', quizz)
    

    return quizz

def scramble_mutation(individual, quizz):
    
    # Find non fixed values index
    v_n_fixed_index = []
    for x in range(len(quizz)):
        # Non fixed values are defined by 0 in the imported quizz
        if quizz[x] == 0:
           v_n_fixed_index = v_n_fixed_index + [x]
    #print('v_n_fixed_index:', v_n_fixed_index)

    i = individual

    # Create new list with the values for mutation
    new = []
    for n in v_n_fixed_index:
            new.append(i[n])
    #print('new list for mutate values:', new)

    # Random sort values in the list
    shuffle(new)
    #print('shuffle new list:', new)

    # Append mutated list to non fixed spaces
    for i,n in zip(v_n_fixed_index, new):
        quizz[i] = n
    #print('result:', quizz)
    

    return quizz


def mutation(quizz, parent, mutation):
    
    def split(arr, size = 9):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
        arrs.append(arr)
        return arrs

    slpit_quizz = split(quizz)
    split_parent = split(parent)

    # select one subgoup index
    #index = random.randrange(len(split_parent))
    index = sample(range(len(split_parent)), 3)
    #print(index)

    # Define selected subgroup for mutation
    quizz = []
    individual = []
    for i in index:
        a = list(slpit_quizz[i].copy())
        quizz.append(a)
        b = split_parent[i].copy()
        individual.append(b)

    
    # Mutate subgroup
    mutated_subgroup = []
    for x,z in zip(individual,quizz):
        list_m = mutation(x, z)
        mutated_subgroup.append(list_m)
    #print(mutated_subgroup)
    
    # Change in the string subgroup by the mutated
    for i,x in zip(index, range(len(mutated_subgroup))):
        split_parent[i] = mutated_subgroup[x]

    # Join the string in 81 elements
    parent = list(flatten(split_parent))
    quizz = list(flatten(slpit_quizz))

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

    parent = [1,5,4,3,6,7,2,8,9,
              2,3,5,4,6,9,7,8,1,
              1,7,2,5,6,7,8,4,3,
              1,3,6,4,5,2,9,8,7,
              1,9,2,3,5,7,4,6,8,
              1,5,2,4,8,3,6,7,9,
              6,2,3,4,7,8,1,9,5,
              1,2,3,5,4,8,6,9,7,
              5,4,2,9,1,6,3,7,8]

    print(mutation(quizz, parent, mutation = scramble_mutation))