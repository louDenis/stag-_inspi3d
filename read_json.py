import json
import get_random
import setup_coords

def read_json(file):
    # Opening JSON file
    f = open(file)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    #create list_main_furniture
    list_main_furniture = []
    list_main_furniture.append(data['furniture']['catalog_id'])
    list_main_furniture.append(data['furniture']['reference'])

    #read options random accessories
    random_accessories = data['random_accessories']
    if random_accessories :
        nb_accessories_random = data['nb_accessories_random']
        catalog_numbers = data['catalog_numbers']
        list_accessories = get_random.get_random_accessories(catalog_numbers, nb_accessories_random)
    else:
        #create list_accessories
        list_accessories = []
        for i in range(len(data['accessories'])):
            list_accessories.append(data['accessories'][i]['catalog_id'])
            list_accessories.append(data['accessories'][i]['reference'])

    #read main furniture pos
    pos_main_furniture = data['pos_main_furniture']
    print('JSON pos_main_furniture=', pos_main_furniture)

    #read options position (random or not)
    if data['random_position'] :
        list_pos_accessories= setup_coords.generate_random_abs_pos_accessories(list_accessories)
        print('JSON list_pos_accessories', list_pos_accessories)
        return list_main_furniture, list_accessories,setup_coords.string_to_vec_main_pos(pos_main_furniture),list_pos_accessories

    else:
        list_pos_accessories= data['pos_accessories']
        #read options position (absolute position or not)
        if data['relative_position'] :
            print('JSON RELATIVE POSITION')
            pos_main_furniture,list_pos_accessories = setup_coords.setup_relative_coords(pos_main_furniture, list_accessories, list_pos_accessories)
            return list_main_furniture, list_accessories, pos_main_furniture,list_pos_accessories
        else:
            print('JSON NOT RELATIVE POSITION')
            pos_main_furniture,list_pos_accessories= setup_coords.string_to_vec(pos_main_furniture, list_pos_accessories)
            return list_main_furniture, list_accessories, pos_main_furniture,list_pos_accessories

    # Closing file
    f.close()

    return list_main_furniture, list_accessories, pos_main_furniture, list_pos_accessories
