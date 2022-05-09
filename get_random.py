
import pandas as pd
import random

#fonction qui prend en entrée une base de données de meuble et un nombre d'accessoires désirés
#et renvoie une liste d'accessoires brute générés aléatoirement
def get_random_furniture_from_csv(catalog_number, nb):
    #data= pd.read_excel(os.path.join(APP_PATH, "Data", "aug_latest.xlsm"),
     #engine='openpyxl',
    path = 'data/'+catalog_number+'.xlsx'
    data= pd.read_excel(path)
    df = pd.DataFrame(data, columns= ['reference'])
    df = df.iloc[3: , :]
    #print(df)
    furniture = []
    for i in range(nb):
        rd_nb = random.randint(0, data.shape[0]-1)
        r= df.iat[rd_nb, 0]
        r = str(r)
        furniture.append(r)
    return furniture

#fonction qui prend en entrée une liste de furniture brute et renvoie la liste au format exploitable
#par la suite du programme
def transform_raw_data(raw_list, num_catalog):
    res = []
    print("longueur raw_list = ", len(raw_list))
    for i in range(len(raw_list)):
        print("i=", i, i%2)
        res.append(str(num_catalog))
        res.append(raw_list[i])
        print(res)
    return res

def get_random_accessories(catalog_number):
    #'data/500.xlsx'
    raw_accessories = get_random_furniture_from_csv(catalog_number, 2)
    print("raw acc= ", raw_accessories)
    list_accessories = transform_raw_data(raw_accessories, 500)
    return list_accessories
