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
if __name__ == '__main__':
    
    #p1 = [1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9]
    #p2 = [11,11,11,11,11,11,11,11,11,22,22,22,22,22,22,22,22,22,33,33,33,33,33,33,33,33,33,44,44,44,44,44,44,44,44,44,55,55,55,55,55,55,55,55,55,66,66,66,66,66,66,66,66,66,77,77,77,77,77,77,77,77,77,88,88,88,88,88,88,88,88,88,99,99,99,99,99,99,99,99,99]
    p1 = [1,5,4,3,6,7,2,8,9,
          2,3,5,4,6,9,7,8,1,
          1,7,2,5,6,7,8,4,3,
          1,3,6,4,5,2,9,8,7,
          1,9,2,3,5,7,4,6,8,
          1,5,2,4,8,3,6,7,9,
          6,2,3,4,7,8,1,9,5,
          1,2,3,5,4,8,6,9,7,
          5,4,2,9,1,6,3,7,8]

    p2 = [8,7,4,3,6,5,2,1,9,
          8,7,5,6,4,9,3,2,1,
          9,7,8,5,6,2,1,4,3,
          9,5,6,4,3,2,1,8,7,
          1,9,8,6,5,7,4,3,2,
          9,5,7,6,8,3,4,2,1,
          6,9,8,7,4,3,1,2,5,
          7,4,3,5,2,8,6,9,1,
          8,4,2,9,1,7,3,6,5]

            
    print(two_points_co(p1, p2))

    #[8, 6, 4, 3, 7, 1, 2, 5, 9,
    # 3, 2, 5, 8, 4, 9, 7, 6, 1, 
    # 9, 7, 1, 2, 6, 5, 8, 4, 3, 
    # 4, 3, 6, 1, 9, 2, 5, 8, 7, 
    # 1, 9, 8, 6, 5, 7, 4, 3, 2, 
    # 2, 5, 7, 4, 8, 3, 9, 1, 6, 
    # 6, 8, 9, 7, 3, 4, 1, 2, 5, 
    # 7, 1, 3, 5, 2, 8, 6, 9, 4, 
    # 5, 4, 2, 9, 1, 6, 3, 7, 8]

    #[8, 6, 4, 3, 7, 1, 2, 5, 9, 
    # 4, 7, 5, 2, 3, 9, 8, 6, 1, 
    # 2, 7, 1, 5, 6, 9, 8, 4, 3, 
    # 3, 9, 6, 1, 5, 2, 4, 8, 7, 
    # 1, 9, 8, 6, 5, 7, 4, 3, 2, 
    # 2, 5, 7, 6, 8, 3, 1, 9, 4, 
    # 6, 3, 9, 7, 8, 4, 1, 2, 5, 
    # 7, 1, 3, 5, 2, 8, 6, 9, 4, 
    # 5, 4, 2, 9, 1, 6, 3, 7, 8]