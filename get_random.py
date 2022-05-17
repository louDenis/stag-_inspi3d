
import pandas as pd
import random

#fonction qui prend en entrée une base de données de meuble et un nombre d'accessoires désirés
#et renvoie une liste d'accessoires brute générés aléatoirement
def get_random_furniture_from_csv(catalog_numbers, nb):
    #data= pd.read_excel(os.path.join(APP_PATH, "Data", "aug_latest.xlsm"),
     #engine='openpyxl',
     print("catalog_numbers=", catalog_numbers)
     catalog_number = catalog_numbers[0]
     path = 'data/'+catalog_number+'.xlsx'
     data= pd.read_excel(path)
     df = pd.DataFrame(data, columns= ['reference'])
     df = df.iloc[3: , :]
     nb_item_in_catalog = []
     nb_item_in_catalog.append(df.shape[0])

     for i in range(1, len(catalog_numbers)):
         print("catalog numberzzzzzzz = ", catalog_numbers)
         catalog_number = catalog_numbers[i]
         print("catalog_number= ", catalog_number)
         path = 'data/'+catalog_number+'.xlsx'
         data= pd.read_excel(path)
         df1 = pd.DataFrame(data, columns= ['reference'])
         nb_item_in_catalog.append(df1.shape[0])
         #df1 = df.iloc[3: , :]
         print(df1)
         df = df.append(df1)

     #construire la colonne catalogue
     catalog_col= []
     for i in range(len(nb_item_in_catalog)):
         for j in range(nb_item_in_catalog[i]):
             catalog_col.append(catalog_numbers[i])
     df['Catalog'] = catalog_col
     #enelver les lignes ou il est écrit "Reference"
     df.drop(df.index[df['reference'] == 'Référence'], inplace=True)
     print(df)

     furniture = []
     catalog_associated = []
     #choisir au hasard des meubles dans le dataframe complet
     for i in range(nb):
        rd_nb = random.randint(0, df.shape[0]-1)
        r= df.iat[rd_nb, 0]
        c= df.iat[rd_nb, 1]
        r = str(r)
        furniture.append(r)
        catalog_associated.append(c)
     print("furniture= " ,furniture)
     print("catalog_associated=", catalog_associated)
     return furniture, catalog_associated

#fonction qui prend en entrée une liste de furniture brute et renvoie la liste au format exploitable
#par la suite du programme
def transform_raw_data(raw_list, catalog_associated):
    res = []
    print("longueur raw_list = ", len(raw_list))
    for i in range(len(raw_list)):
        res.append(catalog_associated[i])
        res.append(raw_list[i])
        print("res=", res)
    return res

def get_random_accessories(catalog_number, nb_acc_random):
    #'data/500.xlsx'
    raw_accessories, catalog_associated = get_random_furniture_from_csv(catalog_number, int(nb_acc_random))
    print("raw acc= ", raw_accessories)
    list_accessories = transform_raw_data(raw_accessories, catalog_associated)
    return list_accessories
