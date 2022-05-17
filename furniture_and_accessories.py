#!/usr/bin/python
import sys, getopt
from converter import parse_vray_text
from launch_rendering import convert_config
import vray
from renderer.VRayFurniture import VRayFurniture
import bounding_box
import get_random
import read_json

#-------------------------------------------------------------------------------
#fonction qui prend en entrée la liste des meubles et renvoie la liste des config associée à ces meubles
def build_config(list_furniture):
    list_config = []
    print(len(list_furniture))
    for i in range(0, len(list_furniture)//2):
        print("i=", i, list_furniture[i*2], list_furniture[(i*2)+1])
        config = parse_vray_text.generate_config(list_furniture[i*2], list_furniture[(i*2)+1])
        convert_config(config)
        asset = parse_vray_text.get_config_asset(config)
        list_config.append(asset)
    return list_config

#-------------------------------------------------------------------------------
#fonction qui prend en entrée la liste des meubles main et accessories et fait le rendu
def render(list_config_main, list_config_accessories,pos_main_furniture,list_pos_accessories):
    print("list_config_accessories=", len(list_config_accessories))
    renderer = vray.Renderer()
    renderer.load('templates/preview_2018/preview_2018.vrscene')
    furniture_main = VRayFurniture(renderer=renderer, config_data=list_config_main[0])
    print("-----------------")
    print(type(pos_main_furniture))
    print(pos_main_furniture)
    print("-----------------")
    furniture_main.move(pos_main_furniture)

    dict_accessories = {}
    for i in range(len(list_pos_accessories)):
        dict_accessories["furniture%s" %i] = VRayFurniture(renderer=renderer, config_data=list_config_accessories[i])
        dict_accessories["furniture%s" %i].move(list_pos_accessories[i])
        dict_accessories["furniture%s" %i].minimum = dict_accessories["furniture%s" %i].minimum/10
        dict_accessories["furniture%s" %i].maximum = dict_accessories["furniture%s" %i].maximum/10

    furniture_main.minimum = furniture_main.minimum/10
    furniture_main.maximum = furniture_main.maximum/10
    for i in range(len(list_pos_accessories)):
        print("bounding box", i)
        bounding_box.intersect(furniture_main, dict_accessories["furniture%s" %i])
    for key, value in dict_accessories.items() :
        print (key, value)

    renderer.start()
    renderer.waitForRenderEnd()
    image = renderer.getImage()
    image.save('intro.png')

#-------------------------------------------------------------------------------
#fonction qui lit les param de l'utilisateur (main furniture,accessories et position associée)
def main(argv):

    list_main_furniture, list_accessories, pos_main_furniture, list_pos_accessories= read_json.read_json('data/data_file.json')
    print("new_list_main_furniture=", list_main_furniture)
    print("new_list_accessories=", list_accessories)

    #construire les asset correspondant à chaque meuble
    list_config_main_furniture = build_config(list_main_furniture)
    list_config_accessories = build_config(list_accessories)

    render(list_config_main_furniture, list_config_accessories, pos_main_furniture,list_pos_accessories)



    #print('main furniture is', main_furniture)
    #print('accessories are', accessories)

#------------------------------------MAIN--------------------------------------
if __name__ == "__main__":
   main(sys.argv[1:])
