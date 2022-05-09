#!/usr/bin/python
import sys, getopt
from converter import parse_vray_text
from launch_rendering import convert_config
import vray
from renderer.VRayFurniture import VRayFurniture
from setup_coords import setup_positions, string_to_vec
from constraints_solver import solver
import get_random
#fonction qui prend en entrée les données brutes (chaine de caractere) et qui
#donne en sortie la liste traitée (suite consecutive de num catalogue, puis nom
#du meuble en string)
def get_list(raw_furniture):
    raw_list= list(raw_furniture.split(" "))
    res_list = []
    temp = []
    bool_end = False
    max_iter = 0
    for i in range(len(raw_list)):
        #print("i=", i, "max_iter=", max_iter)
        if (i - max_iter != 0):
            #print("oui")
            continue
        if bool_end :
            break

        #print("i=",i, "raw_list[i]=", raw_list[i])
        temp = []
        for j in range(i, len(raw_list)):
            #print("\t temp=", temp)
            max_iter = j
            if j == (len(raw_list)-1):
                bool_end = True
            if raw_list[j] != 'and':
                temp.append(raw_list[j])
            else:
                break
        if temp != []:
            num_catalog = temp[0]
            #print("temp 0=", temp[0])
            ref_furniture = temp[1:]
            #print("ref =", ref_furniture)
            res_list.append(num_catalog)
            res_list.append(" ".join(str(x) for x in ref_furniture))
        max_iter += 1
    #print(res_list)
    return res_list

#-------------------------------------------------------------------------------
#fonction qui prend en entrée la liste des meubles et renvoie la liste des config associée à ces meubles
def build_config(list_furniture):
    list_config = []
    for i in range(0, (len(list_furniture)//2)+1, 2):
        config = parse_vray_text.generate_config(list_furniture[i], list_furniture[i+1])
        convert_config(config)
        asset = parse_vray_text.get_config_asset(config)
        list_config.append(asset)
    return list_config

#-------------------------------------------------------------------------------
#fonction qui prend en entrée la liste des meubles main et accessories et fait le rendu
def render(list_config_main, list_config_accessories):
    renderer = vray.Renderer()
    renderer.load('templates/preview_2018/preview_2018.vrscene')
    furniture_main = VRayFurniture(renderer=renderer, config_data=list_config_main[0])
    furniture_main.move_y(-150)
    furniture_main.move_x(180)


    #for i in range(len(list_config_accessories)):
    #    d["furniture{0}".format(i)] = VRayFurniture(renderer=renderer, config_data=list_config_accessories[0])

    furniture1 = VRayFurniture(renderer=renderer, config_data=list_config_accessories[0])
    furniture1.move_x(100)
    furniture2 = VRayFurniture(renderer=renderer, config_data=list_config_accessories[1])
    furniture2.move_y(150)

    print("max main= ", furniture_main.maximum)
    print("min main = ", furniture_main.minimum)
    print("max canap=", furniture1.maximum)
    print("min canap=", furniture1.minimum)

    #solver(furniture_main.maximum, furniture_main.minimum, furniture1.maximum, furniture1.minimum)

    renderer.start()
    renderer.waitForRenderEnd()

#-------------------------------------------------------------------------------
#fonction qui lit les param de l'utilisateur (main furniture,accessories et position associée)
def main(argv):
    opt_random = False
    print("-------------------WELCOME IN THE SCENE GENERATOR------------------\n \n")
    if sys.argv[1] != '-i' or (len(sys.argv) > 3 and sys.argv[3] != '-o' ):
        print('usage: test.py -i <main_furniture> -o <accessories>')
        print('\n You must enter informations as followed \n for each furniture: (in quotes) "furniture_ref catalog_num" \n Every furniture ref and catalog must be separated by the keyword "and"')
        print('\n EXAMPLE: python furniture_and_accessories.py -i "543 420042" -o "560 Canapé and 636 Armoire test bois"')
        print('\n If you wish to pick accessories randomly, just write "random" after -o option \n \n')
        sys.exit(1)
    main_furniture = ''
    accessories = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print('test.py -i <main_furniture> -o <accessories>')
      sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("NEED SOME HELP ? \n")
            print('usage: test.py -i <main_furniture> -o <accessories>')
            print('You must enter informations as followed \n for each furniture: (in quotes) "furniture_ref catalog_num" \n Every furniture ref and catalog must be separated by the keyword "and"')
            print('If you wish to pick accessories randomly, just write "random" and the catalog number after -o')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            main_furniture = arg
        elif opt in ("-o", "--ofile"):
            accessories = arg

    print('main_furniture is "', main_furniture)
    print("accessories are ", accessories )

    #si l'utilisateur a mit les accessoires en aléatoire
    rd_options = (opts[1][1]).split(" ")

    if rd_options[0] == "random" :
        opt_random = True
        catalog_number = rd_options[1]
        list_accessories = get_random.get_random_accessories(catalog_number)
        print("random list_accessories =", list_accessories )

    print("opts=", opts)


    if (opts[0][1] == '-o'):
        print("ERROR: you must enter exactly one furniture")
        sys.exit(2)

    #cast les string en liste est associer les ref à leur num de catalogue
    list_main_furniture= get_list(main_furniture)

    if not opt_random :
        list_accessories= get_list(accessories)


    if (len(list_main_furniture) != 2):
        print("ERROR: you must enter exactly one main furniture")
        sys.exit(2)

    #construire les asset correspondant à chaque meuble
    list_config_main_furniture = build_config(list_main_furniture)
    print("listes before build config", list_main_furniture,list_accessories)
    print("aaaaaaaaaa", list_accessories)
    list_config_accessories = build_config(list_accessories)

    #print(list_config_accessories[0])

    pos_main_furniture, list_pos_accessories = setup_positions(list_main_furniture, list_accessories)
    print(pos_main_furniture)
    print(list_pos_accessories)

    #string_to_vec(pos_main_furniture, list_pos_accessories)
    render(list_config_main_furniture, list_config_accessories)




    #print('main furniture is', main_furniture)
    #print('accessories are', accessories)

#------------------------------------MAIN--------------------------------------
if __name__ == "__main__":
   main(sys.argv[1:])
