from constraint import *
import numpy as np

size_bba_x = 2
size_bba_y = 2

size_bbb_x = 2
size_bbb_y = 2

grid = list(np.arange(0,4))

problem = Problem()
problem.addVariable("maxA_x", grid)
problem.addVariable("minA_x", grid)
problem.addVariable("maxB_x", grid)
problem.addVariable("minB_x", grid)

problem.addVariable("maxA_y", grid)
problem.addVariable("minA_y", grid)
problem.addVariable("maxB_y", grid)
problem.addVariable("minB_y", grid)

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

#les y ne se chevauchent pas
problem.addConstraint(lambda minA_y, maxA_y, maxB_y, minB_y :
                        minA_y <= maxB_y and maxA_y >= minB_y,
                          ("minA_y", "maxA_y", "maxB_y", "minB_y" ))

res = problem.getSolutions()
for i in range(len(res)):
    print("res",i, ": \t", res[i])




"""problem.addConstraint(lambda minA_x, maxA_x, maxB_x, minB_x, maxA_y, minA_y, maxB_y, minB_y  :
                        minA_x <= maxB_x and maxA_x >= minB_x,
                          ("a", "b"))"""

"""(a.minX <= b.maxX && a.maxX >= b.minX) &&
         (a.minY <= b.maxY && a.maxY >= b.minY) &&
         (a.minZ <= b.maxZ && a.maxZ >= b.minZ);"""
