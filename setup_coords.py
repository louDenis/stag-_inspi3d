import math
from vray import Renderer, AColor, Transform, Matrix, Vector
import random
import pandas as pd
from locale import atof, setlocale, LC_NUMERIC
#------------------------------------------------------------------------------

def string_to_vec_main_pos(pos_main_furniture):

    if pos_main_furniture != 'd':
        pos_main_furniture = pos_main_furniture.split(" ")
        pos_main_furniture = [float(x) for x in pos_main_furniture]
        return Vector(pos_main_furniture[0], pos_main_furniture[1], pos_main_furniture[2])

#--------------------------------------------------------------------------------
#fonction qui prend en entrée la liste brute de coords et renvoie la liste avec
#les vecteurs correspondants aux coordonnées
def string_to_vec(pos_main_furniture, list_pos_accessories):

    if pos_main_furniture != 'd':
        pos_main_furniture = pos_main_furniture.split(" ")
        pos_main_furniture = [float(x) for x in pos_main_furniture]
        pos_main_furniture = Vector(pos_main_furniture[0], pos_main_furniture[1], pos_main_furniture[2])

    for i in range(len(list_pos_accessories)):
        if list_pos_accessories[i] != 'd' :
            list_pos_accessories[i] = list_pos_accessories[i].split(" ")
            list_pos_accessories[i] = [float(x) for x in list_pos_accessories[i]]
            list_pos_accessories[i] = Vector(list_pos_accessories[i][0], list_pos_accessories[i][1], list_pos_accessories[i][2])

    return pos_main_furniture, list_pos_accessories

#fonction qui prend en entrée la liste des meubles et la liste de leur dimensions
#et renvoie en sortie la liste des coordonnées associées à chaque meubles

#fonction qui prend en entrée les coordonnées du meuble principal et la liste
#d'accessoires et renvoie la liste des positions des accessoires
def setup_relative_coords(pos_main_furniture, list_accessories, list_relative_pos_accessories):
    print("------------setup_relative_coords--------------")
    pos_main_furniture, list_relative_pos_accessories = string_to_vec(pos_main_furniture, list_relative_pos_accessories)
    #liste de la position absolue des accessoires en fonction de leur position relative au meuble principal
    list_pos_accessories = []
    for i in range(len(list_relative_pos_accessories)):
        print(list_accessories[(i*2)+1])
        list_pos_accessories.append(list_relative_pos_accessories[i] + pos_main_furniture)
    print("list pos=", list_pos_accessories)
    return pos_main_furniture,list_pos_accessories

#fonction qui genere des coordonnées absolues au hasard avec un pas de 10
#et comprises entre 150 et -150 pour x et 180 et -180 pour y
def generate_random_absolute_pos():
    rd_x = random.randrange(-150, 150, 10)
    rd_y = random.randrange(-180, 180, 10)
    return Vector(float(rd_x), float(rd_y), 0.0)


#fonction qui detecte la collison entre 2 objets
def check_collision(pos1, dim1, pos2, dim2):
    print("\t pos1=", pos1)
    print("\t pos2=", pos2)
    print("\t dim1=", dim1)
    print("\t dim2=", dim2)
    collisionX = pos1.x + dim1.x >= pos2.x and pos2.x + dim2.x >= pos1.x
    collisionY = pos1.y + dim1.y >= pos2.y and pos2.y + dim2.y >= pos1.y
    print("\t", collisionX and collisionY)
    return collisionX and collisionY


#fonction qui genere les coordonnees absolue des accessoires
def generate_random_abs_pos_accessories(list_accessories):
    pos_acc = []
    is_odd = len(list_accessories)%2 == 1
    for i in range(len(list_accessories)//2 + is_odd):
        coords = generate_random_absolute_pos()
        """collision = is_there_collision(pos_main_furniture, coords, pos_acc, i)
        while(not collision):
            coords = generate_random_absolute_pos()
            collision = is_there_collision(pos_main_furniture, coords, pos_acc, i)"""
        pos_acc.append(coords)
    return pos_acc
