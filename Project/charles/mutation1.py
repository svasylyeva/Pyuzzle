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
    print(mut_points)

    # Rename to shorten variable name
    i = individual

    i[mut_points[0]], i[mut_points[1]] = i[mut_points[1]], i[mut_points[0]]
    
    return i

if __name__ == '__main__':
    quizz = [0,0,4,3,0,0,2,0,9]
    #i1 = [1,2,3,4,5,6,7,8,9]
    i1 = [1,5,4,3,6,7,2,8,9]

    print(swap_mutation(i1,quizz))

# index of non fixed values, only these values can mutate
# [0, 1, 4, 5, 7]


