from random import sample

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

    for i,n in zip(v_n_fixed_index, new):
        quizz[i] = n
    #print('result:', quizz)
    

    return quizz


if __name__ == '__main__':
    quizz = [0,0,4,3,0,0,2,0,9]
    i1 = [1,5,4,3,6,7,2,8,9]

    print(inversion_mutation(i1, quizz))