# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:41:13 2017

@author: jiang_y
"""

############### Load annotations from json file ###################
import os
import pickle
from shutil import copyfile
from scipy.misc import imread
#from six.moves import cPickle as pickle
#HOME_DIR = r'C:\Users\jiang_y\Documents\MachineLearning\Fastai\courses\deeplearning1\nbs'
#os.chdir(HOME_DIR)

#path = os.getcwd()
#path = 'train/'




#file_path = r'C:\Users\jiang_y\Documents\MachineLearning\Kaggle\Fish\train_anno\cfg_yoyo\bb_json.pickle'
file_path = 'data/bb_json.pickle'
#with open(file_path, 'wb') as f:
#    pickle.dump([bb_json], f) 
with open(file_path, 'rb') as f:
    bb_json = pickle.load(f)[0]
    

path = 'train/'
path_dst = 'fish/'
if not os.path.exists(path_dst): os.mkdir(path_dst)
#os.chdir(HOME_DIR)
folders = ['ALB', 'BET', 'DOL', 'LAG', 'OTHER', 'SHARK', 'YFT']
fish_class = {'ALB':0, 'BET':1, 'DOL':2, 'LAG':3, 'OTHER':4, 'SHARK':5, 'YFT':6}

for folder in folders:
    cur_dir = os.path.join(path,folder)
    files = os.listdir(cur_dir)
    for f in files:
        if f in bb_json.keys():
            new_name = '_'.join([folder,f])
            new_path = os.path.join(path_dst,new_name)
            old_path = os.path.join(cur_dir,f)
            copyfile(old_path,new_path)
            im_array = imread(new_path)  # [height(y),width(x),channel]
            img_h = im_array.shape[0]
            img_w = im_array.shape[1]
            
            txt_name = new_name.replace('.jpg','.txt')
            text_file = open(os.path.join(path_dst,txt_name), 'w')
    
            for a in bb_json[f]:
                x = (a['x'] + a['x'] + a['width'])*0.5/img_w
                y = (a['y'] + a['y'] + a['height'])*0.5/img_h
                w = a['width']/img_w
                h = a['height']/img_h
                str_anno = format('%d %.6f %.6f %.6f %.6f\n'%(fish_class[folder],x,y,w,h))
                text_file.write(str_anno)
            text_file.close()
        else:
            print('%s_%s has no annotation\n'%(folder,f))