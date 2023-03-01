# %%
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from DataAugmentationForObjectDetection.data_aug.data_aug import * #Script in the folder
from DataAugmentationForObjectDetection.data_aug.bbox_util import *

# %%
#Split the images from train,valid and test folders into lists 
def image_distribution(path,dirlist):
    train,valid,test = [],[],[]
    for dir in dirlist:
        for img in os.listdir(os.path.join(path,dir)):
            if img.endswith(".jpg"):# Get only the images
                test.append(os.path.join(path,dir,img)) if dir == 'test' else (train.append(os.path.join(path,dir,img)) if dir == 'train' else valid.append(os.path.join(path,dir,img)))
    return train,valid,test

# %%
#Return a list which is having bounding box annotion format as required by data_aug.py methods  [x1,y1,x2,y2,class] for training test and validdation images 
def ano_distribution(path,dirlist):
    import xml.etree.cElementTree as et
    train,valid,test = [],[],[]
    for dir in dirlist:
        for annotation in os.listdir(os.path.join(path,dir)):
            if annotation.endswith(".xml"): # Get the xml files only 
                tree = et.parse(os.path.join(path,dir,annotation))
                root = tree.getroot()
                anno = []
                for tag in root.findall('object'):#iterates through all the labled objects in the image
                    order = [0,2,1,3] 
                    temp = [subtag.text for subtag in tag[5]] # Store coordinates of bounding box in a list
                    temp = [temp[i] for i in order] # Reordering the list to be x1,y1,x2,y2 instead of x1,x2,y1,y2
                    temp.append(tag[0].text) #Get the class  
                    anno.append(temp)
                test.append(anno) if dir == 'test' else (train.append(anno) if dir == 'train' else valid.append(anno))
    return train,valid,test

# %%
#def main():
path = os.path.join(os.getcwd(),"Data")
directories = [dirnames for root,dirnames,filenames in os.walk(path)][0]

train_img,valid_img,test_img = image_distribution(path,directories) #Storing images
train_ano,valid_ano,test_ano = ano_distribution(path,directories) #Storing annotations

# %%
import itertools
list2 = train_ano.copy()
labels = {'Back_Rest':1,'Seat':2,'Left_armrest':3,'Right_armrest':4,'Base':5}
for obj in itertools.chain.from_iterable(list2):
    obj[4] = labels[obj[4]]

# %%
ar = np.array(list2[0],dtype='float64')

# %%
test_img = cv2.imread(train_img[0])[:,:,::-1] #opencv loads images in bgr. This converts it into rgb
#test_anno = train_ano[0]
img_,bboxes_ = RandomHorizontalFlip(1)(test_img.copy(),ar.copy())
plotted_img = draw_rect(img_,bboxes_)
plt.imshow(plotted_img)
plt.show()