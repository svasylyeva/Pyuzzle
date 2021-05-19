import random
from pandas.core.common import flatten
from mutation1 import swap_mutation
from mutation2 import inversion_mutation
from mutation3 import scramble_mutation

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
    index = random.randrange(len(split_parent))
    #print(index)

    # Define selected subgroup for mutation
    quizz = slpit_quizz[index].copy()
    individual = split_parent[index].copy()
    
    # Mutate subgroup
    mutated_subgroup = mutation(individual, quizz)
    #print(slpit_quizz[index])
    #print(split_parent[index])
    #print(mutated_subgroup)

    # Change in the string subgroup by the mutated
    split_parent[index] = mutated_subgroup

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
