import random
import read_homeByMe

PENALTY_SAME_TYPE = 15
PENALTY_SAME_OBJECT = 30

def randomSolution(nb_accessories, accessories):
    solution = []
    for i in range(nb_accessories):
        rd_idx = random.randint(0,len(accessories)-1)
        solution.append(accessories[rd_idx])
    return solution


def computeReward(solution):
    reward = 0
    for i in range(len(solution)):
        dict1 = solution[i]
        for j in range(i+1, len(solution)):
            dict2 = solution[j]
            is_same_type = read_homeByMe.check_type(dict1.get('type'), dict2.get('type'))
            if is_same_type :
                reward = reward-PENALTY_SAME_TYPE
            if dict1.get('reference') == dict2.get('reference'):
                reward = reward-PENALTY_SAME_OBJECT
        reward += int(dict1.get('value'))
    return reward


def getBestNeighbour(neighbours):
    bestReward = computeReward(neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentReward = computeReward(neighbour)
        if currentReward > bestReward:
            bestReward = currentReward
            bestNeighbour = neighbour
    return bestNeighbour, bestReward

#un voisin de accessories est accessories avec un accessoire modifié (en prenant un accessoire au hasard dans accessories)
#on considère que l'on effectue 10 modifications par éléments de la liste
def getNeighbours(solution, accessories):
    neighbours = []
    for i in range(len(solution)):
        for j in range(2):
            rd_idx = random.randint(0, len(accessories)-1)
            neighbour = solution.copy()
            neighbour[i] = accessories[rd_idx]
            neighbours.append(neighbour)
    return neighbours

def printReferences(accessories):
    res = []
    for accessory in accessories:
        res.append(accessory.get('reference'))
    return res

def printRefNeighbours(neighbours):
    print("-----neighbours-----")
    for neighbour in neighbours:
        res= printReferences(neighbour)
        print(res, computeReward(neighbour))

def hillClimbing(nb_accessories, accessories, nb_iter = 5):
    bestSolution = randomSolution(nb_accessories, accessories)
    bestReward = computeReward(bestSolution)

    neighbours = getNeighbours(bestSolution, accessories)
    bestNeighbour, bestNeighbourReward = getBestNeighbour(neighbours)

    print("bestSolution =", printReferences(bestSolution), "currentReward=", bestReward)
    print("bestNeighbour", printReferences(bestNeighbour), "bestNeighbourReward=", bestNeighbourReward)

    if bestNeighbourReward > bestReward :
        print("NEW BEST:", printReferences(bestNeighbour), "reward=", bestNeighbourReward)
        bestSolution, bestReward = bestNeighbour, bestNeighbourReward

    cpt = 0
    #while bestReward > currentReward:
    while cpt < nb_iter :
        print("------TOUR", cpt,"--------------")
        print("best solution=", printReferences(bestSolution), "best reward=", bestReward)

        neighbours = getNeighbours(bestSolution, accessories)
        printRefNeighbours(neighbours)


        bestNeighbour, bestNeighbourReward = getBestNeighbour(neighbours)
        print("bestNeighbour=", printReferences(bestNeighbour), "bestNeighbourReward=", bestNeighbourReward)

        if bestNeighbourReward > bestReward :
            print("NEW BEST:", printReferences(bestNeighbour), "reward=", bestNeighbourReward)
            bestSolution, bestReward = bestNeighbour, bestNeighbourReward
        cpt += 1

    return bestSolution, bestReward


nb_accessories = 2

accessories = [{'reference' : 'patate', 'type' : 'féculent' , 'value' : '3'} ,
 {'reference' : 'banane', 'type' : 'fruit' , 'value' : '5'},
 {'reference' : 'pates', 'type' : 'féculent' , 'value' : '3'},
 {'reference' : 'courgette', 'type' : 'légume' , 'value' : '1'},
 {'reference' : 'brocoli', 'type' : 'légume' , 'value' : '2'},
 {'reference' : 'pomme', 'type' : 'fruit' , 'value' : '10'},
 {'reference' : 'kiwi', 'type' : 'fruit' , 'value' : '0'},
 {'reference' : 'aubergine', 'type' : 'légume' , 'value' : '3'},
 {'reference' : 'concombre', 'type' : 'légume' , 'value' : '2'},
 {'reference' : 'boeuf', 'type' : 'viande' , 'value' : '10'},
 {'reference' : 'saumon', 'type' : 'viande' , 'value' : '30'},
 {'reference' : 'thon', 'type' : 'viande' , 'value' : '10'},
 {'reference' : 'riz', 'type' : 'féculent' , 'value' : '5'},
 {'reference' : 'lait', 'type' : 'produit laitier' , 'value' : '3'},
 {'reference' : 'fromage', 'type' : 'produit laitier' , 'value' : '4'},
 {'reference' : 'yaourt', 'type' : 'produit laitier' , 'value' : '4'}]
solution, reward = hillClimbing(nb_accessories, accessories, 5)
print("\n \n best solution is", printReferences(solution), "with a score of", reward)
