#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 17:20:58 2024

@author: root
"""

import pandas as pd


db_path = 'C:/Users/Mucho/Work/mac/Target/Pickles/'

def objToStr(dataframe):    
    trues     = [dataframe.dtypes == 'O']
    dataframe = dataframe.astype({col: 'string' for col in trues[0][trues[0] == True].index})
    return dataframe


def tractor_claw(dataframe,col_1,col_2):
    
    nas = dataframe.loc[:,[col_1,col_2]].fillna('vazio')
    idx = nas.loc[nas.loc[:,col_1].str.contains('vazio'),col_1].index
    dataframe.loc[idx,col_1] = nas.loc[idx,col_2]
    dataframe.drop(col_2,axis=1,inplace=True)
    return dataframe


def save_pkl(obj, name='object', path=db_path):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
        file.close()

def load_pkl(name='object', path=db_path):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data