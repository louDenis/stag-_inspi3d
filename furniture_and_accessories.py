from converter import parse_vray_text
from launch_rendering import convert_config
import vray
from renderer.VRayFurniture import VRayFurniture

#fonction qui prend en entrée les données brutes (chaine de caractere) et qui
#donne en sortie la liste traitée (suite consecutive de num catalogue, puis nom
#du meuble en string)
def get_list(raw_furniture):
    print("****************GET LIST***********")
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
    print(res_list)
    return res_list

def build_config(list_furniture):
    list_config = []
    for i in range(0, (len(list_furniture)//2)+1, 2):
        config = parse_vray_text.generate_config(list_furniture[i], list_furniture[i+1])
        convert_config(config)
        asset = parse_vray_text.get_config_asset(config)
        list_config.append(asset)
        print(len(list_config))
    return list_config

def render(list_config_main, list_config_accessories):
    renderer = vray.Renderer()
    renderer.load('templates/preview_2018/preview_2018.vrscene')
    furniture_main = VRayFurniture(renderer=renderer, config_data=list_config_main[0])

    furniture1 = VRayFurniture(renderer=renderer, config_data=list_config_accessories[0])
    furniture1.move_x(100)
    furniture2 = VRayFurniture(renderer=renderer, config_data=list_config_accessories[1])

    renderer.start()
    renderer.waitForRenderEnd()


"""
def render():
    config_table = parse_vray_text.generate_config("543", "420042")
    asset_table = parse_vray_text.get_config_asset(config_table)

    config_canap = parse_vray_text.generate_config("560", "Canapé")
    convert_config(config_canap)
    asset_canap = parse_vray_text.get_config_asset(config_canap)


    renderer = vray.Renderer()
    renderer.load('templates/preview_2018/preview_2018.vrscene')
    furniture = VRayFurniture(renderer=renderer, config_data=asset_canap)
    furniture2 = VRayFurniture(renderer=renderer, config_data=asset_table)
    print("max et min=", furniture.maximum, furniture.minimum)
    print("max et min 2=", furniture2.maximum, furniture2.minimum)
    renderer.start()
    renderer.waitForRenderEnd()
"""
#!/usr/bin/python
import sys, getopt

def main(argv):
    if sys.argv[1] != '-i' or (len(sys.argv) > 3 and sys.argv[3] != '-o'):
        print('usage: test.py -i <main_furniture> -o <accessories>')
        print('You must enter informations as followed \n for each furniture: (in quotes) "furniture_ref catalog_num" \n Every furniture ref and catalog must be separated by the keyword "and"')
        print('EXAMPLE: python furniture_and_accessories.py -i "543 420042" -o "560 Canapé and 636 Fauteuil Highpoly sans AO"')
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
            print('usage: test.py -i <main_furniture> -o <accessories>')
            print('You must enter informations as followed \n for each furniture: (in quotes) "furniture_ref catalog_num" \n Every furniture ref and catalog must be separated by the keyword "and"')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            main_furniture = arg
        elif opt in ("-o", "--ofile"):
            accessories = arg
    print("---------------------------------------------------------------")
    print('main_furniture is "', main_furniture)
    print("opts=", opts)
    print("---------------------------------------------------------------")

    if (opts[0][1] == '-o'):
        print("ERROR: you must enter exactly one furniture")
        sys.exit(2)

    #cast les string en liste est associer les ref à leur num de catalogue
    list_main_furniture= get_list(main_furniture)
    list_accessories= get_list(accessories)

    if (len(list_main_furniture) != 2):
        print("ERROR: you must enter exactly one main furniture")
        sys.exit(2)

    #construire les asset correspondant à chaque meuble
    """list_config_main_furniture = build_config(list_main_furniture)
    list_config_accessories = build_config(list_accessories)

    render(list_config_main_furniture, list_config_accessories)"""


    #print('main furniture is', main_furniture)
    #print('accessories are', accessories)

if __name__ == "__main__":
   main(sys.argv[1:])
   #render()
