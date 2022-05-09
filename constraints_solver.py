from constraint import *
import numpy as np

def solver(max_bba, min_bba, max_bbb, min_bbb):
    size_bba_x = int(max_bba[0]-min_bba[0])
    size_bba_y = int(max_bba[1]-min_bba[1])

    size_bbb_x = int(max_bbb[0]-min_bbb[0])
    size_bbb_y = int(max_bbb[1]-min_bbb[1])

    #print("bba_x, bba_y = ", new_size_bba_x, new_size_bba_y)
    #print("bbb_x, bbb_y = ", new_size_bbb_x, new_size_bbb_y)

    #size_bba_x = 2
    #size_bba_y = 2

    #size_bbb_x = 2
    #size_bbb_y = 2

    grid = list(np.arange(0,4000))

    problem = Problem()
    problem.addVariable("maxA_x", grid)
    problem.addVariable("minA_x", grid)
    problem.addVariable("maxB_x", grid)
    problem.addVariable("minB_x", grid)

    problem.addVariable("maxA_y", grid)
    problem.addVariable("minA_y", grid)
    problem.addVariable("maxB_y", grid)
    problem.addVariable("minB_y", grid)

    """problem.addConstraint(lambda maxA_x : maxA_x == 700, ("maxA_x"))
    problem.addConstraint(lambda minA_x : minA_x == 100, ("minA_x"))
    problem.addConstraint(lambda minA_y : minA_y == 100, ("minA_y"))
    problem.addConstraint(lambda maxA_y : minA_y == 700, ("maxA_y"))"""
    #taille fixe des bouding box (x pour A)
    problem.addConstraint(lambda minA_x, maxA_x : abs(minA_x - maxA_x) == size_bba_x, ("minA_x", "maxA_x") )

    #taille fixe des bouding box (x pour B)
    problem.addConstraint(lambda minB_x, maxB_x : abs(minB_x - maxB_x) == size_bbb_x, ("minB_x", "maxB_x") )

    #taille fixe des bouding box (y pour A)
    problem.addConstraint(lambda minA_y, maxA_y : abs(minA_y - maxA_y) == size_bba_y, ("minA_y", "maxA_y"))

    #taille fixe des bouding box (y pour B)
    problem.addConstraint(lambda minB_y, maxB_y : abs(minB_y - maxB_y) == size_bbb_y, ("minB_y", "maxB_y"))

    #les x ne se chevauchent pas
    problem.addConstraint(lambda minA_x, maxA_x, maxB_x, minB_x :
                            minA_x <= maxB_x and maxA_x >= minB_x,
                              ("minA_x", "maxA_x", "maxB_x", "minB_x" ))

    #minimiser l'écart entre les x
    #problem.addConstraint(ExactSumConstraint(50),
    #                          abs(minA_x - minB_x))

    #minimiser l'écart entre les y

    #les y ne se chevauchent pas
    problem.addConstraint(lambda minA_y, maxA_y, maxB_y, minB_y :
                            minA_y <= maxB_y and maxA_y >= minB_y,
                              ("minA_y", "maxA_y", "maxB_y", "minB_y" ))

    step = 500
    #ajouter un pas de step pour x
    problem.addConstraint(lambda minA_x, maxA_x, minB_x, maxB_x :
                            minA_x % step == 0 and
                            minB_x % step == 0 and
                            maxB_x % step == 0 and
                            maxA_x % step == 0,
                             ("minA_x","maxA_x", "minB_x", "maxB_x"))

    #ajouter un pas de step pour y
    problem.addConstraint(lambda minA_y, maxA_y, minB_y, maxB_y :
                            minA_y % step == 0 and
                            minB_y % step == 0 and
                            maxB_y % step == 0 and
                            maxA_y % step == 0,
                             ("minA_y","maxA_y", "minB_y", "maxB_y"))

    #contraintes évidentes pour gagner du temps de compilation
    problem.addConstraint(AllDifferentConstraint())



    res = problem.getSolutions()
    print(len(res))
    """for i in range(len(res)):
        print("res",i, ": \t", res[i])"""
