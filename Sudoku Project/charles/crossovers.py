from random import randint, sample, choices
import math

def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = []
    offspring2 = []
    # Dimension of sudoku (usually 9)
    Dim = int(math.sqrt(len(p1)))
    co_point = (randint(1, Dim-1))*Dim
    #print(co_point)

    # Exchange parents' tail 
    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]
    return offspring1, offspring2

def two_points_co(p1, p2):
    """Implementation of two points crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # Dimension of sudoku (usually 9)
    Dim = int(math.sqrt(len(p1)))
    offspring1 = []
    offspring2 = []
    mut_points = sample(range(1,Dim), 2)
    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    #print('mut_points:', mut_points)
    
    # Exchange the middle part of the parents
    offspring1 = p1[:mut_points[0]*Dim] + p2[mut_points[0]*Dim:mut_points[1]*Dim] + p1[mut_points[1]*Dim:]
    offspring2 = p2[:mut_points[0]*Dim] + p1[mut_points[0]*Dim:mut_points[1]*Dim] + p2[mut_points[1]*Dim:]
    return offspring1, offspring2

def uniform_co(p1, p2):
    """Implementation of uniform crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # Dimension of sudoku (usually 9)
    Dim = int(math.sqrt(len(p1)))
    offspring1 = []
    offspring2 = []

    # Create binary mask for crossover,
    # where 1 corresponds to a Dim-sized-group('bit') taken from parent1, 
    # 0 - to a 'bit' from a parent2
    binary_mask = choices([0,1], k = Dim)
    #print (binary_mask)
    for idx, val in enumerate(binary_mask):
        if val == 1:
            offspring1 = offspring1 + p1[(idx)*Dim:(idx+1)*Dim]
            offspring2 = offspring2 + p2[(idx)*Dim:(idx+1)*Dim]
        else:
            offspring1 = offspring1 + p2[(idx)*Dim:(idx+1)*Dim]
            offspring2 = offspring2 + p1[(idx)*Dim:(idx+1)*Dim]
    return offspring1, offspring2


# Confirm how it work
if __name__ == '__main__':
    
    p1 = [1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9]
    p2 = [11,11,11,11,11,11,11,11,11,22,22,22,22,22,22,22,22,22,33,33,33,33,33,33,33,33,33,44,44,44,44,44,44,44,44,44,55,55,55,55,55,55,55,55,55,66,66,66,66,66,66,66,66,66,77,77,77,77,77,77,77,77,77,88,88,88,88,88,88,88,88,88,99,99,99,99,99,99,99,99,99]

    print(two_points_co(p1, p2))
