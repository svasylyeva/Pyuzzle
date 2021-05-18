from random import sample

def pmx_co(p1, p2, quizz):

    # Find non fixed values index
    v_n_fixed_index = []
    for x in range(len(quizz)):
        # Non fixed values are defined by 0 in the imported quizz
        if quizz[x] == 0:
           v_n_fixed_index = v_n_fixed_index + [x]
    #print('v_n_fixed_index:', v_n_fixed_index)

    # Create new list with the values for mutation
    new1 = []
    for n in v_n_fixed_index:
            new1.append(p1[n])
    #print('new list for mutate values 1:', new1)

    # Create new list with the values for mutation
    new2 = []
    for n in v_n_fixed_index:
            new2.append(p2[n])
    #print('new list for mutate values 2:', new2)
 
    
    # Sample 2 random co points
    co_points = sample(range(len(new1)), 2)
    co_points.sort()
    #print('index to cross:  ',co_points)

    def PMX(x, y):
        # Create placeholder for offspring
        o = [None] * len(x)

        # Copy co segment into offspring
        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

        # Find set of values not in offspring from co segment in P2
        z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])
        #print('points not in cross for same index:  ',z)

        # Map values in set to corresponding position in offspring
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] != None:
                temp = index
                index = y.index(x[temp])
            o[index] = i
        # Fill in remaining values
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    # Call function twice with parents reversed
    o1, o2 = (
        PMX(new1, new2),
        PMX(new2, new1)
    )
    #print('cross list 1:  ',o1)
    #print('cross list 2:  ',o2)

    quizz1 = quizz.copy()
    quizz2 = quizz.copy()
    # Append cross list to non fixed spaces
    for i,n in zip(v_n_fixed_index, o1):
        quizz1[i] = n
    #print('result:', quizz)

    for i,n in zip(v_n_fixed_index, o2):
        quizz2[i] = n
    #print('result:', quizz)

    return quizz1, quizz2


if __name__ == '__main__':

    quizz = [0,0,4,3,0,0,2,0,9]
    p1 = [1,5,4,3,6,7,2,8,9]
    p2 = [7,8,4,3,1,5,2,6,9]

    print(pmx_co(p1, p2, quizz))