import math
from vray import Renderer, AColor, Transform, Matrix, Vector
#------------------------------------------------------------------------------
#fonction qui recup les options de l'utilisateur concernant la position des meubles.
#Renvoie un dictionnaire avec en clé un meuble et en valeur une position
def setup_positions(list_main_furniture, list_accessories):
    answer = input("Do you want to set up positions for certain furnitures (if you choose not to, posistions by default will be setted) ?(y/n)")
    if (answer == 'n'):
        print(answer) #setup coords par defaut en respectant les contraintes
        return 'd', ['d', '1.2 1.2 1.2']
    elif (answer ==  'y'):
        print('Format: x coordinates, y coordinates, z coordinates OR "d" if you want default coordinates')
        message = "\t"+ list_main_furniture[1] + "\t"
        pos_main_furniture = input(message)

        list_pos_accessories = []
        for i in range(1, (len(list_accessories)//2)+2, 2):
            message = "\t"+ list_accessories[i] + "\t"
            list_pos_accessories.append(input(message))
        return pos_main_furniture, list_pos_accessories

    else:
        print("ERROR: you must press y or n to setup positions")
        setup_positions(list_main_furniture, list_accessories)
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
