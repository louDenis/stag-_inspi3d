import pandas as pd
import cv2
from matplotlib import pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import numpy as np


file = 'furniture_data_img.csv'
path = '/home/lou/Documents/stage/data/furnitures/'+file
fp = open(path)

data= pd.read_csv(fp)
#data.apply(set)
#get vector of existing labels
#print(data.Furniture_Type)
labels= list(data.apply(set)[1])
print(labels)


#img = cv2.imread(jpp)
path2 = '/home/lou/Documents/stage/data/furnitures/furniture_images'
jpp = path2+data.Image_File[200]
print(jpp)
img = cv2.imread(jpp)
#plt.imshow(img)
#plt.show()

print("taille du dataset")
print(data.shape)
print("dimension des images")
print(img.shape)

#separation du jeu de données en train et test train avec un ratio 80-20
train = data.head(7476)
test = data.tail(1870)

x_train = train.Furniture_Type
y_train = path2 + train.Image_File

x_test = test.Furniture_Type
y_test = path2 + test.Image_File


plt.figure(figsize=(13,20))

#affichage de quelques images avec leur label
"""n = 0
for i in range(10):
    for j in range(5):
        plt.axis('off')
        # récupération d'une image et de son label associé
        target, path2img = x_train[n+j], y_train[n+j]
        # affiche du spectrogramme
        plt.subplot(10,5,i*5+j+1)
        img = cv2.imread(path2img)
        plt.imshow(img)
        # ajout d'un titre à l'image
        plt.title('{}'.format(target))
        #plt.colorbar(format='%+2.0f dB')
    n += 32

plt.show()"""

#modification des données: on ne manipule plus le chemin vers les images mais
#les images en elles-memes + on ne manipule plus les chaines de carac de
#la classe mais un num représentant la classe
def get_img_from_path(path2img):
    img = cv2.imread(path2img)
    return img

def class_to_idx(my_class):
    return labels.index(my_class)

x_train = x_train.apply(class_to_idx)
y_train = y_train.apply(get_img_from_path)

x_test = x_test.apply(class_to_idx)
y_test = y_test.apply(get_img_from_path)


#création d'un data loader pour les jeux de données train et test

# numpy vers tensors
y_train = y_train.to_numpy()
x_train = x_train.to_numpy()

y_test = y_test.to_numpy()
x_test = x_test.to_numpy()
#y_train = torch.from_numpy(y_train)

nb_classes = 9


class Dataset(torch.utils.data.Dataset):
  'Characterizes a dataset for PyTorch'
  def __init__(self, x_data, y_labels):
        'Initialization'
        self.y = y_labels
        self.x = x_data

  def __len__(self):
        'Denotes the total number of samples'
        return len(self.x)

  def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample
        X = self.x[index].unsqueeze_(0)
        y = self.y[index]

        return X, y

dataset_train = Dataset(x_train, y_train)
dataset_test = Dataset(x_test, y_test)
